#!/usr/bin/env python3
"""Setup script for SDI Python SDK"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="sdi-python",
    version="1.0.0",
    description="Synthetic Digital Immunity SDK for Python - AI-powered cybersecurity for microservices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="SDI Team",
    author_email="sdi@example.com",
    url="https://github.com/skesani/sdi",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.28.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="sdi cybersecurity anomaly-detection microservices security ai",
    project_urls={
        "Documentation": "https://github.com/skesani/sdi",
        "Source": "https://github.com/skesani/sdi",
        "Tracker": "https://github.com/skesani/sdi/issues",
    },
)

