#!/usr/bin/env python3

from setuptools import setup, find_packages
import os

# Read version from _version.py
version_file = os.path.join(os.path.dirname(__file__), 'src', '_version.py')
with open(version_file) as f:
    exec(f.read())

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="samaya",
    version=__version__,
    author="Surya Waters",
    author_email="surya.waters.1@proton.me",
    description="A minimal pomodoro CLI timer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/suryawaters/samaya",
    packages=find_packages(),
    package_data={
        "src": ["*.mp3", "*.m4a"],
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "samaya=src.cli:main",
        ],
    },
    install_requires=[
        # No external dependencies required
    ],
    extras_require={
        "dev": [
            "pytest",
            "black",
            "flake8",
        ],
    },
)