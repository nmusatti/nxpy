# nxpy_svn --------------------------------------------------------------------

# Copyright Nicola Musatti 2010 - 2018
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See https://github.com/nmusatti/nxpy/tree/master/libs/svn. ------------------

r"""
Subversion URL manipulation.

"""

from __future__ import absolute_import

from six.moves import urllib


class BadUrlError(EnvironmentError):
    r"""Indicates a malformed URL."""


class Url(object):
    r"""
    A well-formed Subversion repository URL that follows standard svn conventions.
    
    The URL must end in either 'trunk', 'tags/label' or 'branches/label'.
    
    """
    def __init__(self, path):
        url = urllib.parse.urlsplit(path)
        if url is None:
            raise BadUrlError(path)
        self.url = url
        path = url.path.split("/")
        if path[-1] == "trunk":
            self.trunk = True
            self.name = path[-2]
        else:
            self.trunk = False
            self.name = path[-3]
        self.tag = None
        self.branch = None
        if path[-2] == "tags":
            self.tag = path[-1]
            self.branch = None
        if path[-2] == "branches":
            self.branch = path[-1]
        if not self.trunk and not self.tag and not self.branch:
            raise BadUrlError(path)

    def __eq__(self, other):
        return self.url == other.url
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __str__(self):
        return self.url.geturl()

    def _urlreplace(self, old, new):
        return Url(self.url.geturl().replace(old, new))

    def istrunk(self):
        return self.trunk
    
    def istag(self, tag=None):
        return ( not tag and self.tag ) or ( tag and self.tag == tag )
    
    def isbranch(self, branch=None):
        return ( not branch and self.branch ) or ( branch and self.branch == branch )
    
    def gettrunk(self):
        if self.trunk:
            return self
        new = "trunk"
        if self.tag:
            old = "tags/" + self.tag
        elif self.branch:
            old = "branches/" + self.branch
        return self._urlreplace(old, new)

    def gettag(self, tag):
        if self.tag:
            if self.tag == tag:
                return self
            else:
                old = "tags/" + self.tag
        new = "tags/" + tag
        if self.trunk:
            old = "trunk"
        elif self.branch:
            old = "branches/" + self.branch
        return self._urlreplace(old, new)

    def getbranch(self, branch):
        if self.branch:
            if self.branch == branch:
                return self
            else:
                old = "branches/" + self.branch
        new = "branches/" + branch
        if self.trunk:
            old = "trunk"
        elif self.tag:
            old = "tags/" + self.tag
        return self._urlreplace(old, new)
