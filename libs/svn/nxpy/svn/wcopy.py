# nxpy_svn --------------------------------------------------------------------

# Copyright Nicola Musatti 2011 - 2018
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See https://github.com/nmusatti/nxpy/tree/master/libs/svn. ------------------

r"""
Working copy manipulation.

"""

from __future__ import absolute_import

import os.path

import nxpy.command.command
import nxpy.svn.svn
import nxpy.svn.url


class ModifiedError(Exception):
    r"""Raised when attempting to tag or branch a working copy that contains changes."""


class NotOnBranchError(Exception):
    r"""Raised when attempting to delete a working copy that is not on the requested branch."""


class NotOnTagError(Exception):
    r"""Raised when attempting to delete a working copy that is not on the requested tag."""


class Wcopy(object):
    r"""
    A working copy obtained by checking out a *Url*.

    """
    def __init__(self, dir_, url=None, username="", password=""):
        r"""
        Initialize attributes.
        
        If *url* is not None, perform a checkout, otherwise check that *dir\_* points to a valid
        working copy.
        
        """
        self.dir = dir_
        self.username = username
        self.password = password
        self.svn = nxpy.svn.svn.Svn()
        if url:
            self.svn.checkout(url, self.dir, ignore_externals=False)
            self.url = url
        else:
            self.url = nxpy.svn.url.Url(self.svn.info(self.dir).url)

    def __str__(self):
        return self.dir

    def commit(self):
        self.svn.commit(self.dir, username=self.username, password=self.password)

    def update(self, ignore_externals=False):
        self.svn.update(self.dir, ignore_externals=ignore_externals)

    # If 'url' exists do nothing, otherwise copy the working copy
    def _copy(self, url):
        info = None
        try:
            info = self.svn.info(url)
        except nxpy.command.command.Error:
            pass
        if not info:
            if self.svn.status(self.dir):
                raise ModifiedError(self.dir)
            self.svn.copy(self.dir, url, username=self.username, password=self.password)
        
    def branch(self, label):
        if self.url.isbranch(label):
            return None
        else:
            u = self.url.getbranch(label)
            self._copy(u)
            return u

    def delete_branch(self, label):
        if not self.url.isbranch(label):
            raise NotOnBranchError(self.dir)
        self.svn.delete(self.url, username=self.username, password=self.password)
        self.url = None
        
    def tag(self, label):
        if self.url.istag(label):
            return None
        else:
            u = self.url.gettag(label)
            self._copy(u)
            return u

    def delete_tag(self, label):
        if not self.url.istag(label):
            raise NotOnTagError(self.dir)
        self.svn.delete(self.url, username=self.username, password=self.password)
        self.url = None

    def delete_path(self, path, keep_local=False):
        path = os.path.join(self.dir, path)
        self.svn.delete(path, keep_local=keep_local)

    def getexternals(self):
        return self.svn.getexternals(self.dir)
    
    def setexternals(self, ext):
        self.svn.setexternals(ext, self.dir, username=self.username, password=self.password)
        self.update(False)
        self.commit()
        self.update(False)

    def getignore(self):
        return self.svn.getignore(self.dir)
    
    def setignore(self, ign):
        self.svn.setignore(ign, self.dir, username=self.username, password=self.password)
        self.update(False)
        self.commit()
        self.update(False)
