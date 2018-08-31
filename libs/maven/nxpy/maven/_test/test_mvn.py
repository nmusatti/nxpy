# nxpy.maven package ----------------------------------------------------------

# Copyright Nicola Musatti 2011 - 2014
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See http://nxpy.sourceforge.net for library home page. ---------------------

r"""
Tests for the mvn module

"""

from __future__ import absolute_import

import os.path

import nxpy.maven.mvn
import nxpy.test.env
import nxpy.test.log
import nxpy.test.test


class MvnTest(nxpy.test.test.TestCase):
    def setUp(self):
        self.env = nxpy.test.env.get_env(self, "maven")
        self.dir = os.path.join(self.env.wcopy, "aggregator")
        self.mvn = nxpy.maven.mvn.Mvn()
        os.chdir(self.dir)
        
    def tearDown(self):
        self.mvn.clean()
        
    def test_package_pass(self):
        self.mvn.package()
