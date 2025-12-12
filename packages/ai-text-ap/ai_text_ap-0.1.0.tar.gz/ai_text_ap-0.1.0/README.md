# ai_text_ap

A simple Python library created by a student to interact with AI text models.

## Functions included
- get_response(prompt)
- summarize_text(text)
- format_response(text)

---

## Installation (after uploading to PyPI)
```bash
pip install ai_text_ap
```

## If you haven't uploaded to PyPI yet, you can install locally while testing:

```bash
pip install .
```

---

## Set Your API Key
This library expects an environment variable called **OPENAI_API_KEY**.

### Windows (CMD)
```bash
set OPENAI_API_KEY=your_api_key_here
```

### Windows (PowerShell)
```bash
$env:OPENAI_API_KEY="your_api_key_here"
```

---

## Usage Example

```python
from ai_text_ap import get_response, summarize_text

print(get_response("Write a poem about trees."))
print(summarize_text("Very long essay text here..."))
"""
print(summarize_text(long_text))
```
---

