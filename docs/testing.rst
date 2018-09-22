.. nxpy documentation ---------------------------------------------------------

.. Copyright Nicola Musatti 2017
.. Use, modification, and distribution are subject to the Boost Software
.. License, Version 1.0. (See accompanying file LICENSE.txt or copy at
.. http://www.boost.org/LICENSE_1_0.txt)

.. See http://nxpy.sourceforge.net for library home page. ---------------------

Running the tests
=================

Nxpy tests are based on the standard ``unittest`` module. As recent features are used the
``unittest2`` backport is required with Python 2.6. Tests reside in ``_test`` subdirectories of the
library package directory. For each ``module`` module tests should be found in a ``test_module``
module.
