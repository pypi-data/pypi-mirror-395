#!/usr/bin/env python
"""
Setup script for coherence-sim package.
For modern installations, use pyproject.toml with pip install.
"""

from setuptools import find_packages, setup

if __name__ == "__main__":
    setup(
        name="coherence-sim",
        version="1.0.0",
        packages=find_packages(),
        install_requires=[
            "numpy>=1.20.0",
            "matplotlib>=3.5.0",
            "scipy>=1.7.0",
        ],
        python_requires=">=3.8",
    )
