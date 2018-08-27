# nxpy.core package ----------------------------------------------------

# Copyright Nicola Musatti 2013 - 2015
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See http://nxpy.sourceforge.net for library home page. ---------------------

r"""
filesystem related utilities.

"""

from __future__ import absolute_import

import logging
import os
import shutil
import stat


def _on_error(func, path, ex_info):
    r"""Error handler for :py:func:`shutil.rmtree`."""
    try:
        mode = os.stat(path).st_mode
        if not stat.S_ISLNK(mode):
            os.chmod(path, mode | stat.S_IWRITE)
            if stat.S_ISDIR(mode):
                os.rmdir(path)
            else:
                os.remove(path)
        return
    except:
        pass
    logging.error(path + ": not removed")


def blasttree(dir_):
    r"""Remove a directory more stubbornly than :py:func:`shutil.rmtree`.

    Required on filesystems that do not allow removal of non-writable files
    
    """
    shutil.rmtree(dir_, ignore_errors=False, onerror=_on_error)


class CurrentDirectory(object):
    r"""A context manager that allows changing the current directory temporarily."""
    def __init__(self, path):
        r"""Set the current directory to *path*."""
        self._path = path
        self._prev = os.getcwd()
        self._curr = self._prev
    
    @property
    def current(self):
        r"""Return the current directory."""
        return self._curr

    def __enter__(self):
        os.chdir(self._path)
        self._curr = os.getcwd()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self._prev)
        self._curr = self._prev
        return False
