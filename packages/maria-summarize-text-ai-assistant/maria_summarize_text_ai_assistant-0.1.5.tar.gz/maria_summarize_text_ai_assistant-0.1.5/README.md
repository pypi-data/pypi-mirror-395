# maria_summarize_text_ai_assistant

A simple Python library to summarize long text using an AI API (Groq).

## Features
- AI-powered text summarization  
- Clean API design  
- Docstrings included  
- Easy to use in Flask or any Python app  

---

## Installation

After uploading to PyPI:

```bash
pip install maria_summarize_text_ai_assistant
pip install groq python-dotenv
```

## Usage

```python
import os
from maria_summarize_text_ai_assistant import summarize_text

# Set your API key in environment
os.environ["GROQ_API_KEY"] = "YOUR_GROQ_API_KEY"

long_text = "Artificial intelligence is transforming industries..."
summary = summarize_text(long_text)
print(summary)
```

## Next Steps

Update `setup.py` version number.

Rebuild your package:
```bash
python setup.py sdist bdist_wheel
```

Upload to PyPI:
```bash
python -m twine upload dist/*
```

In your Flask app, just set the `GROQ_API_KEY` environment variable — your code will work seamlessly.