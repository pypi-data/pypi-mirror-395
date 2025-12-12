#!/usr/bin/env python3
"""
Setup script for ioload
This file is kept for backward compatibility.
Modern builds use pyproject.toml
"""

from setuptools import setup

# Entry points need to be in setup.py for console scripts
setup(
    entry_points={
        "console_scripts": [
            "ioload=ioload:cli",
        ],
    },
)
