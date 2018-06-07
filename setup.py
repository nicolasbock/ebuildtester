#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    long_description=long_description,
    long_description_content_type="text/rst",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    packages=["ebuildtester"],
    entry_points={
        "console_scripts": [
            "ebuildtester = ebuildtester.main:main"
        ]
    }
)
