Developer Documentation
=======================

This project supports Python 3.11 and later

For locally testing changes it is very handy to install `tox` which automates
the creation of Python virtual environments.

Dependencies
------------

- `docker`
- `fuse`

Setting up a developer environment
----------------------------------

.. code-block:: console

    $ python -m virtualenv venv
    $ source venv/bin/activate
    $ (venv) pip install -r requirements.txt

Install `ebuildtester` in the `virtualenv`:

.. code-block:: console

    $ (venv) pip install .

Run the development version:

.. code-block:: console

    $ (venv) ebuildtester ...
