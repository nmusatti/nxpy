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

The libraries should be considered in maintenance mode, where only small changes are applied from
time to time. Tests are usually run against the currently supported Python versions, which at this
time are 3.13, 3.12, 3.11, 3.10 and 3.9.

Note that these libraries are old: the bulk of the development took place between 2007 and 2009.
Most would benefit from a bit of modernization, but this is not likely to happen as I only code in
Python sporadically. Code supporting old Python releases has not been removed and some of the
libraries may still work with versions as early as 3.2 and 2.5. On the other hand no test has been
run on older releases for a long time, so there is no guarantee that they work and, if they do,
that they will continue to do so. 

Originally the libraries resided on `SourceForge`_ and were distributed as a single package.
Starting from release 1.0.0 each library is being packaged separately even though they are all
hosted within this project.

.. _ReadTheDocs: https://nxpy.readthedocs.io/en/latest/
.. _SourceForge: http://nxpy.sourceforge.net
