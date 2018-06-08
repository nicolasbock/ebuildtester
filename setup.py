#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="ebuildtester",
    author="Nicolas Bock",
    author_email="nicolasbock@gmail.com",
    description="A container approach to test a Gentoo package within a clean stage3",
    license="BSD",
    url="https://github.com/nicolasbock/gentoo-test-package",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    packages=["ebuildtester"],
    entry_points={
        "console_scripts": [
            "ebuildtester = ebuildtester.main:main"
        ]
    }
)
