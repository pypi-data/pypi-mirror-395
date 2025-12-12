#!/usr/bin/env python3
"""
Setup configuration for arbitbot package
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="arbitbot",
    version="0.1.0",
    author="Hung-Ching-Lee",
    description="Multi-exchange cryptocurrency arbitrage detection tool using CCXT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hung-Ching-Lee/Arbitbot",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    python_requires=">=3.8",
    install_requires=[
        "ccxt>=1.80.0",
        "requests>=2.28.0",
        "pandas>=1.5.0",
        "ipywidgets>=8.0.0",
    ],
)
