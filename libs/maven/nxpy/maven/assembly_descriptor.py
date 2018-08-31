# nxpy.maven package ---------------------------------------------------------

# Copyright Nicola Musatti 2010 - 2017
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See http://nxpy.sourceforge.net for library home page. ---------------------

r"""
Manipulation of Maven Assembly Plugin Assembly Descriptor files.

"""

from __future__ import absolute_import

import os.path

import nxpy.xml.util


class BadAssemblyDescriptorFileError(EnvironmentError):
    pass


class AssemblyDescriptor(object):
    
    def __init__(self, path):
        self.path = os.path.realpath(path)
        self.dir = os.path.split(self.path)[0]
        try:
            self.tree = nxpy.xml.util.parse(path)
        except IOError:
            raise BadAssemblyDescriptorFileError(path)
        self.root = self.tree.getroot()
        self._ns = nxpy.xml.util.Namespace(element=self.root)

        depset = self._ns.find(self.root, "dependencySets")
        deps = None
        if depset is not None:
            if len(depset) > 0:
                deps = depset[0]
            else:
                deps = self._ns.SubElement(depset, "dependencySet")
        if deps is None:
            raise BadAssemblyDescriptorFileError(path)
        self.includes = nxpy.xml.util.SequenceElement(deps, "includes", "include", self._ns.url)
        self.excludes = nxpy.xml.util.SequenceElement(deps, "excludes", "exclude", self._ns.url)
        self._writer = nxpy.xml.util.Writer(self._make_root_tag(), {}, 4)

    _schema_loc = nxpy.xml.util.QName(
            r"{http://www.w3.org/2001/XMLSchema-instance}schemaLocation")
    
    _root_fmt = ( 
r'''<{0}
    xmlns="{1}"
    xmlns:xsi="{2}"
    xsi:{3}="{4}">'''
        )
    
    def _make_root_tag(self):
        root = nxpy.xml.util.QName(self.root.tag)
        return AssemblyDescriptor._root_fmt.format(root.tag, root.url, 
                AssemblyDescriptor._schema_loc.url, AssemblyDescriptor._schema_loc.tag,
                self.root.get(AssemblyDescriptor._schema_loc.text))
    
    @property
    def modified(self):
        return ( ( self.includes and self.includes.modified ) or 
                 ( self.excludes and self.excludes.modified ) )

    def write(self, where):
        if not where:
            where = self.path
        self._writer.write(self.root, where)

    def save(self):
        if self.modified:
            self.write(None)
            self.includes.modified = False
            self.excludes.modified = False
            return True
        return False
