.. nxpy documentation ----------------------------------------------------------

.. Copyright Nicola Musatti 2010 - 2021
.. Use, modification, and distribution are subject to the Boost Software
.. License, Version 1.0. (See accompanying file LICENSE.txt or copy at
.. http://www.boost.org/LICENSE_1_0.txt)

.. See https://github.com/nmusatti/nxpy. ---------------------------------------


Nick's Python Toolbox
=====================

Nxpy is an etherogeneous collection of libraries, dealing with diverse topics such as wrapping
complex commands with API's, automation of backup files, support for writing your own file-like
objects and many other things.


.. toctree::
   :maxdepth: 1

   abstract.rst
   backup_file.rst
   command.rst
   file_object.rst
   file.rst
   maven.rst
   memo.rst
   nonblocking_subprocess.rst
   past.rst
   path.rst
   ply.rst
   sequence.rst
   sort.rst
   svn.rst
   temp_file.rst
   test.rst
   xml.rst
   core.rst
   testing.rst
   doc_gen.rst
   releasing.rst


Tests are run with Python 3.11, 3.12, 3.13, 3.14 and 3.15 on Linux, macOS and Windows. The code is
still meant to be compatible with Python 2.7, but this is no longer tested and the packages are
built for Python 3 only. Python 2.x support is likely to be removed in the future.

Originally the libraries resided on `SourceForge`_ and were distributed as a single package.
Starting from release 1.0.0 each library is being packaged separately even though they are all
hosted within the same project on `GitHub`_.

The Nxpy logo was drawn by Claudia Romano.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _SourceForge: http://nxpy.sourceforge.net/
.. _GitHub: https://github.com/nmusatti/nxpy
