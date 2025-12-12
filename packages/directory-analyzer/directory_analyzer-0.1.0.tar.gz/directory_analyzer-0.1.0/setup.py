from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="directory_analyzer",
    version="0.1.0",
    packages=find_packages(),
    author="Volodymyr",
    author_email="vova.dzimina@gmail.com",
    description="Recursive directory analyzer with stats, top files and duplicate detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
)