# Markdown Extract

A Simple Python library to parse Markdown files from headers.

[![PyPI Latest Release](https://img.shields.io/pypi/v/markdown-extract.svg)](https://pypi.org/project/markdown-extract/)

## Installation

Install via pip:

```bash
pip install markdown-extract
```

## Usage

```python
from markdown_extract import MarkdownExtractor

markdown_content = """
# Section 1
Some content here.

## Subsection 1.1
More details.
"""

extractor = MarkdownExtractor(markdown_content)

# 1. Access sections using dictionary-style brackets
print(extractor["Section 1"])
# Output:
# # Section 1
# Some content here.
# ...

# 2. Access nested sections
print(extractor["Section 1"]["Subsection 1.1"])
# Output:
# ## Subsection 1.1
# More details.

# 3. List child headers
print(extractor.list())
# Output: ['Section 1']

print(extractor["Section 1"].list())
# Output: ['Subsection 1.1']

# 4. Access the full document (root)
print(extractor[""])
```

## Features

- **Nested Parsing**: Correctly parses Markdown headers into a nested structure.
- **Robust Extraction**: Ignores "headers" that are actually inside:
    - Code blocks (` ``` `)
    - Tables
    - Math blocks (`$$`)
    - YAML front matter (`---`)
- **Indentation Support**: Handles indented headers correctly.
- **Easy Access**: Use bracket notation (`extractor["Header"]`) or `.get_section()` method.
- **Discovery**: Use `.list()` to see available child headers at any level.

## Development

To run the tests:

```bash
python tests/run_tests.py
```
