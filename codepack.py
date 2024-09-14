#!/usr/bin/env python3
"""
CodePack: A tool to pack a directory of code files into a single Markdown file.

This script traverses a given directory, creates a visual representation of its
structure, and combines the content of all files into a single Markdown document.
It's useful for code sharing and documentation purposes.
"""

import os
import argparse
from pathlib import Path
import fnmatch

DEFAULT_IGNORE_PATTERNS = [
    '.git', '.git/**',  # Ignore the entire .git directory and its contents
    '.gitignore', '.gitattributes',
    '.vscode/', '.idea/', '*.swp', '*.swo', '*~',
    '__pycache__/', '*.pyc',
    'venv/', 'env/', '.env',
    '.DS_Store', 'Thumbs.db',
    'build/', 'dist/',
    'node_modules/',
    '*.log',
    '*.bak', '*.tmp'
]

def load_ignore_patterns(directory):
    """
    Load ignore patterns from .gitignore or .codepackignore file.

    Args:
        directory (Path): The directory to search for ignore files.

    Returns:
        list: List of ignore patterns.
    """
    gitignore = directory / '.gitignore'
    codepackignore = directory / '.codepackignore'

    if gitignore.exists():
        with open(gitignore, 'r') as f:
            patterns = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    elif codepackignore.exists():
        with open(codepackignore, 'r') as f:
            patterns = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    else:
        patterns = DEFAULT_IGNORE_PATTERNS

    return patterns

def should_ignore(path, ignore_patterns, base_dir):
    """
    Check if a path should be ignored based on ignore patterns.

    Args:
        path (str): The path to check.
        ignore_patterns (list): List of ignore patterns.
        base_dir (str): The base directory for relative path calculation.

    Returns:
        bool: True if the path should be ignored, False otherwise.
    """
    rel_path = os.path.relpath(path, base_dir)
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
            return True
    return False

def is_binary_file(file_path):
    """
    Check if a file is binary.

    Args:
        file_path (str): The path to the file.

    Returns:
        bool: True if the file is binary, False otherwise.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file.read(1024)
        return False
    except UnicodeDecodeError:
        return True

def create_project_structure(directory, ignore_patterns):
    """
    Generate a visual representation of the project structure.

    Args:
        directory (Path): The path to the directory to process.
        ignore_patterns (list): List of ignore patterns.

    Returns:
        str: A string representation of the project structure.
    """
    structure = []
    for root, dirs, files in os.walk(directory):
        rel_root = os.path.relpath(root, directory)
        if should_ignore(rel_root, ignore_patterns, directory):
            continue

        level = len(Path(rel_root).parts)
        indent = '    ' * level
        folder = os.path.basename(root)
        
        if level == 0:
            structure.append(f"# Project Structure\n/{folder}")
        else:
            structure.append(f"{indent[:-4]}└── {folder}")
        
        subindent = '    ' * (level + 1)
        for file in sorted(files):
            file_path = os.path.join(root, file)
            if not should_ignore(file_path, ignore_patterns, directory) and not is_binary_file(file_path):
                structure.append(f"{subindent}├── {file}")
    
    return '\n'.join(structure)

def read_file_content(file_path):
    """
    Read and return the content of a file.

    Args:
        file_path (Path): The path to the file to read.

    Returns:
        str: The content of the file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def get_file_extension(file_path):
    """
    Get the file extension, defaulting to 'txt' if not present.

    Args:
        file_path (Path): The path to the file.

    Returns:
        str: The file extension without the dot, or 'txt' if no extension.
    """
    return file_path.suffix[1:] if file_path.suffix else 'txt'

def create_markdown_content(directory, ignore_patterns):
    """
    Create the full Markdown content including structure and file contents.

    Args:
        directory (Path): The path to the directory to process.
        ignore_patterns (list): List of ignore patterns.

    Returns:
        str: The complete Markdown content.
    """
    content = [create_project_structure(directory, ignore_patterns), ""]
    
    for root, _, files in os.walk(directory):
        rel_root = os.path.relpath(root, directory)
        if should_ignore(rel_root, ignore_patterns, directory):
            continue
        for file in sorted(files):
            file_path = os.path.join(root, file)
            if should_ignore(file_path, ignore_patterns, directory) or is_binary_file(file_path):
                continue
            relative_path = os.path.relpath(file_path, directory)
            extension = get_file_extension(Path(file_path))
            
            content.extend([
                f"\n# {relative_path}",
                f"```{extension}",
                read_file_content(file_path),
                "```"
            ])
    
    return '\n'.join(content)

def main():
    """
    Main function to run the script.

    Parses command-line arguments, processes the specified directory,
    and writes the output to a Markdown file.
    """
    parser = argparse.ArgumentParser(description="Pack a directory of code files into a single Markdown file.")
    parser.add_argument("directory", nargs='?', default='.', help="Path to the directory to process (default: current directory)")
    parser.add_argument("-o", "--output", help="Path for the output Markdown file (default: {directory_name}.md in the current directory)")
    args = parser.parse_args()

    directory = Path(args.directory).expanduser().resolve()
    if not directory.is_dir():
        print(f"Error: {directory} is not a valid directory.")
        return

    ignore_patterns = load_ignore_patterns(directory)

    if args.output:
        output_path = Path(args.output).expanduser().resolve()
    else:
        output_path = Path(f"{directory.name}.md")

    markdown_content = create_markdown_content(directory, ignore_patterns)
    
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(markdown_content)
    
    print(f"Markdown file created successfully: {output_path}")

if __name__ == "__main__":
    main()