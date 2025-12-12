"""
Setup script for gradioSearch package
Created with assistance from aider.chat
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file for long description
readme_file = Path(__file__).parent / "README.md"
long_description = (
    readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""
)

setup(
    name="gradioSearch",
    version="0.2.1",
    description="A CLI tool for searching FAISS vector databases with Gradio GUI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="thiswillbeyourgithub",
    url="https://github.com/thiswillbeyourgithub/gradioSearcher",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "gradio==5.50.0",
        "pandas==2.3.3",
        "langchain-community==0.4.1",
        "sentence-transformers==5.1.2",
        "tqdm>=4.67.1",
        "beartype>=0.22.6",
        "faiss-cpu>=1.13.1"
    ],
    entry_points={
        "console_scripts": [
            "gradioSearch=gradioSearch.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
