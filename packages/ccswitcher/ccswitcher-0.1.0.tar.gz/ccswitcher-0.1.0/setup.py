"""Setup script for CCswitcher."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ccswitcher",
    version="0.1.0",
    author="CCswitcher Contributors",
    description="CLI tool to switch between different Claude Code API settings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ccswitcher",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "click>=8.0.0",
        "pyyaml>=5.0.0",
    ],
    entry_points={
        "console_scripts": [
            "ccswitcher=ccswitcher.cli:main",
        ],
    },
)
