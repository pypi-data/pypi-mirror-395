#!/usr/bin/env python3
"""
File Parser CLI
Multimodal processing pipeline: processes PDFs (removes headers/footers, converts to markdown, generates image captions)
and audio files (diarization and transcription to markdown).
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
from file_parser.audio_parser import AudioExtractor, load_diarization_model, load_asr_model

# Model configuration
MODEL_PATH = "mlx-community/InternVL3-1B-4bit"
PROMPT = "Describe the image in detail. Extract important text from graphs, diagrams, or tables if they appear in the image, and be specific about it."

# Load the model once (lazy loading)
_model = None
_processor = None
_config = None

# Audio models (lazy loading)
_diar_model = None
_asr_model = None


def _load_vlm_model():
    """Lazy load the MLX VLM model to avoid loading it if not needed."""
    global _model, _processor, _config
    if _model is None:
        print("Loading MLX VLM model...")
        _model, _processor = load(MODEL_PATH, trust_remote_code=True)
        _config = load_config(MODEL_PATH)
        print("Model loaded successfully.")
    return _model, _processor, _config


def _load_audio_models(model_name="nvidia/parakeet-tdt-0.6b-v3", source_lang=None, target_lang=None, taskname=None):
    """Lazy load audio processing models (diarization and ASR)."""
    global _diar_model, _asr_model
    if _diar_model is None:
        print("Loading diarization model...")
        _diar_model = load_diarization_model()
        print("Diarization model loaded successfully.")
    if _asr_model is None:
        print(f"Loading ASR model ({model_name})...")
        _asr_model = load_asr_model(model_name)
        print("ASR model loaded successfully.")
    return _diar_model, _asr_model


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
    model, processor, config = _load_vlm_model()
    
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


def pipeline(input_dir, output_dir, audio_model="nvidia/parakeet-tdt-0.6b-v3", source_lang=None, target_lang=None, taskname=None):
    """
    Process PDF and audio files from input directory and output processed markdown files.
    
    Args:
        input_dir: Directory containing files to process
        output_dir: Directory to save processed markdown files
        audio_model: ASR model name (e.g., "nvidia/canary-1b-v2" or "nvidia/parakeet-tdt-0.6b-v3")
        source_lang: Source language for canary model
        target_lang: Target language for canary model
        taskname: Task name ("asr" or "ast") for canary model
    """
    # Normalize paths
    input_dir = os.path.abspath(input_dir)
    output_dir = os.path.abspath(output_dir)
    
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Detect file types
    pdf_ls = glob.glob(join(input_dir, "*.pdf"))
    audio_extensions = ['*.wav', '*.mp3', '*.m4a', '*.flac', '*.WAV', '*.MP3', '*.M4A', '*.FLAC']
    audio_ls = []
    for ext in audio_extensions:
        audio_ls.extend(glob.glob(join(input_dir, ext)))
    
    # # Copy other files to output directory (skip PDFs and audio files)
    # all_files = glob.glob(join(input_dir, "*.*"))
    # for p in all_files:
    #     is_pdf = p.endswith('.pdf')
    #     is_audio = any(p.lower().endswith(ext.replace('*', '')) for ext in audio_extensions)
    #     if not is_pdf and not is_audio:
    #         shutil.copyfile(p, join(output_dir, os.path.basename(p)))
    
    # Load audio models if we have audio files
    if audio_ls:
        _load_audio_models(audio_model, source_lang, target_lang, taskname)
    
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
    
    # Process audio files
    for audio_file in audio_ls:
        root, file_name = os.path.split(audio_file)
        print('# PROCESSING', file_name)
        
        base_name = os.path.splitext(file_name)[0]
        md_file = join(output_dir, base_name + '.md')
        
        if not Path(md_file).is_file():
            print('### Transcribing audio', md_file)
            audio_extractor = AudioExtractor(
                audio_path=Path(audio_file),
                output_path=Path(md_file),
                diar_model=_diar_model,
                asr_model=_asr_model,
                model_name=audio_model,
                source_lang=source_lang,
                target_lang=target_lang,
                taskname=taskname,
            )
            success = audio_extractor.run()
            if success:
                print('### Done!')
            else:
                print('### Failed to process audio file')
        else:
            print('### Skip transcribing audio (file already exists)')
    
    print(f'\n### All files processed. Output saved to: {output_dir}')


def main():
    """Main function to handle command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Process PDF and audio files: PDFs (remove headers/footers, convert to markdown, generate image captions), '
                    'Audio files (diarization and transcription to markdown).'
    )
    parser.add_argument(
        'input_dir',
        type=str,
        help='Input directory containing files to process'
    )
    parser.add_argument(
        'output_dir',
        type=str,
        help='Output directory for processed markdown files'
    )
    parser.add_argument(
        '--audio-model',
        type=str,
        default='nvidia/parakeet-tdt-0.6b-v3',
        help='ASR model name for audio processing (e.g., "nvidia/canary-1b-v2" or "nvidia/parakeet-tdt-0.6b-v3"). Default: nvidia/parakeet-tdt-0.6b-v3'
    )
    parser.add_argument(
        '--source-lang',
        type=str,
        default=None,
        help='Source language for canary model (only relevant when using canary models)'
    )
    parser.add_argument(
        '--target-lang',
        type=str,
        default=None,
        help='Target language for canary model (only relevant when using canary models)'
    )
    parser.add_argument(
        '--taskname',
        type=str,
        default=None,
        choices=['asr', 'ast'],
        help='Task name for canary model: "asr" or "ast" (only relevant when using canary models)'
    )
    
    args = parser.parse_args()
    
    # Validate input directory exists
    if not os.path.exists(args.input_dir):
        print(f"Error: Input directory does not exist: {args.input_dir}")
        return
    
    # Run the pipeline
    pipeline(
        args.input_dir,
        args.output_dir,
        audio_model=args.audio_model,
        source_lang=args.source_lang,
        target_lang=args.target_lang,
        taskname=args.taskname,
    )


if __name__ == "__main__":
    main()

