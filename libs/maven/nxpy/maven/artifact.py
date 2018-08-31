# nxpy.maven package ---------------------------------------------------------

# Copyright Nicola Musatti 2010 - 2017
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See http://nxpy.sourceforge.net for library home page. ---------------------

r"""
Maven artifacts.

"""

from __future__ import absolute_import

import functools
import os.path

import nxpy.xml.util


_ns = nxpy.xml.util.Namespace("http://maven.apache.org/POM/4.0.0")


def _trim(s):
    return s.replace("-", "").lower()

@functools.total_ordering
class Artifact(object):
    def __init__(self, element):
        self._modified = False
        self._groupId = _ns.find(element, "groupId")
        self._artifactId = _ns.find(element, "artifactId")
        self._version = _ns.find(element, "version")
        try:
            self._packaging = _ns.find(element, "packaging").text
        except AttributeError:
            try:
                self._packaging = _ns.find(element, "type").text
            except AttributeError:
                self._packaging = None
        if self._packaging is None:
            self._packaging = "jar"
        try:
            self._relativePath = os.path.normpath(_ns.find(element, "relativePath").text)
        except AttributeError:
            self._relativePath = None

    groupId = nxpy.xml.util.make_property("_groupId")
    artifactId = nxpy.xml.util.make_property("_artifactId")
    version = nxpy.xml.util.make_property("_version")
    
    def qualified_name(self, full=False):
        name = self.groupId + ":" + self.artifactId
        if full:
            name += ":" + self.packaging + ":" + self.version
        return name

    def before(self, other):
        return ( ( [ _trim(s) for s in self.groupId.split(".") ], _trim(self.artifactId) ) < 
                ( [ _trim(s) for s in other.groupId.split(".") ], _trim(other.artifactId) ) )
        
    @property
    def modified(self):
        return self._modified

    @property
    def packaging(self):
        return self._packaging
    
    @property
    def relativePath(self):
        return self._relativePath
    
    def __str__(self):
        v = ""
        try:
            v = self.version
        except AttributeError:
            pass
        return "%s:%s:%s" % ( self.groupId, self.artifactId, v )

    def __eq__(self, value):
        return ( ( self.groupId, self.artifactId ) == ( value.groupId, value.artifactId ) )

    def __lt__(self, value):
        return ( ( self.groupId, self.artifactId ) < ( value.groupId, value.artifactId ) )

    def __hash__(self):
        return hash("%s:%s" % ( self.groupId, self.artifactId ))
