#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="ebuildtester",
    packages=["ebuildtester"],
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    entry_points={
        "console_scripts": ["ebuildtester = ebuildtester.main:main"]
    },
    author="Nicolas Bock",
    author_email="nicolasbock@gmail.com",
    description="A dockerized approach to test a Gentoo package within a clean stage3",
    license="BSD",
    url="https://github.com/nicolasbock/gentoo-test-package"
)
