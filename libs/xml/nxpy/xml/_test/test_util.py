# nxpy_xml --------------------------------------------------------------------

# Copyright Nicola Musatti 2017 - 2019
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See https://github.com/nmusatti/nxpy/tree/master/libs/xml. ------------------

r"""
Tests for the util module

"""

import os.path

import lxml.etree

import nxpy.core.file
import nxpy.core.temp_file
import nxpy.test.test
import nxpy.xml.util


class UtilTest(nxpy.test.test.TestCase):
    _root = ( r'<project xmlns="http://maven.apache.org/POM/4.0.0"'
              r' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n' 
              r'    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0' 
              r' http://maven.apache.org/maven-v4_0_0.xsd">' )
    _ns = nxpy.xml.util.Namespace("http://maven.apache.org/POM/4.0.0")

    _dir_levels = 6
    
    def setUp(self):
        self.base_dir = os.path.realpath(__file__)
        for i in range(self._dir_levels):
            self.base_dir = os.path.split(self.base_dir)[0]

    def test_marshal_pass(self):
        base_dir = os.path.realpath(__file__)
        for i in range(self._dir_levels):
            base_dir = os.path.split(base_dir)[0]
        src = os.path.join(base_dir, "test", "backup", "maven", "third", "trunk", "pom.xml")
        tree = nxpy.xml.util.parse(src)
        root = tree.getroot()
        writer = nxpy.xml.util.Writer(self._root, None, 4)
        with nxpy.core.temp_file.TempFile(mode="w+", prefix="test_util_") as dest:
            writer.write(root, dest)
            self.assertTrue(nxpy.core.file.compare(src, dest.name, ignore_eof=True))

    def _round_trip(self, data, change=None):
        with nxpy.core.temp_file.TempDir(prefix="test_util_") as dir_:
            src = os.path.join(dir_.name, "src.xml")
            dest = os.path.join(dir_.name, "dest.xml")
            with open(src, "wb") as f:
                f.write(data)
            writer = nxpy.xml.util.PreservingWriter(src)
            root = nxpy.xml.util.parse(src).getroot()
            if change:
                change(root)
            writer.write(root, dest)
            with open(dest, "rb") as f:
                return f.read()

    def test_preserving_round_trip_pass(self):
        for dirpath, dirnames, filenames in os.walk(os.path.join(self.base_dir, "test", "backup")):
            for n in filenames:
                if n.endswith(".xml"):
                    with open(os.path.join(dirpath, n), "rb") as f:
                        data = f.read()
                    self.assertEqual(self._round_trip(data), data)

    _preserving = ( b'<?xml version="1.0" encoding="ISO-8859-1"?>\r\n'
                    b'<!-- prolog -->\r\n'
                    b'<root xmlns="urn:test"\r\n'
                    b'\ta="1">\r\n'
                    b'\t<empty />\r\n'
                    b'\t<text>caf\xe9</text>\r\n'
                    b'\t<!-- <not-empty/> -->\r\n'
                    b'</root>\r\n'
                    b'\r\n' )

    def test_preserving_pass(self):
        self.assertEqual(self._round_trip(self._preserving), self._preserving)
        data = ( b'\xef\xbb\xbf' + self._preserving.replace(b'ISO-8859-1', b'UTF-8')
                 .replace(b'\xe9', b'\xc3\xa9') )
        self.assertEqual(self._round_trip(data), data)

    def test_preserving_modified_pass(self):
        def change(root):
            ns = nxpy.xml.util.Namespace("urn:test")
            ns.find(root, "text").text = u"th\xe9"
            ns.SubElement(root, "added")
        expected = ( self._preserving.replace(b"caf\xe9", b"th\xe9")
                     .replace(b"</root>", b"<added /></root>") )
        self.assertEqual(self._round_trip(self._preserving, change), expected)

    def test_preserving_changed_root_pass(self):
        def change(root):
            root.set("a", "2")
        result = self._round_trip(self._preserving, change)
        self.assertTrue(b'<root xmlns="urn:test" a="2">\r\n' in result)
        self.assertTrue(result.endswith(b"</root>\r\n\r\n"))

    def test_sequence_element(self):
        path = os.path.join(self.base_dir, "test", "backup", "maven", "aggregator", "trunk", "pom.xml")
        tree = nxpy.xml.util.parse(path)
        root = tree.getroot()
        modules = nxpy.xml.util.SequenceElement(root, "modules", "module", self._ns.url)
        length = len(modules)
        count = 0
        for m in modules.root:
            if m.tag is not lxml.etree.Comment and self._ns.get_tag(m) == "module":
                count += 1
        self.assertEqual(count, length)
        for m in modules:
            self.assertEqual(m.find(" "), -1)

    _mapping = r'''
<parent>
    <root_tag>
        <key1>value1</key1>
        <key2>value2</key2>
    </root_tag>
</parent>
'''
            
    def test_mapping_element(self):
        tree = lxml.etree.fromstring(self._mapping)
        me = nxpy.xml.util.MappingElement(tree, 'root_tag')
        for k in me:
            self.assertTrue(k == 'key1' and me[k] == 'value1' or k == 'key2' and me[k] == 'value2')
