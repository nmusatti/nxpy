.. nxpy documentation ----------------------------------------------------------

.. Copyright Nicola Musatti 2017 - 2018
.. Use, modification, and distribution are subject to the Boost Software
.. License, Version 1.0. (See accompanying file LICENSE.txt or copy at
.. http://www.boost.org/LICENSE_1_0.txt)

.. See https://github.com/nmusatti/nxpy. ---------------------------------------

Creating a new release
======================

The basic steps for the creation of a new release are:

* Ensure that all the desired changes have been committed to the ``default`` branch.
* Run tests on all the supported versions of Python on all the supported platforms.

  +---------------------------+
  | Supported Python versions |
  +---------------------------+
  | 2.6                       |
  +---------------------------+
  | 2.7                       |
  +---------------------------+
  | 3.3                       |
  +---------------------------+
  | 3.4                       |
  +---------------------------+
  | 3.5                       |
  +---------------------------+
  | 3.6                       |
  +---------------------------+

  +---------------------------+
  | Supported platforms       |
  +---------------------------+
  | Linux                     |
  +---------------------------+
  | MacOS                     |
  +---------------------------+
  | Windows 7 or later        |
  +---------------------------+

* Ensure that all tests either pass or are skipped for a valid reason, e.g. a module requires a
  higher version of Python.
* Update release information where required:

  + ``CHANGES.txt``
  + ``DESCRIPTION.txt``
  + ``README.rst``
  + ``setup.py``
  + ``docs/index.rst``

* 