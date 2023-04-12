=================
shatoru-lifecycle
=================

.. image:: https://github.com/UMD-2022/shatoru-lifecycle/actions/workflows/test-all.yaml/badge.svg
    :target: https://github.com/UMD-2022/shatoru-lifecycle/actions/workflows/test-all.yaml
    :alt: Tests

.. image:: https://github.com/UMD-2022/shatoru-lifecycle/actions/workflows/documentation.yaml/badge.svg
    :target: https://UMD-2022.github.io/shatoru-lifecycle/
    :alt: Documentation

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code style: black

.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
    :target: https://pycqa.github.io/isort/
    :alt: imports: isort

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
    :target: https://github.com/pre-commit/pre-commit
    :alt: pre-commit

::

   This is a Python project quality guidelines

Prerequisites
-------------

-  Python ≥ 3.8.0
-  Conda ≥ 4.12.0
-  PostgreSQL ≥ 14
-  GNU Make ≥ 3.75

Python
~~~~~~

First make sure that you have python 3.10 or greater installed in your
system.

.. code:: bash

   python --version

If not then first `download <https://www.python.org/downloads/>`__ and
install the appropriate version of python in your system.

Virtual Environment
~~~~~~~~~~~~~~~~~~~

Before you start coding, we recommend creating an isolated `virtual
environment`_ to avoid any problems with your installed Python packages.
This can easily be done via either |virtualenv|_::

    pip install virtualenv
    virtualenv .venv
    source .venv/bin/activate

PostgreSQL
~~~~~~~~~~

Download PostgreSQL and PgAdmin (optional) from
`here <https://www.postgresql.org/download/>`__

GNU Make
~~~~~~~~

Usually, GNU Make comes installed by default on a Linux based system. If
you do not have GNU Make installed in your system then you can skip to
the next part.

Check the version of GNU Make of your system

.. code:: bash

   make --version

Getting Started
---------------

First setup and create a database named ``shatoru``.

Now, create a ``.env`` file from ``.env.sample``. Fill in your database
details and email information. To generate a secret key execute the
command below:

.. code:: bash

   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

After that, create a conda virtual environment

.. code:: bash

   virtualenv .venv


Once the installations have been completed activate the virtual
environment that you just created.

.. code:: bash

   source .venv/bin/activate

Always remember to activate your virtual environment before running the
backend server.

Now that we have the virtual environment activated, execute the commands
below to setup your backend and start the server

.. code:: bash

   make init
   make server

Tests
-----

Run the following command to install the test dependencies::

   pip install -e ".[test]"

You can now run the unit tests via `pytest`::

   pytest

The test files are under tests directory under shatoru_backend.

Run the following command to install dependencies for load test::

   pip install locust

Ypu can now run the command

   locust -f locustfiles --class-picker

Navigate to `http://localhost:8089 <http://localhost:8089>`_

The test files are under tests directory under shatoru_backend.

Documentation
-------------

You will need tox to generate your documentation::

   pip install tox

You can now generate the documentation using the following command::

   tox -e docs

The documentations would be generated in `docs/_build/html`. You can open the `index.html` file in your browser to view the generated documentation.

Other useful commands
~~~~~~~~~~~~~~~~~~~~~

.. to set python3 as your default
.. code:: bash

   code ~/.zshrc
   alias python="python3"

.. to activate the virtual environment
.. code:: bash

   source ./.venv/bin/activate

.. to install dependencies specified in dev key of cfg file | -e is used to install as editable
.. code:: bash

   pip install -e ".[dev]"

.. install all packages specified in test key of the cfg file
.. code:: bash

   pip install -e ".[test]"

.. code:: bash

   pip install flake8
   pip install -U black

.. code:: bash

   pre-commit
   pre-commit install
   pre-commit autoupdate

.. code:: bash

   pip install loguru

.. to check if pytest package is installed in venv
.. code:: bash

   pip show pytest

.. |virtualenv| replace:: ``virtualenv``

.. _virtual environment: https://realpython.com/python-virtual-environments-a-primer/
.. _virtualenv: https://virtualenv.pypa.io/en/stable/
