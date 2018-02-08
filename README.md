# gentoo-test-package

[![Build Status](https://travis-ci.org/nicolasbock/gentoo-test-package.svg?branch=master)](https://travis-ci.org/nicolasbock/gentoo-test-package)
[![PyPI version](https://badge.fury.io/py/ebuildtester.svg)](https://badge.fury.io/py/ebuildtester)
[![Documentation Status](https://readthedocs.org/projects/ebuildtester/badge/?version=latest)](http://ebuildtester.readthedocs.io/en/latest/?badge=latest)

A dockerized approach to test a Gentoo package within a clean stage3.

Usage
=====

```bash
ebuildtester --portage-dir /usr/portage --overlay-dir /usr/local/portage --use R boost imaging python qt5 rendering views --unmask =sci-libs/vtk-8.0.1 --with-X --atom =sci-libs/vtk-8.0.1
```
