# nxpy.maven package ---------------------------------------------------------

# Copyright Nicola Musatti 2010 - 2017
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See http://nxpy.sourceforge.net for library home page. ---------------------

r"""
Manipulation of Maven POM files.

"""

from __future__ import absolute_import

import collections
import os.path

import lxml.etree

import nxpy.xml.util
import nxpy.maven.artifact


_ns = nxpy.xml.util.Namespace("http://maven.apache.org/POM/4.0.0")


class BadPomFileError(EnvironmentError):
    pass


class ArtifactAlreadyPresentError(ValueError):
    pass


class MissingArtifactError(ValueError):
    pass


class ModuleAlreadyPresentError(ValueError):
    pass


class MissingModuleError(ValueError):
    pass


class DependencyIterator(collections.Iterator):
    def __init__(self, deps):
        self.iter = iter(deps.dependencies)

    def __next__(self):
        return next(self.iter)[1]


class Dependencies(object):
    def __init__(self, element):
        self.element = element
        self._modified = False
        self.dependencies = []
        if self.element is not None:
            i = 0
            for d in element.getchildren():
                if d.tag is not lxml.etree.Comment:
                    a = nxpy.maven.artifact.Artifact(d)
                    self.dependencies.append([i, a])
                i += 1

    def _saved(self):
        self._modified = False
        for a in self.dependencies:
            a[1]._modified = False

    @property
    def modified(self):
        return self._modified or any([ a[1]._modified for a in self.dependencies ])
    
    def contains(self, artifact):
        if isinstance(artifact, nxpy.maven.artifact.Artifact):
            group_id = artifact.groupId
            artifact_id = artifact.artifactId
        else:
            group_id, artifact_id = artifact.split(":")[0:2]
        for a in self.dependencies:
            if a[1].groupId == group_id and a[1].artifactId == artifact_id:
                return a[1]
        return None
    
    def add(self, artifact):
        if self.contains(artifact):
            raise ArtifactAlreadyPresentError()
        d = _ns.Element("dependency")
        d.text = self.element.text + "    "
        d.tail = self.element.tail + "    "
        gi = _ns.SubElement(d,"groupId")
        gi.text = artifact.groupId
        gi.tail = d.text
        ai = _ns.SubElement(d,"artifactId")
        ai.text = artifact.artifactId
        ai.tail = d.text
        v = _ns.SubElement(d,"version")
        v.text = artifact.version
        if artifact.packaging != "jar":
            v.tail = d.text
            p = _ns.SubElement(d,"type")
            p.text = artifact.packaging
            p.tail = d.tail + "    "
        else:
            v.tail = d.tail + "    "            
        art = nxpy.maven.artifact.Artifact(d)
        art._modified = True
        index = 0
        for i in range(0, len(self.dependencies) -1):
            if index == 0:
                if self.dependencies[i][1] > art:
                    index = i
            else:
                self.dependencies[i][0] += 1
        if index < len(self.dependencies):
            d.tail += "    "
        else:
            self.element[self.dependencies[index-1][0]].tail += "    "
        self.element.insert(self.dependencies[index][0], d)
        self.dependencies.insert(index, [self.dependencies[index][0], art])

    def remove(self, artifact):
        if not self.contains(artifact):
            raise MissingArtifactError()
        index = -1
        for i in range(0, len(self.dependencies) -1):
            if index == -1:
                if ( self.dependencies[i][1].artifactId == artifact.artifactId and 
                        self.dependencies[i][1].groupId == artifact.groupId ):
                    index = i
            else:
                self.dependencies[i][0] -= 1
        if index == -1:
            raise MissingArtifactError()
        if self.dependencies[index][0] == len(self.element) - 1:
            self.element[self.dependencies[index][0] -1].tail = self.element[self.dependencies[index][1]].tail
        del self.element[self.dependencies[index][0]]
        del self.dependencies[index]
        self._modified = True

    def __str__(self):
        return "\n".join([ str(a) for a in self.dependencies ])

    def __iter__(self):
        return DependencyIterator(self)


class Modules(nxpy.xml.util.SequenceElement):
    """
    Map a POM's modules element to a mutable sequence.
    
    Supports addition and removal of modules by name.
    """
    def __init__(self, root):
        super(Modules, self).__init__(root, "modules", "module", _ns.url)

    def _saved(self):
        self.modified = False

    def contains(self, module):
        return module in self

    def add(self, module):
        if self.contains(module):
            raise ModuleAlreadyPresentError()
        i = 0
        for m in self:
            if m > module:
                break
            i += 1
        self.insert(i, module)

    def remove(self, module):
        i = 0
        for m in self:
            if m == module:
                break
            i += 1
        if i == len(self):
            raise MissingModuleError()
        del self[i]


class Scm(object):
    def __init__(self, element):
        self._modified = False
        self.element = element
        self._connection = _ns.find(element, "connection")
        self._developerConnection = _ns.find(element, "developerConnection")
        self._url = _ns.find(element, "url")

    connection = nxpy.xml.util.make_property("_connection")
    developerConnection = nxpy.xml.util.make_property("_developerConnection")
    url = nxpy.xml.util.make_property("_url")

    @property
    def modified(self):
        return self._modified


class Repository(object):
    def __init__(self, element):
        self._modified = False
        self.element = element
        self._id = _ns.find(element, "id")
        self._name = _ns.find(element, "name")
        self._url = _ns.find(element, "url")

    id = nxpy.xml.util.make_property("_id")
    name = nxpy.xml.util.make_property("_name")
    url = nxpy.xml.util.make_property("_url")

    @property
    def modified(self):
        return self._modified


class DistributionManagement(object):
    def __init__(self, element):
        self.element = element
        self.repository = Repository(_ns.find(element, "repository"))
        self.snapshotRepository = Repository(_ns.find(element, "snapshotRepository"))

    def _saved(self):
        self.repository._modified = False
        self.snapshotRepository._modified = False

    @property
    def modified(self):
        return self.repository.modified or self.snapshotRepository.modified


class Properties(nxpy.xml.util.MappingElement):
    def __init__(self, parent):
        super(Properties, self).__init__(parent, "properties", _ns.url)
        
    
class Pom(object):
    _root = ( r'<project xmlns="http://maven.apache.org/POM/4.0.0"'
              r' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n' 
              r'    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0' 
              r' http://maven.apache.org/maven-v4_0_0.xsd">' )

    def __init__(self, path):
        self.path = os.path.realpath(path)
        self.dir = os.path.split(self.path)[0]
        try:
            self.tree = nxpy.xml.util.parse(path)
        except IOError:
            raise BadPomFileError(path)
        self.root = self.tree.getroot()
        self.artifact = nxpy.maven.artifact.Artifact(self.root)
        self.dependencies = Dependencies(_ns.find(self.root, "dependencies"))
        parent = _ns.find(self.root, "parent")
        try:
            self.parent = nxpy.maven.artifact.Artifact(parent)
        except ( AttributeError, TypeError ):
            self.parent = None
        self.scm = None
        scm = _ns.find(self.root, "scm")
        if scm  is not None:
            self.scm = Scm(scm)
        self.modules = Modules(self.root)
        depmgmt = None
        if self.artifact.packaging == "pom":
            deps = _ns.find(self.root, "dependencyManagement")
            if deps is not None:
                depmgmt = _ns.find(deps, "dependencies")
        self.dependencyManagement = Dependencies(depmgmt)
        self.properties = Properties(self.root)
        self.assembly_descriptor = None
        build = _ns.find(self.root, "build")
        if build is not None:
            plugins = _ns.find(build, "plugins")
            if plugins is not None:
                for p in plugins.getchildren():
                    if _ns.find(p, "artifactId").text == "maven-assembly-plugin":
                        ad = _ns.find(_ns.find(p, "configuration"), "descriptors")[0]
                        self.assembly_descriptor = os.path.normpath(os.path.join(self.dir, 
                                ad.text))
                        break
        self.distributionManagement = None
        dm = _ns.find(self.root, "distributionManagement")
        if dm is not None:
            self.distributionManagement = DistributionManagement(dm)
        self._writer = nxpy.xml.util.Writer(self._root, None, 4)

    def qualified_name(self, full=False):
        return self.artifact.qualified_name(full)

    @property
    def modified(self):
        return ( self.artifact.modified or ( self.parent and self.parent.modified ) or
                 self.modules.modified or self.dependencies.modified or 
                 self.dependencyManagement.modified or ( self.scm and self.scm.modified ) or 
                 self.properties.modified or 
                 ( self.distributionManagement and self.distributionManagement.modified ) )

    def write(self, where):
        if not where:
            where = self.path
        self._writer.write(self.root, where)

    def save(self):
        if self.modified:
            self.write(None)
            self.artifact._modified = False
            if self.parent:
                self.parent._modified = False
            self.scm._modified = False
            self.dependencies._saved()
            self.dependencyManagement._saved()
            self.distributionManagement._saved()
            self.modules._saved()
            self.properties.modified = False
            return True
        return False
