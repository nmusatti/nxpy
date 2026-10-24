.. nxpy documentation ----------------------------------------------------------

.. Copyright Nicola Musatti 2017 - 2026
.. Use, modification, and distribution are subject to the Boost Software
.. License, Version 1.0. (See accompanying file LICENSE.txt or copy at
.. http://www.boost.org/LICENSE_1_0.txt)

.. See https://github.com/nmusatti/nxpy. ---------------------------------------

Running the tests
=================

Nxpy tests are based on the standard ``unittest`` module and are run with ``pytest``. Tests reside
in ``_test`` subdirectories of the library package directory. For each ``module`` module tests
should be found in a ``test_module`` module.

Requirements
------------

* `tox`_ 4 with the `tox-uv`_ plugin, e.g. installed with ``uv tool install tox --with tox-uv``.
  With tox-uv, Python releases installed with uv, e.g. with ``uv python install 3.15``, are found as
  well as those in your ``PATH``.
* The ``nxpy-maven`` tests require Maven and a JDK in your ``PATH``. The test Maven projects target
  the oldest LTS JDK still in premier support, currently JDK 21, so that or a later JDK is needed.
* The ``nxpy-svn`` tests and the test environment setup require the Subversion command line tools,
  ``svn`` and ``svnadmin``, in your ``PATH``.

Running the tests with tox
--------------------------

The tox environments are named after the Python version and the platform, e.g. ``py313-lnx``,
``py313-mac`` or ``py313-win``. Run the following in the root directory of your development checkout:

* ``tox -p`` runs the tests for every supported Python version in parallel. Environments for other
  platforms are skipped.
* ``tox -e py313-lnx`` runs a single environment.
* ``tox -r -p`` recreates the environments. Do this after changing the dependencies of a library:
  tox doesn't reinstall them in existing environments, so a broken requirement may go unnoticed.

Each environment installs all the libraries in editable mode, builds the test environment in its
own temporary directory and runs the tests of all the libraries.

The test environment
--------------------

Several ``nxpy-maven`` and ``nxpy-svn`` tests work on test data: a Subversion repository, a working
copy of the Maven projects in ``test/backup`` and the files in ``test/data``. The
``test/bin/setup_test_env.py`` script creates them in the directory named by the ``NXPY_TEST_DIR``
environment variable, removing its previous contents. When ``NXPY_TEST_DIR`` isn't set, these tests
are skipped.

The tests modify the test data, so the test environment must be created again before each run. tox
does this automatically. To run the tests of a single library without tox, e.g. with the Python of
an existing tox environment on Linux or macOS::

    export NXPY_TEST_DIR=$PWD/.tox/py313-lnx/tmp
    .tox/py313-lnx/bin/python test/bin/setup_test_env.py
    .tox/py313-lnx/bin/python -m pytest libs/maven

Continuous integration
----------------------

GitHub Actions runs the tests on every push and pull request, for every supported Python version
on Linux, macOS and Windows with the oldest supported LTS JDK, and with the newest LTS JDK for the
newest Python version. The workflow is defined in ``.github/workflows/test.yml``.


.. _tox: https://tox.wiki/
.. _tox-uv: https://github.com/tox-dev/tox-uv
