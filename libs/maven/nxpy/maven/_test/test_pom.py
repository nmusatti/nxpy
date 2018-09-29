# nxpy_maven ------------------------------------------------------------------

# Copyright Nicola Musatti 2010 - 2018
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See https://github.com/nmusatti/nxpy/tree/master/libs/maven. ----------------

r"""
Tests for the pom module

"""

# Python 2.5 compatibility
from __future__ import with_statement    
from __future__ import absolute_import

import os.path
import shutil

import nxpy.core.file
import nxpy.core.temp_file
import nxpy.core.past
import nxpy.test.env
import nxpy.test.test
import nxpy.xml.util

if nxpy.core.past.V_2_7.at_least():
    import nxpy.maven.pom


class PomTestBase(nxpy.test.test.TestCase):
    def setUp(self):
        self.env = nxpy.test.env.get_env(self, "maven")
        self.dir = os.path.join(self.env.wcopy, "aggregator")
        self.pom = nxpy.maven.pom.Pom(os.path.join(self.dir, "first", "pom.xml"))


class ArtifactTest(PomTestBase):
    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_7)
    def test_modified_pass(self):
        self.pom.artifact.artifactId = "pippo"
        self.assertTrue(self.pom.artifact.modified)


class DependenciesTest(PomTestBase):
    def setUp(self):
        super(DependenciesTest, self).setUp()
        self.dep_pom = nxpy.maven.pom.Pom(os.path.join(self.dir, "test-dep", "pom.xml"))

    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_7)
    def test_contains_pass(self):
        deps = self.dep_pom.dependencyManagement
        self.assertTrue(deps.contains(self.pom.artifact))
        self.assertTrue(deps.contains(self.pom.artifact.qualified_name(True)))
        self.assertTrue(deps.contains(self.pom.artifact.qualified_name(False)))

    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_7)
    def test_contains_fail(self):
        deps = self.dep_pom.dependencies
        self.assertFalse(deps.contains(self.pom.artifact))
        self.assertFalse(deps.contains(self.pom.artifact.qualified_name(True)))
        self.assertFalse(deps.contains(self.pom.artifact.qualified_name(False)))

    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_7)
    def test_modified_pass(self):
        deps = self.dep_pom.dependencyManagement
        a = deps.contains(self.pom.artifact)
        a.groupId = "pluto"
        self.assertTrue(deps.modified)

    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_7)
    def test_add_pass(self):
        deps = self.dep_pom.dependencyManagement
        pom = nxpy.maven.pom.Pom(os.path.join(self.dir, "third", "pom.xml"))
        self.assertFalse(deps.contains(pom.artifact))
        deps.add(pom.artifact)
        self.assertTrue(deps.modified)
        self.assertTrue(deps.contains(pom.artifact))

    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_7)
    def test_add_fail(self):
        deps = self.dep_pom.dependencyManagement
        pom = nxpy.maven.pom.Pom(os.path.join(self.dir, "second", "pom.xml"))
        self.assertRaises(nxpy.maven.pom.ArtifactAlreadyPresentError, deps.add, pom.artifact)

    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_7)
    def test_add_nonjar_pass(self):
        deps = self.dep_pom.dependencyManagement
        pom = nxpy.maven.pom.Pom(os.path.join(self.dir, "webapp2", "pom.xml"))
        self.assertFalse(deps.contains(pom.artifact))
        deps.add(pom.artifact)
        ns = nxpy.xml.util.Namespace("http://maven.apache.org/POM/4.0.0")
        found = False
        for d in deps.element.getchildren():
            for e in d.getchildren():
                tag = ns.get_tag(e)
                if tag == "artifactId":
                    if e.text == "webapp2":
                        found = True
                    elif found:
                        self.fail("Packaging should be 'war'")
                elif found and tag == "type":
                    self.assertEqual(e.text, "war")
                    break
            if found:
                break
        self.assertTrue(deps.modified)
        self.assertTrue(deps.contains(pom.artifact))

    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_7)
    def test_remove_pass(self):
        deps = self.dep_pom.dependencyManagement
        pom = nxpy.maven.pom.Pom(os.path.join(self.dir, "second", "pom.xml"))
        deps.remove(pom.artifact)
        self.assertTrue(deps.modified)
        self.assertFalse(deps.contains(pom.artifact))

    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_7)
    def test_remove_fail(self):
        deps = self.dep_pom.dependencyManagement
        pom = nxpy.maven.pom.Pom(os.path.join(self.dir, "third", "pom.xml"))
        self.assertFalse(deps.contains(pom.artifact))
        self.assertRaises(nxpy.maven.pom.MissingArtifactError, deps.remove, pom.artifact)


class DistributionManagementTest(PomTestBase):
    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_7)
    def test_structure_pass(self):
        dm = self.pom.distributionManagement
        self.assertTrue(dm.repository is not None)
        self.assertEqual(dm.repository.id, "releases")
        self.assertTrue(dm.snapshotRepository is not None)
        self.assertEqual(dm.snapshotRepository.id, "snapshots")


class PropertiesTest(PomTestBase):
    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_7)
    def test_add_pass(self):
        with nxpy.core.temp_file.TempDir(prefix="test_pom_") as dir_:
            shutil.copy(os.path.join(self.pom.dir, "pom.xml"), dir_.name)
            p = nxpy.maven.pom.Pom(os.path.join(dir_.name, "pom.xml"))
            self.assertRaises(KeyError, p.properties.__getitem__, "owf.arch.patch-project")
            p.properties["owf.arch.patch-project"] = "opm-patch"
            self.assertTrue(p.modified)
            self.assertEqual(p.properties["owf.arch.patch-project"], "opm-patch")
            p.save()
            self.assertFalse(p.modified)


class PomTest(PomTestBase):
    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_7)
    def test_modified_pass(self):
        self.pom.artifact.groupId = "pluto"
        self.assertTrue(self.pom.modified)

    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_7)
    def test_write_pass(self):
        with nxpy.core.temp_file.TempFile(mode="w+", prefix="test_pom_") as f:
            self.pom.write(f)
            self.assertTrue(nxpy.core.file.compare(os.path.join(self.pom.dir, "pom.xml"), f.name))

    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_7)
    def test_save_pass(self):
        with nxpy.core.temp_file.TempDir(prefix="test_pom_") as dir_:
            shutil.copy(os.path.join(self.pom.dir, "pom.xml"), dir_.name)
            p = nxpy.maven.pom.Pom(os.path.join(dir_.name, "pom.xml"))
            p.artifact.version = "0.0.1-SNAPSHOT"
            self.assertTrue(p.modified)
            p.save()
            self.assertFalse(p.modified)

    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_7)
    def test_assembly_descriptor_pass(self):
        p = nxpy.maven.pom.Pom(os.path.join(self.dir, "patch", "pom.xml"))
        self.assertTrue(p.assembly_descriptor is not None)

    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_7)
    def test_module_pass(self):
        pom = nxpy.maven.pom.Pom(os.path.join(self.dir, "pom.xml"))
        self.assertTrue(pom.modules.contains("second"))

    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_7)
    def test_add_module_pass(self):
        pom = nxpy.maven.pom.Pom(os.path.join(self.dir, "pom.xml"))
        module = "third"
        pom.modules.add(module)
        self.assertTrue(pom.modified)
        self.assertTrue(pom.modules.contains(module))

    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_7)
    def test_remove_module_pass(self):
        pom = nxpy.maven.pom.Pom(os.path.join(self.dir, "pom.xml"))
        module = "second"
        pom.modules.remove(module)
        self.assertTrue(pom.modified)
        self.assertFalse(pom.modules.contains(module))
