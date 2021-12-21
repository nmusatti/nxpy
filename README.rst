Nick's Python Toolbox
=====================

.. image:: https://github.com/nmusatti/nxpy/actions/workflows/test.yml/badge.svg

.. image:: https://readthedocs.org/projects/nxpy/badge/?version=latest
    :target: https://nxpy.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Nxpy is an etherogeneous collection of libraries, dealing with diverse topics such as 
wrapping complex commands with API's, automation of backup files, support for writing your 
own file-like objects and many other things. The documentation is available on `ReadTheDocs`_.

The libraries are:

* *abstract*:    The ``abstractstatic`` method decorator.
* *backup_file*: Create backups for files you need to modify.
* *command*:     Tools to wrap possibly interactive commands with complex option sets.
* *file*:        File related utilities.
* *file_object*: File-like object implementation helpers.
* *maven*:       A Python interface to the Maven build tool.
* *memo*:        Base class for memoizable objects.
* *nonblocking_subprocess*: A ``Popen`` subclass that performs non-blocking I/O.
* *past*:        Tools for Python version compatibility management.
* *path*:        Filesystem related utilities.
* *ply*:         An object oriented wrapper for the PLY lexer/parser tool.
* *sequence*:    Sequence related utilities.
* *sort*:        Sorting functions.
* *svn*:         A wrapper for the Subversion version control tool.
* *temp_file*:   Temporary files and directories implemented as context managers.
* *test*:        Testing related utilities.
* *xml*:         XML related support classes, based on the lxml library.

The libraries are being developed with Python 3.10 so as to be compatible with Python 2.7. Tests are
run and most modules work also with 3.6, 3.7, 3.8 and 3.9. Some should still work with versions as
early as 3.2 and 2.5. There is no immediate plan to remove Python 2.x support, but in general
earlier releases will only be supported as long as external tools, such as GitHub Actions or pip,
keep supporting them. 

Originally the libraries resided on `SourceForge`_ and were distributed as a single package.
Starting from release 1.0.0 each library is being packaged separately even though they are all
hosted within this project.

.. _ReadTheDocs: https://nxpy.readthedocs.io/en/latest/
.. _SourceForge: http://nxpy.sourceforge.net
