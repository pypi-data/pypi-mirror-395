# Directory Analyzer

Directory Analyzer is a simple Python tool that scans a directory recursively and generates a structured report.

## Features

- Count total number of files and folders.
- Group files by extension and calculate total size per extension.
- Find top 10 largest files in the directory tree.
- Detect duplicate files by comparing file content (hash).
- Handle file access errors safely (permission denied, missing files).
- Print report to console or save it to a file.

## Command line arguments

- `path` (required): path to the target directory.
- `--output` (optional): path to a file where the report will be saved.

## Requirements

- Python 3.8 or newer.
- Standard library only (os, hashlib, collections, argparse, etc.).