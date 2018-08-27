# nxpy.command package -------------------------------------------------------

# Copyright Nicola Musatti 2011 - 2014
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See http://nxpy.sourceforge.net for library home page. ---------------------

r"""
Tools to wrap a Python API around interactive and non-interactive programs.

The :py:class:`.command.Command` and :py:class:`interpreter.Interpreter` classes handle batch and 
interactive commands respectively. They can be provided with :py:class:`.option.Config` instances
which describe the options available to the programs being wrapped. The :py:class:`.option.Parser` 
class can then be used to validate option sets and construct the corresponding command lines.
See the :py:mod:`.svn.svn` module for a concrete example.

"""
