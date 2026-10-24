.. nxpy documentation ----------------------------------------------------------

.. Copyright Nicola Musatti 2017 - 2018
.. Use, modification, and distribution are subject to the Boost Software
.. License, Version 1.0. (See accompanying file LICENSE.txt or copy at
.. http://www.boost.org/LICENSE_1_0.txt)

.. See https://github.com/nmusatti/nxpy. ---------------------------------------

Generating the documentation
============================

Nxpy's documentation is written in reStructuredText and rendered with Sphinx. It is published on
`ReadTheDocs`_, configured by ``.readthedocs.yaml`` in the root directory; the requirements for
building it are listed in ``docs/requirements.txt``.

To build the HTML documentation locally with `uv`_, run the following in the root directory::

    uv run --no-project --with-requirements docs/requirements.txt sphinx-build -b html docs docs/_build/html


.. _ReadTheDocs: https://nxpy.readthedocs.io/
.. _uv: https://docs.astral.sh/uv/
