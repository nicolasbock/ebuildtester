#!/usr/bin/env python

from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="ebuildtester",
    author="Nicolas Bock",
    author_email="nicolasbock@gmail.com",
    maintainer="Nicolas Bock",
    maintainer_email="nicolasbock@gmail.com",
    description="A container approach to test a Gentoo package within a clean stage3 container",
    license="BSD",
    url="http://ebuildtester.readthedocs.io/",
    download_url="https://github.com/nicolasbock/ebuildtester",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    packages=["ebuildtester"],
    # package_dir={"ebuildtester": "ebuildtester"},
    # package_data={"ebuildtester": ["data/ebuildtester.bash-completion"]},
    # include_package_data=True,
    data_files=[(".", ["ebuildtester/data/ebuildtester.bash-completion"])],
    entry_points={
        "console_scripts": [
            "ebuildtester = ebuildtester.main:main"
        ]
    }
)
