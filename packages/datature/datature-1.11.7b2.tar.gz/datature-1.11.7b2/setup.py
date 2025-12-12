#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   setup.py
@Author  :   Raighne.Weng
@Contact :   developers@datature.io
@License :   Apache License 2.0
@Desc    :   Setup module
"""

import re

import setuptools

# read the contents of your README file
with open("README.md", "r", encoding="utf8") as rd:
    long_description = rd.read()

# read the version number
with open("datature/nexus/version.py", "r", encoding="utf8") as rd:
    version = re.search(r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]', rd.read()).group(1)

REQUIRES = []
with open("requirements.txt", "r", encoding="utf8") as f:
    for line in f:
        line, _, _ = line.partition("#")
        line = line.strip()
        if not line or line.startswith("setuptools"):
            continue
        REQUIRES.append(line)

setuptools.setup(
    name="datature",
    version=version,
    author="Datature",
    license="Apache License 2.0",
    author_email="developers@datature.io",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://datature.io/",
    project_urls={
        "Homepage": "https://datature.io/",
        "Documentation": "https://developers.datature.io/docs/python-sdk",
        "Download": "https://pypi.org/project/datature#files",
        "Changelog": "https://developers.datature.io/docs/sdk-changelog",
        "Slack Community": "https://datature.io/community",
    },
    description="Python bindings for the Datature API",
    packages=setuptools.find_namespace_packages(),
    python_requires=">=3.8",
    install_requires=REQUIRES,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: Apache Software License",
    ],
    entry_points={
        "console_scripts": ["datature=datature.nexus.cli.main:main"],
    },
)
