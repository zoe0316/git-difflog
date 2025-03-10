#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Allen
# @date  : 2025-03-10 09:21


from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="git-difflog",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A git extension to save diff outputs with timestamps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zoe0316/git-difflog",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "git-difflog=gitdifflog.__main__:main",
        ],
    },
)
