# nxpy_temp_file --------------------------------------------------------------

# Copyright Nicola Musatti 2010 - 2018
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See https://github.com/nmusatti/nxpy/tree/master/libs/temp_file. ------------

r"""
Temporary files and directories.

Requires at least Python 2.6

"""

from __future__ import absolute_import

import logging
import os
import shutil
import stat
import tempfile

import nxpy.core.file_object
import nxpy.core.path
import nxpy.core.past


class TempFile(nxpy.core.file_object.WritableFileObject):
    r"""A temporary file that implements the context manager protocol.
    
    Wrap a :py:func:`tempfile.NamedTemporaryFile` generated file-like object, to ensure it is not
    deleted on close, but rather when the underlying context is closed.
    
    """
    def __init__(self, *args, **kwargs):
        r"""Create a temporary file with the given arguments."""
        # Python 2.5 compatible syntax. Doesn't work, but ensures that tests are skipped rather
        # than broken.
        # file = tempfile.NamedTemporaryFile(*args, delete=False, **kwargs)
        kwargs["delete"] = False
        if nxpy.core.past.V_2_7.at_most() and "encoding" in kwargs:
            del kwargs["encoding"]
        file_ = tempfile.NamedTemporaryFile(*args, **kwargs)
        super(TempFile, self).__init__(file_)
    
    @property
    def name(self):
        r"""Return the actual file name."""
        return self._file.name

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file.close()
        os.remove(self._file.name)
        return False


class TempDir(object):
    r"""A temporary directory that implements the context manager protocol.
    
    The directory is removed when the context is exited from. Uses :py:func:`tempfile.mkdtemp` to 
    create the actual directory.
    
    """
    def __init__(self, *args, **kwargs):
        r"""Create a temporary directory with the given arguments."""
        self.dir = tempfile.mkdtemp(*args, **kwargs)
        mode = os.stat(self.dir).st_mode
        os.chmod(self.dir, mode | stat.S_IWRITE)

    @property
    def name(self):
        r"""Return the directory name."""
        return self.dir

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        nxpy.core.path.blasttree(self.dir)
        return False
