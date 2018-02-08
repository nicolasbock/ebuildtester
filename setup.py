#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="ebuildtester",
    version="0.1.2",
    packages=["ebuildtester"],
    entry_points={
        "console_scripts": ["ebuildtester = ebuildtester.main:main"]
    },
    author="Nicolas Bock",
    author_email="nicolasbock@gmail.com",
    description="A dockerized approach to test a Gentoo package within a clean stage3",
    license="BSD",
    url="https://github.com/nicolasbock/gentoo-test-package",
    project_urls={
        "Releases": "https://github.com/nicolasbock/gentoo-test-package/releases"
    }
)
