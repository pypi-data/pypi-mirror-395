# maria_summarize_text_ai_assistant

A simple Python library to summarize long text using an AI API (Groq).

## Features
- AI-powered text summarization  
- Clean API design  
- Docstrings included  
- Easy to use in Flask or any Python app  
- Automatic `.env` file support for API key configuration

---

## Installation

```bash
pip install maria_summarize_text_ai_assistant
```

The package automatically installs `groq` and `python-dotenv` dependencies.

---

## Usage

### Method 1: Using .env file (Recommended)

1. Create a `.env` file in your project directory:
```
GROQ_API_KEY=your_actual_groq_api_key_here
```

2. Use the library in your code:
```python
from maria_summarize_text_ai_assistant import summarize_text

long_text = "Artificial intelligence is transforming industries..."
summary = summarize_text(long_text)
print(summary)
```

### Method 2: Set environment variable manually

```python
import os
from maria_summarize_text_ai_assistant import summarize_text

# Set your API key in environment
os.environ["GROQ_API_KEY"] = "YOUR_GROQ_API_KEY"

long_text = "Artificial intelligence is transforming industries..."
summary = summarize_text(long_text)
print(summary)
```

---

## Publishing Updates

Update `setup.py` version number, then rebuild your package:
```bash
python setup.py sdist bdist_wheel
```

Upload to PyPI:
```bash
python -m twine upload dist/*
```