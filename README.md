# CodePack

CodePack is a simple yet powerful Python tool that packs a directory of code files into a single, well-structured Markdown file. It's perfect for developers who need to share their codebase in a readable format, or for those who want to prepare their code for analysis by AI language models like GPT.

## Features

- Automatically traverses and captures the structure of your project directory
- Creates a visual representation of your project's file structure
- Includes the full content of each file in the output
- Supports all text-based file types
- Generates a single Markdown file for easy sharing and viewing
- Preserves file extensions for proper syntax highlighting in Markdown

## Installation

1. Ensure you have Python 3.6 or later installed on your system.
2. Download the `codepack.py` script to your local machine.

No additional dependencies are required!

## Usage

Run CodePack from the command line with the following syntax:

```
python codepack.py <input_directory> <output_file>
```

For example:

```
python codepack.py /path/to/your/project /path/to/output/project_structure.md
```

This will create a Markdown file named `project_structure.md` in the specified output location, containing the structure and content of all files in the input directory.

## Example Output

The generated Markdown file will have a structure similar to this:

```markdown
# Project Structure
/YourProject
    ├── file1.py
    ├── file2.js
    └── subdirectory
        ├── file3.html
        └── file4.css

# file1.py

Content of file1.py

# file2.js

Content of file2.js

# subdirectory/file3.html

Content of file3.html

# subdirectory/file4.css
​
Content of file4.css

```

## Contributing

Contributions to CodePack are welcome! Here are some ways you can contribute:

1. Report bugs or suggest features by opening an issue.
2. Improve documentation for the project.
3. Submit pull requests with bug fixes or new features.

Please ensure that your code adheres to the existing style of the project to maintain consistency.

## License

You can use it for free, but I haven't decided which protocol yet and neet to learn the difference.
See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to all contributors who have helped to improve this tool.
- Inspired by the need for an easy way to share code structures with AI language models and fellow developers.

## Contact

If you have any questions or feedback, please open an issue on the GitHub repository.

Happy coding!
