#!/usr/bin/env python3
"""
File Parser CLI
PDF processing pipeline: removes headers/footers, converts to markdown, and generates image captions.
"""

import subprocess
import os
import glob
import argparse
from os.path import join
from pathlib import Path
import shutil
import hashlib
import re
from PIL import Image
from mlx_vlm import load, generate
from mlx_vlm.prompt_utils import apply_chat_template
from mlx_vlm.utils import load_config
from file_parser.pdf_parser import PDFExtractor

# Model configuration
MODEL_PATH = "mlx-community/InternVL3-1B-4bit"
PROMPT = "Describe the image in detail. Extract important text from graphs, diagrams, or tables if they appear in the image, and be specific about it."

# Load the model once (lazy loading)
_model = None
_processor = None
_config = None


def _load_model():
    """Lazy load the MLX VLM model to avoid loading it if not needed."""
    global _model, _processor, _config
    if _model is None:
        print("Loading MLX VLM model...")
        _model, _processor = load(MODEL_PATH)
        _config = load_config(MODEL_PATH)
        print("Model loaded successfully.")
    return _model, _processor, _config


def extract_data(pdf_path, output_path):
    """Convert PDF to markdown using marker_single."""
    bash_command = f'marker_single "{pdf_path}" --output_dir "{output_path}"'
    process = subprocess.Popen(
        bash_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    output, error = process.communicate()

    print("Output:")
    print(output.decode("utf-8"))

    print("Error:")
    print(error.decode("utf-8"))

    return_code = process.returncode
    return return_code == 0


def image_to_caption(image_path):
    """
    Generate a caption for an image using MLX VLM (InternVL).
    
    Args:
        image_path: Path to the image file
        
    Returns:
        str: Generated caption text
    """
    # Load model if not already loaded
    model, processor, config = _load_model()
    
    # Load image using PIL
    image = [Image.open(image_path)]
    
    # Apply chat template
    formatted_prompt = apply_chat_template(
        processor, config, PROMPT, num_images=len(image)
    )
    
    # Generate output
    response = generate(model, processor, formatted_prompt, image, verbose=False)
    
    # Extract text from GenerationResult object
    if isinstance(response, str):
        response_text = response
    else:
        # Try to get text from GenerationResult object
        try:
            if hasattr(response, 'text'):
                response_text = response.text
            elif hasattr(response, 'generated_text'):
                response_text = response.generated_text
            elif hasattr(response, 'output'):
                response_text = response.output
            elif hasattr(response, '__getitem__'):
                response_text = response[0] if len(response) > 0 else str(response)
            else:
                response_text = str(response)
        except Exception as e:
            print(f"Warning: Could not extract text from response: {e}")
            print(f"Response type: {type(response)}")
            print(f"Response attributes: {dir(response)}")
            response_text = str(response)
    
    # Clean up the response (remove newlines and extra whitespace)
    if isinstance(response_text, str):
        response_text = response_text.replace('\n', ' ').strip()
    else:
        response_text = str(response_text).replace('\n', ' ').strip()
    
    print('\n', image_path)
    print(response_text, '\n')
    return response_text


def pipeline(input_dir, output_dir):
    """
    Process PDF files from input directory and output processed markdown files.
    
    Args:
        input_dir: Directory containing PDF files to process
        output_dir: Directory to save processed markdown files
    """
    # Normalize paths
    input_dir = os.path.abspath(input_dir)
    output_dir = os.path.abspath(output_dir)
    
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Copy non-PDF files to output directory
    all_files = glob.glob(join(input_dir, "*.*"))
    for p in all_files:
        if not p.endswith('.pdf'):
            shutil.copyfile(p, join(output_dir, os.path.basename(p)))
    
    # Process PDF files
    pdf_ls = glob.glob(join(input_dir, "*.pdf"))
    
    # Create temporary directories for processing
    header_removed_path = join(input_dir, 'header_footer_remove')
    md_dir = join(header_removed_path, 'markdown')
    
    if not os.path.exists(header_removed_path):
        os.makedirs(header_removed_path)
    
    for pdf_file in pdf_ls:
        root, file_name = os.path.split(pdf_file)
        print('# PROCESSING', file_name)
        
        # Step 1: Remove headers and footers
        removed_file_path = join(header_removed_path, file_name)
        if not Path(removed_file_path).is_file():
            print('### Remove headers and footers', removed_file_path)
            pdf_extractor = PDFExtractor(pdf_file, removed_file_path)
            pdf_extractor.run()
        else:
            print('### Skip removing headers and footers')
        
        # Step 2: Convert to Markdown
        base_name = file_name.rstrip('.pdf')
        file_hash = str(int(hashlib.sha1(pdf_file.encode("utf-8")).hexdigest(), 16) % (10 ** 5))
        md_file = join(md_dir, file_hash, base_name, base_name + '.md')
        
        if not Path(md_file).is_file():
            print('### Convert to Markdown', md_file)
            extract_data(removed_file_path, join(md_dir, file_hash))
        else:
            print('### Skip converting to Markdown')
        
        # Step 3: Generate image captions and create final markdown
        md_file_caption = join(output_dir, base_name + '.md')
        if not Path(md_file_caption).is_file():
            print('### Captionize images', md_file_caption)
            content = open(md_file, 'r').read()
            content = content.replace('_Image_', '_image_').replace('.Png]', '.png]').replace('.Png)', '.png)').replace('.png]', f'_{file_hash}.png]')
            
            # Find all image files (png, jpeg, jpg, etc.) in the markdown directory
            image_dir = join(join(md_dir, file_hash), base_name)
            image_extensions = ['*.png', '*.jpeg', '*.jpg', '*.PNG', '*.JPEG', '*.JPG']
            image_ls = []
            for ext in image_extensions:
                image_ls.extend(glob.glob(join(image_dir, ext)))
            
            # Process each image found
            for image_path in image_ls:
                _, img_name = os.path.split(image_path)
                print(f'Processing image: {img_name}')
                
                # Generate caption
                caption = image_to_caption(image_path)
                
                # Replace markdown image syntax: ![](...) or ![alt](...) with ![caption](...)
                escaped_img_name = re.escape(img_name)
                pattern = rf'!\[([^\]]*)\]\({escaped_img_name}\)'
                replacement = f'![{caption}]({img_name})'
                content = re.sub(pattern, replacement, content)
            
            with open(md_file_caption, 'w') as f:
                f.write(content)
        else:
            print('### Skip image captionization')
        print('### Done!')
    
    print(f'\n### All files processed. Output saved to: {output_dir}')


def main():
    """Main function to handle command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Process PDF files: remove headers/footers, convert to markdown, and generate image captions.'
    )
    parser.add_argument(
        'input_dir',
        type=str,
        help='Input directory containing PDF files to process'
    )
    parser.add_argument(
        'output_dir',
        type=str,
        help='Output directory for processed markdown files'
    )
    
    args = parser.parse_args()
    
    # Validate input directory exists
    if not os.path.exists(args.input_dir):
        print(f"Error: Input directory does not exist: {args.input_dir}")
        return
    
    # Run the pipeline
    pipeline(args.input_dir, args.output_dir)


if __name__ == "__main__":
    main()

