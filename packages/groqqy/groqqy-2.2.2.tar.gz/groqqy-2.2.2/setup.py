"""
Groqqy - Simple general-purpose AI assistant powered by Groq
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="groqqy",
    version="2.1.0",
    author="Scott Sennewald",
    description="Clean, composable micro agentic bot - Teaching kernel for agentic AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scottsen/groqqy",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "loguru>=0.7.0",
    ],
    entry_points={
        "console_scripts": [
            "groqqy=groqqy.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
