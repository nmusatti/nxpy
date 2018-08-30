# nxpy.core package ----------------------------------------------------------

# Copyright Nicola Musatti 2014
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See http://nxpy.sourceforge.net for library home page. ---------------------

r"""
Tests for the file module.

"""

# Python 2.5 compatibility
from __future__ import with_statement    
from __future__ import absolute_import

import os.path

import six

import nxpy.core.file
import nxpy.core.past
import nxpy.core.temp_file
import nxpy.test.test


class FileTest(nxpy.test.test.TestCase):
    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_6)
    def testEqual(self):
        with nxpy.core.temp_file.TempFile() as first:
            with nxpy.core.temp_file.TempFile() as second:
                first.write(six.b("abcd\nefg"))
                second.write(six.b("abcd\nefg"))
                first.close()
                second.close()
                self.assertTrue(nxpy.core.file.compare(first.name, second.name))

    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_6)
    def testDifferent(self):
        with nxpy.core.temp_file.TempFile() as first:
            with nxpy.core.temp_file.TempFile() as second:
                first.write(six.b("abcd"))
                second.write(six.b("efgh"))
                first.close()
                second.close()
                self.assertFalse(nxpy.core.file.compare(first.name, second.name))

    def test_open_(self):
        with nxpy.core.temp_file.TempDir() as d:
            with nxpy.core.file.open_(os.path.join(d.name, "f"), "w+", encoding="utf-8") as f:
                orig = six.u("Spicy Jalape\u00f1o")
                s = orig
                if nxpy.core.past.V_2_7.at_most():
                    s = s.encode("utf-8")
                f.write(s)
                f.seek(0)
                s1 = f.read()
                if nxpy.core.past.V_2_7.at_most():
                    s1 = s1.decode("utf-8")
                self.assertEqual(orig, s1)
