# AI Assist Utils

A simple Python library to help with common AI tasks like getting responses from LLMs, summarizing text, and formatting outputs.

## Installation

You can install this package locally:

```bash
pip install .
```

## Usage

### Setup

You need an OpenAI API key to use the AI features. You can set it as an environment variable `OPENAI_API_KEY` or pass it directly to the functions.

### Examples

```python
from ai_assist_utils import get_response, summarize_text, format_response

# 1. Get a response from AI
prompt = "What is the capital of France?"
response = get_response(prompt)
print(response)

# 2. Summarize text
long_text = "..." # Your long text here
summary = summarize_text(long_text)
print(summary)

# 3. Format response
raw_text = "  Some text with extra spaces.  "
formatted = format_response(raw_text)
print(f"'{formatted}'")
```

## Functions

- `get_response(prompt, api_key=None, model="gpt-3.5-turbo")`: Sends a prompt to OpenAI.
- `summarize_text(text, api_key=None)`: Summarizes the given text.
- `format_response(text)`: Cleans up the text output.

## Testing

Run unit tests with:

```bash
python -m unittest discover tests
```
