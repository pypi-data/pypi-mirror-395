from setuptools import setup, find_packages

setup(
    name="maria_summarize_text_ai_assistant",
    version="0.1.0",
    description="A simple AI-powered text summarization library",
    packages=find_packages(),
    install_requires=["openai"],
    author="Maria Jose",
    python_requires=">=3.8",
)