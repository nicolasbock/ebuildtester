.. toctree::
   :maxdepth: 2
   :caption: Contents:


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


Requirements
------------

You require `Docker <https://wiki.gentoo.org/wiki/Docker>`_ and `FUSE
<https://wiki.gentoo.org/wiki/Filesystem_in_Userspace>`_. Docker must be
configured to use the `devicemapper
<https://docs.docker.com/storage/storagedriver/device-mapper-driver/>`_
storage driver.  This can be achieved with the following inside
``/etc/docker/daemon.json``:

.. code-block:: javascript

   {
     "storage-driver": "devicemapper"
   }

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

    usage: ebuildtester [-h] [--version] [--atom ATOM [ATOM ...]] [--live-ebuild]
                             [--manual] --portage-dir PORTAGE_DIR
                             [--overlay-dir OVERLAY_DIR] [--update {yes,true,no,false}]
                             [--threads N] [--use USE [USE ...]]
                             [--global-use GLOBAL_USE [GLOBAL_USE ...]] [--unmask ATOM]
                             [ --python-single-target VAR ] [ --python-targets VAR ]
                             [--unstable] [--gcc-version VER] [--rm] [--with-X]
                             [--with-vnc]
                             [--profile {default/linux/amd64/17.0,default/linux/amd64/17.0/systemd}]

    A dockerized approach to test a Gentoo package within a clean stage3.

    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      --atom ATOM [ATOM ...]
                            The package atom(s) to install
      --live-ebuild         Unmask the live ebuild of the atom
      --manual              Install package manually
      --portage-dir PORTAGE_DIR
                            The local portage directory
      --overlay-dir OVERLAY_DIR
                            Add overlay dir (can be used multiple times)
      --update {yes,true,no,false}
                            Update container before installing atom
      --threads N           Use N (default 8) threads to build packages
      --use USE [USE ...]   The use flags for the atom
      --global-use GLOBAL_USE [GLOBAL_USE ...]
                            Set global USE flag
      --unmask ATOM         Unmask atom (can be used multiple times)
      --unstable            Globally 'unstable' system, i.e. ~amd64
      --gcc-version VER     Use gcc version VER
      --python-single-target  Define a PYTHON_SINGLE_TARGET variable
      --python-targets        Define a PYTHON_TARGETS variable
      --rm                  Remove container after session is done
      --with-X              Globally enable the X USE flag
      --with-vnc            Install VNC server to test graphical applications
      --profile {default/linux/amd64/17.0,default/linux/amd64/17.0/systemd}

Mailing List
============

.. raw:: html

   <div class="classictemplate template" style="display: block;">
   <style type="text/css">
     #groupsio_embed_signup input {border:1px solid #999; -webkit-appearance:none;}
     #groupsio_embed_signup label {display:block; font-size:16px; padding-bottom:10px; font-weight:bold;}
     #groupsio_embed_signup .email {display:block; padding:8px 0; margin:0 4% 10px 0; text-indent:5px; width:58%; min-width:130px;}
     #groupsio_embed_signup {
       background:#fff; clear:left; font:14px Helvetica,Arial,sans-serif;
     }
     #groupsio_embed_signup .button {

         width:25%; margin:0 0 10px 0; min-width:90px;
         background-image: linear-gradient(to bottom,#337ab7 0,#265a88 100%);
         background-repeat: repeat-x;
         border-color: #245580;
         text-shadow: 0 -1px 0 rgba(0,0,0,.2);
         box-shadow: inset 0 1px 0 rgba(255,255,255,.15),0 1px 1px rgba(0,0,0,.075);
         padding: 5px 10px;
         font-size: 12px;
         line-height: 1.5;
         border-radius: 3px;
         color: #fff;
         background-color: #337ab7;
         display: inline-block;
         margin-bottom: 0;
         font-weight: 400;
         text-align: center;
         white-space: nowrap;
         vertical-align: middle;
       }
   </style>
   <div id="groupsio_embed_signup">
   <form action="https://groups.io/g/ebuildtester/signup?u=5161632144670903757" method="post" id="groupsio-embedded-subscribe-form" name="groupsio-embedded-subscribe-form" target="_blank">
       <div id="groupsio_embed_signup_scroll">
         <label for="email" id="templateformtitle">Subscribe to our group</label>
         <input type="email" value="" name="email" class="email" id="email" placeholder="email address" required="">

       <div style="position: absolute; left: -5000px;" aria-hidden="true"><input type="text" name="b_5161632144670903757" tabindex="-1" value=""></div>
       <div id="templatearchives"><p><a id="archivelink" href="https://groups.io/g/ebuildtester/topics">View Archives</a></p></div>
       <input type="submit" value="Subscribe" name="subscribe" id="groupsio-embedded-subscribe" class="button">
     </div>
   </form>
   </div>
   </div>
