# AI Helper Library

This is a custom Python library designed to interact with the Anti Gravity AI tool.

## Installation

```bash
pip install ai_helper_lib
```

## Usage

```python
from ai_helper_lib import ask_antigravity, summarize_text

response = ask_antigravity("What is the future of AI?")
print(response)

summary = summarize_text("This is a very long text that needs to be shortened for better readability.")
print(summary)
```

## Features

- **ask_antigravity**: Sends a prompt to the AI and gets a response.
- **summarize_text**: Truncates long text.
- **format_text**: Cleans up whitespace.
