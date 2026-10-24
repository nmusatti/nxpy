.. nxpy documentation ----------------------------------------------------------

.. Copyright Nicola Musatti 2017 - 2026
.. Use, modification, and distribution are subject to the Boost Software
.. License, Version 1.0. (See accompanying file LICENSE.txt or copy at
.. http://www.boost.org/LICENSE_1_0.txt)

.. See https://github.com/nmusatti/nxpy. ---------------------------------------

Creating new releases
=====================

Libraries should only be released when needed. Each library is built and released on its own from
its directory under ``libs``; the combined ``Nxpy`` project in the root directory is not built.

The steps below use `uv`_ to build packages and to create test environments, and run `twine`_
through ``uvx``. In the commands ``<lib>`` is the library directory name, e.g. ``maven``, and
``<package>`` the package name, e.g. ``nxpy-maven``.

Preparation
-----------

* Run ``tox -p`` in the root directory of your development checkout. tox runs the environments for
  the current platform only, for every supported Python release that it finds or that uv can
  install.
* Commit any remaining change and push upstream. Check that the GitHub Actions tests pass on all
  supported platforms and Python versions.
* Bump the library version number in its ``pyproject.toml`` according to semantic versioning:
  increment the minor version element if the new release includes API breaking changes, the patch
  version element otherwise. Add ``rc1`` to the version number to mark the fact that this is a
  release candidate, e.g. ``1.1.0rc1``.
* If the library requires a newer release of another Nxpy library, update its ``dependencies``
  with that library's release candidate as the lower bound, e.g. ``nxpy_xml>=1.1.0rc1``. The final
  release satisfies it too, while ``nxpy_xml>=1.1.0`` would reject both the release candidate and
  the development version installed by tox.
* Update any other release related file, e.g.:

  + ``CHANGES.txt``
  + ``README.rst``

* Commit the changes.

Building
--------

Always build from a clean export of the repository, not from your development checkout: setuptools
merges the file list of an existing ``*.egg-info`` directory into the packages, so stale build
files may end up in them.

* Export the current commit and build the library::

    git archive HEAD | tar x -C <export dir>
    uv build --out-dir <dist dir> <export dir>/libs/<lib>

* Check the contents of the resulting packages in ``<dist dir>``. Wheels must not contain
  ``nxpy/__init__.py``, ``nxpy/core/__init__.py`` or ``_test`` packages.
* Run ``uvx twine check --strict <dist dir>/*``. Fix any resulting problem.

Release candidate
-----------------

* Run ``uvx twine upload --repository testpypi <dist dir>/*`` to upload the library to
  `Test PyPI`_. You will need a Test PyPI account and an API token for that.
* Create a new virtual environment and install the new library in it::

    uv venv <venv dir>
    uv pip install --refresh --python <venv dir> --index-url https://test.pypi.org/simple/ \
        --extra-index-url https://pypi.org/simple/ --index-strategy unsafe-best-match \
        <package>==<version>

  Naming the exact release candidate, e.g. ``nxpy-maven==1.1.0rc1``, lets uv install it without
  accepting pre-releases of the other dependencies; release candidates of other Nxpy libraries
  are still installed when the package's requirements name them. ``--refresh`` makes uv fetch the
  index again instead of using a cached copy that predates the upload.
* Perform a minimal test.

Release
-------

* Remove the ``rc1`` suffix from the version number in ``pyproject.toml``, commit and push.
* Export and build again in an empty ``<dist dir>``, check the contents of the resulting packages
  and run ``uvx twine check --strict <dist dir>/*``.
* Run ``uvx twine upload <dist dir>/*`` to upload the library to `PyPI`_. You will need a PyPI
  account and an API token.
* Create another virtual environment, install the new library in it with
  ``uv pip install --refresh --python <venv dir> <package>`` and perform a last test.
  Right after an upload the index may still list only the previous release; if that is what gets
  installed, wait a minute and try again.

Supported versions and platforms
--------------------------------

  +---------------------------+
  | Supported Python versions |
  +---------------------------+
  | 3.11                      |
  +---------------------------+
  | 3.12                      |
  +---------------------------+
  | 3.13                      |
  +---------------------------+
  | 3.14                      |
  +---------------------------+
  | 3.15                      |
  +---------------------------+

  +---------------------------+
  | Supported platforms       |
  +---------------------------+
  | Linux                     |
  +---------------------------+
  | macOS                     |
  +---------------------------+
  | Windows                   |
  +---------------------------+


.. _PyPI: https://pypi.org/
.. _Test PyPI: https://test.pypi.org/
.. _twine: https://twine.readthedocs.io/
.. _uv: https://docs.astral.sh/uv/
