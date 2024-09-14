import os
import argparse

def create_project_structure(directory):
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
        for file in files:
            structure.append(f"{subindent}├── {file}")
    return '\n'.join(structure)

def read_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def create_markdown_content(directory):
    content = [create_project_structure(directory), ""]
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, directory)
            content.append(f"\n# {relative_path}")
            content.append("```")
            content.append(read_file_content(file_path))
            content.append("```")
    
    return '\n'.join(content)

def main():
    parser = argparse.ArgumentParser(description="Create a structured Markdown file from a directory.")
    parser.add_argument("directory", help="Path to the directory to process")
    parser.add_argument("output", help="Path for the output Markdown file")
    args = parser.parse_args()

    markdown_content = create_markdown_content(args.directory)
    
    with open(args.output, 'w', encoding='utf-8') as output_file:
        output_file.write(markdown_content)
    
    print(f"Markdown file created successfully: {args.output}")

if __name__ == "__main__":
    main()