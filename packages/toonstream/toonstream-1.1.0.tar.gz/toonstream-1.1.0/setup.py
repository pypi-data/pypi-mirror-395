"""
Setup script for toonstream package.

Installation:
    pip install -e .  # Development install
    pip install .     # Regular install
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="toonstream",
    version="1.1.0",
    author="Vivek Pandian",
    author_email="vivekpandian08@gmail.com",
    description="Token Oriented Object Notation - Efficient data serialization for LLMs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vivekpandian08/toonstream",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies for core functionality
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
        "test": [
            "tiktoken>=0.5.0",  # For token comparison tests
        ],
    },
    entry_points={
        "console_scripts": [
            # Add CLI tools here if needed
        ],
    },
    keywords="toon json serialization tokens llm optimization csv tabular",
    project_urls={
        "Bug Reports": "https://github.com/vivekpandian08/toonstream/issues",
        "Source": "https://github.com/vivekpandian08/toonstream",
        "Documentation": "https://github.com/vivekpandian08/toonstream#readme",
    },
)
