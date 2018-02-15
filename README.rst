Introduction
============

This script is a tool to test a Gentoo ebuild and its
dependencies. The idea is that the package is emerged in a clean (and
current) stage3 Docker container.

.. image:: https://travis-ci.org/nicolasbock/ebuildtester.svg?branch=master
    :target: https://travis-ci.org/nicolasbock/ebuildtester

.. image:: https://badge.fury.io/py/ebuildtester.svg
    :target: https://badge.fury.io/py/ebuildtester

.. image:: https://readthedocs.org/projects/ebuildtester/badge/?version=latest
   :target: http://ebuildtester.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://badge.waffle.io/nicolasbock/ebuildtester.svg?columns=all
   :target: https://waffle.io/nicolasbock/ebuildtester
   :alt: 'Waffle.io - Columns and their card count'


Usage
-----

We are going to assume that the user has a local git clone of the portage tree in

.. code-block:: bash

   /usr/local/git/gentoo

We have added a new ebuild and would like to verify that the build
dependencies are all correct. We can build the package (ATOM) with:

.. code-block:: bash

   ebuildtester --portage-dir /usr/local/git/gentoo \
     --atom ATOM \
     --use USE1 USE2

where we have specified two USE flags, USE1 and USE2. The
`ebuildtester` command will now create a docker container and start
installing the ATOM. All specified dependencies will be installed as
well.


Command line arguments
----------------------

The command understands the following command line arguments:

.. code-block:: bash

   usage: ebuildtester [-h] [--atom ATOM [ATOM ...]] [--manual] --portage-dir
                       PORTAGE_DIR [--overlay-dir OVERLAY_DIR] [--update]
                       [--threads N] [--use USE [USE ...]] [--unmask ATOM]
                       [--gcc-version VER] [--with-X]

   optional arguments:
     -h, --help            show this help message and exit
     --atom ATOM [ATOM ...]
                           The package atom(s) to install
     --manual              Install package manually
     --portage-dir PORTAGE_DIR
                           The local portage directory
     --overlay-dir OVERLAY_DIR
                           Add overlay dir (can be used multiple times)
     --update              Update container before installing atom
     --threads N           Use N threads to build packages
     --use USE [USE ...]   The use flags for the atom
     --unmask ATOM         Unmask atom (can be used multiple times)
     --gcc-version VER     Use gcc version VER
     --with-X              Install VNC server to test graphical applications
