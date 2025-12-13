"""
Setup script for CognitiveAI Python SDK
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# Read version from package
def get_version():
    version_file = os.path.join(this_directory, "cognitiveai", "__init__.py")
    with open(version_file, "r") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"')
    raise RuntimeError("Unable to find version string.")

setup(
    name="cognitiveai-sdk",
    version=get_version(),
    author="CognitiveAI Team",
    author_email="team@cognitiveai.ai",
    description="Python SDK for CognitiveAI API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cognitiveai/cognitiveai-python-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="cognitiveai reasoning ai llm api sdk",
    python_requires=">=3.8",
    install_requires=[
        "aiohttp>=3.8.0",
        "pydantic>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "isort>=5.10.0",
            "mypy>=1.0.0",
            "flake8>=4.0.0",
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.2.0",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/cognitiveai/cognitiveai-python-sdk/issues",
        "Source": "https://github.com/cognitiveai/cognitiveai-python-sdk",
        "Documentation": "https://docs.cognitiveai.ai/python-sdk",
    },
)
