# nxpy.core package ----------------------------------------------------------

# Copyright Nicola Musatti 2010 - 2014
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See http://nxpy.sourceforge.net for library home page. ---------------------

r"""
File related utilities.

"""

# Python 2.5 compatibility
from __future__ import with_statement    
from __future__ import absolute_import

import os

import six
from six.moves import zip

import nxpy.core.past


def compare(file1, file2, ignore_eof=True, encoding=None):
    r"""
    Compare two text files for equality.
    If *ignore_eof* is *True*, end of line characters are not considered.
    If not *None* *encoding* is used to open the files. On Python 2.x *encoding* is ignored.
    
    """
    if isinstance(file1, six.string_types):
        f1 = open_(file1, "r", encoding=encoding)
    else:
        f1 = file1
        f1.seek(0, os.SEEK_SET)
    if isinstance(file2, six.string_types):
        f2 = open_(file2, "r", encoding=encoding)
    else:
        f2 = file2
        f2.seek(0, os.SEEK_SET)
    with f1:
        with f2:
            for l1, l2 in zip(f1, f2):
                if ( ( not ignore_eof and l1 != l2 ) or 
                     ( ignore_eof and l1.rstrip("\r\n") != l2.rstrip("\r\n") ) ):
                    return False
            return True


def open_(*args, **kwargs):
    r"""Open a file removing invalid arguments on Python 2.x."""
    if nxpy.core.past.V_2_7.at_most() and "encoding" in kwargs:
        del kwargs["encoding"]
    return open(*args, **kwargs)
