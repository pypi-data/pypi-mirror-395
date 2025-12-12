# Jupyter Switch

[![PyPI version](https://badge.fury.io/py/jupyter-switch.svg)](https://badge.fury.io/py/jupyter-switch)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful, lightweight and intuitive tool to seamlessly convert between Markdown (.md) and Jupyter Notebook (.ipynb) formats.

## ✨ Features

- 🚀 **Automatic detection**: Automatically detects whether the input file is `.md` or `.ipynb` and converts accordingly
- 🔄 **Bidirectional conversion**: Convert from Markdown to Jupyter Notebook and vice versa
- 🛡️ **Backup protection**: Automatically creates backups when output files already exist
- 📋 **Preserves structure**: Maintains code blocks, markdown content, and cell structure
- 🔧 **MCP integration**: Works as an MCP server tool for AI assistants

## 🤖 MCP Tool Usage (Recommended for AI Assistants)

This package provides an MCP (Model Context Protocol) server that can be used with AI assistants like Claude.

### Installation as MCP Server

Add to your MCP settings configuration:

```json
{
  "mcpServers": {
    "jupyter-switch": {
      "command": "uvx",
      "args": ["--from", "jupyter-switch", "jupyter-switch-mcp"]
    }
  }
}
```

### Available Tool

- **`switch_file`**: Converts between `.md` and `.ipynb` formats automatically based on input file extension

### Recommended Workflow for .ipynb Editing

1. **Convert to Markdown**: Use the `switch_file` tool to convert `.ipynb` → `.md` for easier editing
2. **Edit**: Modify the `.md` file with your preferred editor
3. **Convert back**: Use the tool again to convert `.md` → `.ipynb` when done

### Example

```
"Translate this notebook to French, using jupyter-switch"
```





## 📦 CLI Usage

### Installation

Install the package using pip:

```bash
pip install jupyter-switch
```

### Usage

The main command is `jupyter-switch`:

```bash
# Convert a Markdown file to Jupyter Notebook
jupyter-switch example.md

# Convert a Jupyter Notebook to Markdown
jupyter-switch example.ipynb
```

### Install with uv (Recommended) ⚡️

[`uvx`](https://docs.astral.sh/uv/concepts/tools/) will automatically install the package and run the command.

```bash
# Convert README.md to README.ipynb
uvx jupyter-switch README.md

# Convert notebook.ipynb to notebook.md
uvx jupyter-switch notebook.ipynb
```

The tool will automatically:
- Detect the input file format
- Generate the appropriate output filename
- Create a backup if the output file already exists
- Convert the content while preserving structure

### Help 🆘

```bash
jupyter-switch --help
jupyter-switch --version
```

## Conversion Details 🔄

### Markdown to Jupyter Notebook
- Python code blocks (```python...```) become code cells
- All other content becomes markdown cells
- Adds appropriate notebook metadata and structure

### Jupyter Notebook to Markdown  
- Code cells become Python code blocks
- Markdown cells are preserved as-is
- Cell outputs are ignored during conversion

## Requirements 🐍

- Python >= 3.10

## License 📄

MIT License
