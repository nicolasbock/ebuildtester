#!/usr/bin/env python

from setuptools import setup

from sphinx.setup_command import BuildDoc
cmdclass = {'build_sphinx': BuildDoc}

with open("README.rst", "r") as fh:
    long_description = fh.read()

name = "ebuildtester"

setup(
    name=name,
    author="Nicolas Bock",
    author_email="nicolasbock@gmail.com",
    description="A container approach to test a Gentoo package within a clean stage3 container",
    license="BSD",
    url="http://ebuildtester.readthedocs.io/",
    long_description=long_description,
    long_description_content_type="text/x-rst",

    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    packages=["ebuildtester"],
    entry_points={
        "console_scripts": [
            "ebuildtester = ebuildtester.main:main"
        ]
    },
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'release': ('setup.py', release),
            'source_dir': ('setup.py', 'doc')}},
)
