Developer Documentation
=======================

This project supports Python 3.8, 3.9, 3.10, 3.11 and 3.12. Other Python versions
might work as well but are not regularly tested.

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

    $ (venv) python setup.py install

Run the development version:

.. code-block:: console

    $ (venv) ebuildtester ...
