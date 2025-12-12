from setuptools import setup, find_packages
from pathlib import Path

# Read README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="maria_summarize_text_ai_assistant",
    version="0.1.6",  # Added python-dotenv support for .env files
    packages=find_packages(),
    install_requires=["groq", "python-dotenv"],  # Groq Python package and dotenv

    description="A simple AI-powered text summarization helper using Groq API.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Maria Jose",
)
