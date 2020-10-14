.. nxpy documentation ----------------------------------------------------------

.. Copyright Nicola Musatti 2017 - 2020
.. Use, modification, and distribution are subject to the Boost Software
.. License, Version 1.0. (See accompanying file LICENSE.txt or copy at
.. http://www.boost.org/LICENSE_1_0.txt)

.. See https://github.com/nmusatti/nxpy. ---------------------------------------

Creating new releases
=====================

Libraries should only be released when needed. Although a combined package is not released, its
configuration should be updated to reflect library changes.

Assuming all changes to code and documentation have been pushed to the upstream repository, the
basic steps for the creation of a new library release are:

* Run ``tox`` in the root directory of your development checkout. Ideally you should be developing
  against the most recent supported Python release on one of the supported platforms. As long as
  Python 2.7 is supported tests should be run against it too.
* Update any release related configuration file, e.g.:

  + ``CHANGES.txt``
  + ``README.rst``
  + ``setup.py``

* Commit to ``master`` any remaining change and push upstream. This should trigger Travis tests
  against all the supported Python versions.
* Bump the library version number according to semantic versioning: increment the minor version
  element if the new release includes API breaking changes, the increment version element otherwise.
  Add ``rc1`` to the release number to mark the fact that this is a release candidate.
* Run ``python setup.py sdist bdist_wheel`` in the library's root directory. Check the contents of
  the resulting packages in the ``dist`` directory.
* Run ``twine check dist/*``. Fix any resulting problem.
* Run ``twine upload --repository-url https://test.pypi.org/legacy/ dist/*`` to upload the library
  to `Test PyPI`_. You will need a Test PyPI account for that.
* Create a new virtualenv and install the new library in it with
  ``pip install --index-url https://test.pypi.org/simple/ --no-deps --pre <<Library>>``.
* Perform a minimal test.
* Remove the ``build``, ``dist`` and ``<<Library>>.egg-info`` directories.
* Remove the ``rc1`` prefix from the version number in the ``setup.py`` file.
* Commit and push all outstanding changes.
* Run ``python setup.py sdist bdist_wheel`` again and check the contents of the resulting packages.
* Run ``twine check dist/*``.
* Run ``twine upload dist/*`` to upload the library to `PyPI`_. You will need a PyPI account.
* Create another virtualenv and install the new library in it with ``pip install <<Library>>``.
* Perform a last test.

  +---------------------------+
  | Supported Python versions |
  +---------------------------+
  | 2.7                       |
  +---------------------------+
  | 3.6                       |
  +---------------------------+
  | 3.7                       |
  +---------------------------+
  | 3.8                       |
  +---------------------------+
  | 3.9                       |
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


.. _PyPI: https://pypi.org/
.. _Test PyPI: https://test.pypi.org/
