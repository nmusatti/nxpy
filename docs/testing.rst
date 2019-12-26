.. nxpy documentation ----------------------------------------------------------

.. Copyright Nicola Musatti 2017 - 2019
.. Use, modification, and distribution are subject to the Boost Software
.. License, Version 1.0. (See accompanying file LICENSE.txt or copy at
.. http://www.boost.org/LICENSE_1_0.txt)

.. See https://github.com/nmusatti/nxpy. ---------------------------------------

Running the tests
=================

Nxpy tests are based on the standard ``unittest`` module. As recent features are used the
``unittest2`` backport is required with Python 2.6. Tests reside in ``_test`` subdirectories of the
library package directory. For each ``module`` module tests should be found in a ``test_module``
module.

Tests may be run for all supported Python versions installed on your system and present in your
``PATH`` environment variable with ``tox`` and ``pytest``. Dependencies from libraries available
from PyPI are automatically installed by tox. The following additional requirements should also be
fulfilled:

* The ``nxpy-maven`` library requires that a recent version of Maven be present in your ``PATH``.
* The ``nxpy-svn`` library requires that a recent version of Subversion be present in your ``PATH``.
