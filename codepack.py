#!/usr/bin/env python3
"""
CodePack: A tool to pack a directory of code files into a single Markdown file.

This script traverses a given directory, creates a visual representation of its
structure, and combines the content of all files into a single Markdown document.
It's useful for code sharing and documentation purposes.
"""

import os
import argparse

def create_project_structure(directory):
    """
    Generate a visual representation of the project structure.

    Args:
        directory (str): The path to the directory to process.

    Returns:
        str: A string representation of the project structure.
    """
    structure = []
    for root, dirs, files in os.walk(directory):
        level = root.replace(directory, '').count(os.sep)
        indent = '    ' * level
        folder = os.path.basename(root)
        
        if level == 0:
            structure.append(f"# Project Structure\n/{folder}")
        else:
            structure.append(f"{indent[:-4]}└── {folder}")
        
        subindent = '    ' * (level + 1)
        for file in sorted(files):  # Sort files for consistent output
            structure.append(f"{subindent}├── {file}")
    
    return '\n'.join(structure)

def read_file_content(file_path):
    """
    Read and return the content of a file.

    Args:
        file_path (str): The path to the file to read.

    Returns:
        str: The content of the file, or a placeholder for binary files.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        # Return a placeholder for binary files
        return f"[Binary file: {os.path.basename(file_path)}]"

def get_file_extension(file_path):
    """
    Get the file extension, defaulting to 'txt' if not present.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The file extension without the dot, or 'txt' if no extension.
    """
    _, ext = os.path.splitext(file_path)
    return ext[1:] if ext else 'txt'

def create_markdown_content(directory):
    """
    Create the full Markdown content including structure and file contents.

    Args:
        directory (str): The path to the directory to process.

    Returns:
        str: The complete Markdown content.
    """
    content = [create_project_structure(directory), ""]
    
    for root, _, files in os.walk(directory):
        for file in sorted(files):  # Sort files for consistent output
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, directory)
            extension = get_file_extension(file_path)
            
            # Add file content to the Markdown
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
    parser.add_argument("directory", help="Path to the directory to process")
    parser.add_argument("output", help="Path for the output Markdown file")
    args = parser.parse_args()

    markdown_content = create_markdown_content(args.directory)
    
    with open(args.output, 'w', encoding='utf-8') as output_file:
        output_file.write(markdown_content)
    
    print(f"Markdown file created successfully: {args.output}")

if __name__ == "__main__":
    main()