"""
Setup configuration for the upserver package.
This file is maintained for compatibility with older build systems.
For modern installations, prefer using pyproject.toml.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="upserver",
    version="0.1.0",
    author="Álex Vieira",
    description="A file server for uploading and downloading files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eiAlex/upserver",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "upserver=upserver.cli:main",
        ],
    },
    keywords="file server upload download file management",
    project_urls={
        "Bug Tracker": "https://github.com/eiAlex/upserver/issues",
        "Source Code": "https://github.com/eiAlex/upserver",
    },
)
