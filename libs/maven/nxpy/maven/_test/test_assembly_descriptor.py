# nxpy_maven ------------------------------------------------------------------

# Copyright Nicola Musatti 2010 - 2018
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See https://github.com/nmusatti/nxpy/tree/master/libs/maven. ----------------

r"""
Tests for the assembly_descriptor module

"""

# Python 2.5 compatibility
from __future__ import with_statement    
from __future__ import absolute_import

import os.path
import shutil

import nxpy.core.file
import nxpy.core.past
import nxpy.core.temp_file
import nxpy.test.env
import nxpy.test.test

if nxpy.core.past.V_2_7.at_least():
    import nxpy.maven.assembly_descriptor


class AssemblyDescriptorTest(nxpy.test.test.TestCase):
    def setUp(self):
        self.env = nxpy.test.env.get_env(self, "maven")
        self.dir = os.path.join(self.env.wcopy, "aggregator")
        self.ad = nxpy.maven.assembly_descriptor.AssemblyDescriptor(os.path.join(self.dir, 
                "patch", "src", "main", "assembly", "zip.xml"))

    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_7)
    def test_write_pass(self):
        with nxpy.core.temp_file.TempFile(mode="w+", prefix="test_assembly_descriptor_") as f:
            self.ad.write(f)
            self.assertTrue(nxpy.core.file.compare(os.path.join(self.ad.path), f.name))

    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_7)
    def test_modify_pass(self):
        with nxpy.core.temp_file.TempDir(prefix="test_assembly_descriptor_") as dir_:
            shutil.copy(os.path.join(self.ad.dir, "zip.xml"), dir_.name)
            ad = nxpy.maven.assembly_descriptor.AssemblyDescriptor(os.path.join(dir_.name, 
                    "zip.xml"))
            self.assertRaises(IndexError, ad.includes.__getitem__, 2)
            ad.excludes[0] = "owf.test:first"
            self.assertTrue(ad.modified)
            self.assertEqual(ad.excludes[0], "owf.test:first")
            ad.save()
            self.assertFalse(ad.modified)

    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_7)
    def test_add_pass(self):
        with nxpy.core.temp_file.TempDir(prefix="test_assembly_descriptor_") as dir_:
            shutil.copy(os.path.join(self.ad.dir, "zip.xml"), dir_.name)
            f1 = os.path.join(dir_.name, "zip.xml")
            ad = nxpy.maven.assembly_descriptor.AssemblyDescriptor(f1)
            self.assertRaises(IndexError, ad.includes.__getitem__, 2)
            ad.excludes[0] = "owf.test:first"
            self.assertEqual(ad.excludes[0], "owf.test:first")
            ad.excludes.append("owf.test:second")
            self.assertEqual(ad.excludes[1], "owf.test:second")
            ad.save()
            ad1 = nxpy.maven.assembly_descriptor.AssemblyDescriptor(f1)
            f2 = os.path.join(dir_.name, "zip1.xml")
            ad1.write(f2)
            self.assertTrue(nxpy.core.file.compare(f1, f2))

    _root = ( 
r'''<assembly
    xmlns="http://maven.apache.org/plugins/maven-assembly-plugin/assembly/1.1.2"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/plugins/maven-assembly-plugin/assembly/1.1.2 http://maven.apache.org/plugins/maven-assembly-plugin/assembly/1.1.2 ">'''
    )

    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_7)
    def test_error_schema_1_1_2(self):
        data = nxpy.test.env.get_data(self, "maven")
        ad = nxpy.maven.assembly_descriptor.AssemblyDescriptor(os.path.join(data.data,
                "asm_desc_1_1_2.xml"))
        tag = ad._make_root_tag()
        self.assertEqual(tag, AssemblyDescriptorTest._root)
