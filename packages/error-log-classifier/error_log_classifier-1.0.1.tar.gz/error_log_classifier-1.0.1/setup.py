#!/usr/bin/env python3
"""Setup script for Error Log Classifier package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="error-log-classifier",
    version="1.0.1",
    author="Preetham Ghorpade & Harish R S",
    author_email="contact@example.com",
    description="Intelligent error log clustering and analysis tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/preetham3127/Error-log-classifier",
    project_urls={
        "Bug Tracker": "https://github.com/preetham3127/Error-log-classifier/issues",
        "Documentation": "https://github.com/preetham3127/Error-log-classifier/docs",
        "Source Code": "https://github.com/preetham3127/Error-log-classifier",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Logging",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "error-log-classifier=main:main",
        ],
    },
    keywords="error logs clustering analysis signature extraction patterns",
    include_package_data=True,
    zip_safe=False,
)
