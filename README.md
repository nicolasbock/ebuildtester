# ebuildtester

[![Build Status](https://travis-ci.org/nicolasbock/ebuildtester.svg?branch=master)](https://travis-ci.org/nicolasbock/ebuildtester)
[![PyPI version](https://badge.fury.io/py/ebuildtester.svg)](https://badge.fury.io/py/ebuildtester)
[![Documentation Status](https://readthedocs.org/projects/ebuildtester/badge/?version=latest)](http://ebuildtester.readthedocs.io/en/latest/?badge=latest)
[![Waffle.io - Columns and their card count](https://badge.waffle.io/nicolasbock/ebuildtester.png?columns=all)](https://waffle.io/nicolasbock/ebuildtester?utm_source=badge)

A dockerized approach to test a Gentoo package within a clean stage3.

Detailed documentation can be found at http://ebuildtester.readthedocs.io/.

Usage
=====

```bash
ebuildtester --portage-dir /usr/portage \
    --overlay-dir /usr/local/portage \
    --use R boost imaging python qt5 rendering views \
    --unmask =sci-libs/vtk-8.0.1 \
    --with-X \
    --atom =sci-libs/vtk-8.0.1
```
