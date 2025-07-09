Introduction
============

This is a tool to test a Gentoo ebuild and its dependencies. The idea is that
the ebuild is emerged in a clean (and current) stage3 Docker container.

.. image:: https://badge.fury.io/py/ebuildtester.svg
    :target: https://badge.fury.io/py/ebuildtester

.. image:: https://readthedocs.org/projects/ebuildtester/badge/?version=latest
   :target: http://ebuildtester.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://github.com/nicolasbock/ebuildtester/actions/workflows/build.yaml/badge.svg
   :target: https://github.com/nicolasbock/ebuildtester/actions?query=workflow%3Abuild
   :alt: GitHub Actions

.. image:: https://badges.gitter.im/ebuildtester/ebuildtester.svg
   :alt: Join the chat at https://gitter.im/ebuildtester/ebuildtester
   :target: https://gitter.im/ebuildtester/ebuildtester?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

.. image:: https://snapcraft.io/ebuildtester/badge.svg
   :alt: Get it from the Snap Store
   :target: https://snapcraft.io/ebuildtester

Requirements
------------

Using require `Docker <https://wiki.gentoo.org/wiki/Docker>`_ and `FUSE
<https://wiki.gentoo.org/wiki/Filesystem_in_Userspace>`_.

If you plan to use specific storage driver options (by passing
``--storage-opt``), be aware that these are specific to the `configured Docker
storage driver
<https://docs.docker.com/storage/storagedriver/select-storage-driver/>`__. Refer
to the Docker documentation about `storage drivers
<https://docs.docker.com/storage/storagedriver/>`_ for more information.
Particularly see the list of `options per storage driver
<https://docs.docker.com/engine/reference/commandline/dockerd/#options-per-storage-driver>`_.

System-wide configuration of the storage driver used by Docker is done in
``/etc/docker/daemon.json``. For example, to select the `devicemapper
<https://docs.docker.com/storage/storagedriver/device-mapper-driver/>`_ storage
driver, specify:

.. code-block:: javascript

   {
     "storage-driver": "devicemapper"
   }

Usage
-----

We are going to assume that the user has a local git clone of the portage tree in

.. code-block:: console

   /usr/local/git/gentoo

We have added a new ebuild and would like to verify that the build
dependencies are all correct. We can build the package (ATOM) with:

.. code-block:: console

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

.. code-block:: console

   usage: ebuildtester [-h] [--version] [--atom ATOM [ATOM ...]] [--binhost BINHOST] [--live-ebuild]
                       [--manual] --portage-dir PORTAGE_DIR [--overlay-dir OVERLAY_DIR] [--update]
                       [--install-basic-packages] [--threads N] [--use USE [USE ...]]
                       [--global-use GLOBAL_USE [GLOBAL_USE ...]] [--unmask ATOM] [--unstable]
                       [--gcc-version VER] [--python-single-target PYTHON_SINGLE_TARGET]
                       [--python-targets PYTHON_TARGETS] [--rm] [--storage-opt STORAGE_OPT [STORAGE_OPT ...]]
                       [--with-X] [--with-vnc] [--profile PROFILE] [--features FEATURES [FEATURES ...]]
                       [--docker-image DOCKER_IMAGE] [--docker-command DOCKER_COMMAND] [--pull]
                       [--show-options] [--ccache CCACHE_DIR] [--batch]

   A dockerized approach to test a Gentoo package within a clean stage3.

   options:
     -h, --help            show this help message and exit
     --version             show program's version number and exit
     --atom ATOM [ATOM ...]
                           The package atom(s) to install
     --binhost BINHOST     Binhost URI
     --live-ebuild         Unmask the live ebuild of the atom
     --manual              Install package manually
     --portage-dir PORTAGE_DIR
                           The local portage directory
     --overlay-dir OVERLAY_DIR
                           Add overlay dir (can be used multiple times)
     --update              Update container before installing atom
     --install-basic-packages
                           Install basic packages after container starts
     --threads N           Use N (default 8) threads to build packages
     --use USE [USE ...]   The use flags for the atom
     --global-use GLOBAL_USE [GLOBAL_USE ...]
                           Set global USE flag
     --unmask ATOM         Unmask atom (can be used multiple times)
     --unstable            Globally 'unstable' system, i.e. ~amd64
     --gcc-version VER     Use gcc version VER
     --python-single-target PYTHON_SINGLE_TARGET
                           Specify a PYTHON_SINGLE_TARGET
     --python-targets PYTHON_TARGETS
                           Specify a PYTHON_TARGETS
     --rm                  Remove container after session is done
     --storage-opt STORAGE_OPT [STORAGE_OPT ...]
                           Storage driver options for all volumes (same as Docker param)
     --with-X              Globally enable the X USE flag
     --with-vnc            Install VNC server to test graphical applications
     --profile PROFILE     The profile to use (default = default/linux/amd64/23.0)
     --features FEATURES [FEATURES ...]
                           Set FEATURES, see https://wiki.gentoo.org/wiki/FEATURES (default = ['-sandbox',
                           '-usersandbox', 'userfetch'])
     --docker-image DOCKER_IMAGE
                           Specify the docker image to use (default = gentoo/stage3)
     --docker-command DOCKER_COMMAND
                           Specify the docker command
     --pull                Download latest docker image
     --show-options        Show currently selected options and defaults
     --ccache CCACHE_DIR   Path to mount that contains ccache cache
     --batch               Do not drop into interactive shell

It is also possible to store default values in a toml configuration file at `~/.config/ebuildtester/config.toml`.
The next example shows all the configuration options that are currently available:

.. code-block:: toml

    portage_dir = "/var/db/repos/gentoo"
    overlay_dir = ["/var/db/repos/guru"]

    features = ["sandbox", "usersandbox", "userfetch"]

    install_basic_packages = false
    docker_command = "docker"
    unstable = true
    update = true
    batch = false
    pull = true
    rm = true
