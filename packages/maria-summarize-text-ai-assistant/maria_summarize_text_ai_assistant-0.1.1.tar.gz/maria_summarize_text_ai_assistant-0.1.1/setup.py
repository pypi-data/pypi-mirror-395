from setuptools import setup, find_packages
from pathlib import Path

# Read README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="maria_summarize_text_ai_assistant",
    version="0.1.1",
    packages=find_packages(),
    install_requires=["openai"],
    
    description="A simple AI-based text summarization helper.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Maria Jose",
)
