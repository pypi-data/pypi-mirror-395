# ACS Chatbot Library

`acs_chatbot` is a Python library designed to assist with common AI tasks using Google's Gemini API.

## Installation

You can install the library locally:

```bash
pip install .
```

## Setup

You need a Google Gemini API key. You can set it as an environment variable:

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

**Linux/macOS:**
```bash
export GEMINI_API_KEY="your_api_key_here"
```

Or you can pass it directly in your code using `configure_api_key`.

## Usage

```python
from acs_chatbot import get_response, summarize_text, format_response, configure_api_key

# Optional: Configure API key if not in env vars
# configure_api_key("your_api_key_here")

# Get a response
response = get_response("Hello, AI!")
print(response)

# Summarize text
summary = summarize_text("Long text here...")
print(summary)

# Format response
formatted = format_response(response)
print(formatted)
```
