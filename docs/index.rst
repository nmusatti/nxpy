.. nxpy documentation ----------------------------------------------------------

.. Copyright Nicola Musatti 2010 - 2018
.. Use, modification, and distribution are subject to the Boost Software
.. License, Version 1.0. (See accompanying file LICENSE.txt or copy at
.. http://www.boost.org/LICENSE_1_0.txt)

.. See https://github.com/nmusatti/nxpy. ---------------------------------------

.. Nxpy documentation master file, created by
   sphinx-quickstart on Sat Apr 30 22:44:21 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


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


The libraries are being developed with Python 3.7 so as to be compatible with Python 2.7. Tests are
run and most modules work also with 3.4, 3.5 and 3.6. Some should still work with versions as early
as 3.2 and 2.5.

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
