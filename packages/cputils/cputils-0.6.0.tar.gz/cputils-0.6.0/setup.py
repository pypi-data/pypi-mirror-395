#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script"""

from setuptools import setup, find_packages
import os

# Get the long description from the README file
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md")) as f:
    long_description = f.read()

setup(
    author="Dih5",
    author_email="dihedralfive@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        # 'Intended Audience :: Science/Research',
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    description="Utilities for Competitive Programming",
    entry_points={
        "console_scripts": [
            "cpconfig=cputils.config:main",
            "cpsamples=cputils.samples:main",
            "cptest=cputils.testing:main",
            "cpsubmit=cputils.submit:main",
            "cpmenu=cputils.menu:main",
        ],
    },
    extras_require={
        "docs": ["sphinx", "nbsphinx", "sphinx-rtd-theme", "IPython"],
        "test": ["pytest"],
    },
    keywords=[],
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="cputils",
    packages=find_packages(include=["cputils", "cputils.*"], exclude=["demos", "tests", "docs"]),
    install_requires=[
        "yaconfig",
        "requests",
        "beautifulsoup4",
        "lxml",
    ],
    url="https://github.com/Dih5/cputils",
    version='0.6.0',
)
