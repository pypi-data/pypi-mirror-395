from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="multimodal-parsers",
    version="0.1.1",
    author="Uyen Hoang",
    author_email="thho00003@stud.uni-saarland.de",
    description="PDF processing pipeline: remove headers/footers, convert to markdown, and generate image captions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thuuyen98/PIER-QA",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Pillow>=10.0.0",
        "mlx-vlm>=0.3.0",
        "pymupdf>=1.23.0",
        "scikit-learn>=1.0.0",
        "numpy>=1.20.0",
        "marker-pdf>=0.2.14",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "multimodal-parsers=file_parser.cli:main",
        ],
    },
    include_package_data=True,
)

