import json
import re
import sys
import uuid
import os
import shutil
import argparse


def md_to_ipynb(md_file_path, ipynb_file_path):
    """
    Convert a Markdown file to Jupyter Notebook format

    Args:
        md_file_path: Path to the input markdown file
        ipynb_file_path: Path to the output ipynb file
    """
    # Read the markdown file
    with open(md_file_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Initialize the notebook structure
    notebook = {
        "cells": [],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (ipykernel)",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.11.9",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }

    # Pattern to match Python code blocks
    code_block_pattern = r"```python\n(.*?)```"

    # Split content by code blocks
    parts = re.split(code_block_pattern, md_content, flags=re.DOTALL)

    for i, part in enumerate(parts):
        part = part.strip()
        if not part:
            continue

        # Code cells (odd indices after splitting by code block pattern)
        if i % 2 == 1:
            cell = {
                "cell_type": "code",
                "execution_count": None,
                "id": str(uuid.uuid4()),
                "metadata": {},
                "outputs": [],
                "source": [part],
            }
            notebook["cells"].append(cell)

        # Markdown cells (even indices including 0)
        else:
            # Split by newlines and make each line a separate string in the source list
            markdown_lines = part.split("\n")
            cell = {
                "cell_type": "markdown",
                "id": str(uuid.uuid4()),
                "metadata": {},
                "source": markdown_lines,
            }
            notebook["cells"].append(cell)

    # Write the notebook to a file
    with open(ipynb_file_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=1)

    return f"Successfully converted {md_file_path} to {ipynb_file_path}"


def ipynb_to_md(input_file, output_file):
    """
    Convert a Jupyter notebook (.ipynb in JSON format) to a Markdown file.

    Args:
        input_file: Path to the input .ipynb file
        output_file: Path to the output .md file
    """
    # Read the JSON file
    with open(input_file, "r", encoding="utf-8") as f:
        notebook = json.load(f)

    # Process cells and convert to markdown
    markdown_content = ""

    for cell in notebook["cells"]:
        cell_type = cell["cell_type"]

        # Get the source content (handling both string and list formats)
        source = cell["source"]
        if isinstance(source, list):
            source = "".join(source)

        # Process based on cell type
        if cell_type == "markdown":
            # For markdown cells, add content directly
            markdown_content += source + "\n\n"

        elif cell_type == "code":
            # For code cells, wrap content in Python code block, ignore outputs
            markdown_content += f"```python\n{source}\n```\n\n"

    # Write the markdown content to output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    return f"Successfully converted {input_file} to {output_file}"


def backup_file(file_path):
    """
    Create a backup of a file by appending .bak to its name

    Args:
        file_path: Path to the file to backup
    """
    backup_path = f"{file_path}.bak"
    shutil.copy2(file_path, backup_path)
    return f"Created backup at {backup_path}"


def detect_file_type(file_path):
    """
    Detect the file type based on extension

    Args:
        file_path: Path to the file

    Returns:
        str: 'md' or 'ipynb'
    """
    if file_path.lower().endswith(".md"):
        return "md"
    elif file_path.lower().endswith(".ipynb"):
        return "ipynb"
    else:
        raise ValueError(f"Unsupported file type: {file_path}")


def convert_file(input_file):
    """
    Convert a file between markdown and notebook formats
    
    Recommended workflow for editing .ipynb files:
    1. First, use this tool to convert .ipynb to .md for easier editing
    2. Edit the .md file with your preferred text editor  
    3. After completing all edits, use this tool again to convert .md back to .ipynb

    Args:
        input_file: Path to the input file
    """
    # Detect file type
    file_type = detect_file_type(input_file)

    # Determine output file path
    if file_type == "md":
        output_file = input_file.replace(".md", ".ipynb")
        if not output_file.endswith(".ipynb"):  # Handle case sensitivity
            output_file = input_file[:-3] + ".ipynb"
    else:  # ipynb
        output_file = input_file.replace(".ipynb", ".md")
        if not output_file.endswith(".md"):  # Handle case sensitivity
            output_file = input_file[:-6] + ".md"

    # Check if output file exists and backup if needed
    if os.path.exists(output_file):
        message = backup_file(output_file)
        print(message)

    # Perform conversion
    if file_type == "md":
        result = md_to_ipynb(input_file, output_file)
    else:  # ipynb
        result = ipynb_to_md(input_file, output_file)

    return result


def main():
    """
    Main CLI function for jupyter-switch command
    """
    parser = argparse.ArgumentParser(
        description="Convert between Markdown (.md) and Jupyter Notebook (.ipynb) formats. "
                   "Recommended workflow: Convert .ipynb to .md for easier editing, then convert back to .ipynb when done.",
        prog="jupyter-switch",
    )

    parser.add_argument(
        "file",
        help="Input file path (.md or .ipynb). The script will automatically detect the file type and convert accordingly.",
    )

    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")

    args = parser.parse_args()

    try:
        # Check if file exists
        if not os.path.exists(args.file):
            print(f"Error: File '{args.file}' not found.")
            sys.exit(1)

        result = convert_file(args.file)
        print(result)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
