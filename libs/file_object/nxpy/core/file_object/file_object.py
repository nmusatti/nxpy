# nxpy.core package ----------------------------------------------------------

# Copyright Nicola Musatti 2008 - 2015
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See http://nxpy.sourceforge.net for library home page. ---------------------

r"""
Helper classes for the implementation of read-only and writable file objects that forward calls
to an actual file object variable.

"""

from __future__ import absolute_import


class ReadOnlyFileObject(object):
    r"""
    Implement the non modifying portion of the file object protocol by delegating to 
    another file object.
    
    Subclass and override as needed.
    """
    def __init__(self, file_=None):
        r"""Set the delegate file object."""
        self.setFile(file_)

    def setFile(self, file_):
        r"""Set the delegate file object."""
        self._file = file_

    def __iter__(self):
        return self._file.__iter__()

    def __next__(self):
        return self._file.__next__()

    def __getattr__(self, name):
        if name in ( "truncate", "write", "writeline" ):
            raise AttributeError()
        return getattr(self._file, name)


class WritableFileObject(ReadOnlyFileObject):
    r"""
    Implement the file object protocol by delegating to another file object.
    
    Subclass and override as needed.
    """
    def __init__(self, file_=None):
        super(WritableFileObject, self).__init__(file_)

    def __getattr__(self, name):
        return getattr(self._file, name)
