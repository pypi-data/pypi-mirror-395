# ai_helpers

A helper library for building AI-powered applications in Python.

## Features
- Send prompt to AI model and get responses.
- Summarize long text.
- Clean and format AI responses.

## Example Usage

```python
from ai_helpers import get_response, summarize_text

API_KEY = "YOUR_API_KEY"

reply = get_response("Hello, how are you?", API_KEY)
print(reply)
