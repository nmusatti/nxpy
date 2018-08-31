# nxpy.svn package -----------------------------------------------------------

# Copyright Nicola Musatti 2010 - 2014
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See http://nxpy.sourceforge.net for library home page. ---------------------

r"""
test_svnadmin.py - tests for the svnadmin module
"""

# Python 2.5 compatibility
from __future__ import with_statement    
from __future__ import absolute_import

import os.path

import nxpy.core.temp_file
import nxpy.svn.svnadmin
import nxpy.svn.svn
import nxpy.test.test


class SvnAdminTest(nxpy.test.test.TestCase):
    def test_pass(self):
        with nxpy.core.temp_file.TempDir(prefix="test_svnadmin_") as d:
            path = os.path.join(d.name, "repo")
            nxpy.svn.svnadmin.SvnAdmin().create(path)
            url = "file:///" + path.replace(os.sep, "/").lstrip("/")
            info = nxpy.svn.svn.Svn().info(url)
            self.assertEqual(url.lower(), info.url.lower())
