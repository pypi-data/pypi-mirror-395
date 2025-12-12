# multimodal-parsers

PDF processing pipeline: removes headers/footers, converts to markdown, and generates image captions using MLX VLM.

## Installation

```bash
pip install multimodal-parsers
```

## Dependencies

The package automatically installs:
- Pillow
- mlx-vlm
- pymupdf
- scikit-learn
- numpy
- marker-pdf

Additionally, you may need to install:
```bash
pip install "unstructured[pdf]"
```

## Usage

After installation, use the `multimodal-parsers` command:

```bash
multimodal-parsers <input_dir> <output_dir>
```

### Example

```bash
multimodal-parsers Database/Private/Files Database/Private/Files/output
```

## What it does

1. **Removes headers and footers** from PDF files using clustering algorithms
2. **Converts PDFs to markdown** using marker-pdf
3. **Generates image captions** using MLX VLM (InternVL3-1B-4bit)
4. **Outputs final markdown files** with captioned images

## Development

```bash
git clone https://github.com/thuuyen98/PIER-QA
cd PIER-QA
pip install -e ".[dev]"
```

## License

MIT License
