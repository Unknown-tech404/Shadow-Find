#!/usr/bin/env python3
"""
Setup script for SHADOW FIND - Universal Link Extractor
"""

from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="shadow-find",
    version="2.1.0",
    author="Unknown-tech404",
    author_email="",
    description="Universal Link Extractor - Extract All Links & URLs from Any Website",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/unknown-tech404/shadow-find",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Topic :: Security",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
        "beautifulsoup4>=4.9.0",
        "colorama>=0.4.4",
    ],
    entry_points={
        "console_scripts": [
            "shadow-find=shadow_find:main",
        ],
    },
    keywords=[
        "web-scraping",
        "link-extractor",
        "url-extractor",
        "security",
        "reconnaissance",
        "osint",
        "web-crawler",
    ],
)
