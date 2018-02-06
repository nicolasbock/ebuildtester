#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="ebuildtester",
    version="0.1.0",
    packages=find_packages(),
    test_suite="tests",
    entry_points={
        "console_scripts": ["ebuildtester = ebuildtester.main:main"]
    }
)
