# nxpy_svn --------------------------------------------------------------------

# Copyright Nicola Musatti 2012 - 2018
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See https://github.com/nmusatti/nxpy/tree/master/libs/svn. ------------------

r"""
Tests for the wcopy module

"""

# Python 2.5 compatibility
from __future__ import with_statement    
from __future__ import absolute_import

import getpass
import logging
import os
import os.path
import sys

import nxpy.core.temp_file
import nxpy.svn.wcopy
import nxpy.test.env
import nxpy.test.test


logging.basicConfig(stream=sys.__stderr__, level=logging.INFO)


class WcopyTest(nxpy.test.test.TestCase):
    def setUp(self):
        self.env = nxpy.test.env.get_env(self, "maven")
        if self.env:
            self.dir = os.path.join(self.env.wcopy, "aggregator")

    def test_check_out(self):
        with nxpy.core.temp_file.TempDir(prefix="test_wcopy_") as d:
            path = os.path.join(d.name, "first")
            u = self.env.repo + "/first/trunk"
            wcopy = nxpy.svn.wcopy.Wcopy(path, u, username=getpass.getuser())
            self.assertEqual(u.lower(), wcopy.url.lower())

    def test_delete_path(self):
        with nxpy.core.temp_file.TempDir(prefix="test_wcopy_") as d:
            path = os.path.join(d.name, "first")
            u = self.env.repo + "/first/trunk"
            wcopy = nxpy.svn.wcopy.Wcopy(path, u, username=getpass.getuser())
            d = os.path.join("src", "main", "java", "owf", "test", "first")
            f = "First.java"
            wcopy.delete_path(os.path.join(d, f))
            l = os.listdir(os.path.join(wcopy.dir, d))
            self.assertTrue(f not in l)
