Nxpy Sort
=========

You can install the library with pip::

    pip install nxpy-sort

*Nxpy Sort* provides the ``topological_sort()`` function which takes a sequence of ordered couples
of values and returns a single sequence where each value is guaranteed to come before every value
that comes after it in any of the input couples. When this is not possible, e.g. for inputs like
``(1 2) (2 1)``, ``None`` is returned.

The library's documentation is available on
`ReadTheDocs <https://nxpy.readthedocs.io/en/latest/sort.html>`_.
