# nxpy_svn --------------------------------------------------------------------

# Copyright Nicola Musatti 2010 - 2018
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See https://github.com/nmusatti/nxpy/tree/master/libs/svn. ------------------

r"""
test_url.py - tests for the url module
"""

from __future__ import absolute_import

import nxpy.svn.url
import nxpy.test.test


trunk_path = "svn://pippo/pluto/paperino/trunk"
tag_path = "svn://pippo/pluto/paperino/tags/TAG"
branch_path = "svn://pippo/pluto/paperino/branches/BRANCH"


class UrlTest(nxpy.test.test.TestCase):
    def test_init_trunk_pass(self):
        u = nxpy.svn.url.Url(trunk_path)
        self.assertTrue(u.istrunk())
        self.assertEqual("paperino", u.name)
        self.assertFalse(u.isbranch())
        self.assertFalse(u.istag())

    def test_init_tag_pass(self):
        u = nxpy.svn.url.Url(tag_path)
        self.assertTrue(u.istag())
        self.assertTrue(u.istag("TAG"))
        self.assertEqual("paperino", u.name)
        self.assertFalse(u.isbranch())
        self.assertFalse(u.istrunk())

    def test_init_branch_pass(self):
        u = nxpy.svn.url.Url(branch_path)
        self.assertTrue(u.isbranch())
        self.assertTrue(u.isbranch("BRANCH"))
        self.assertEqual("paperino", u.name)
        self.assertFalse(u.istag())
        self.assertFalse(u.istrunk())

    def test_init_fail(self):
        self.assertRaises(nxpy.svn.url.BadUrlError, nxpy.svn.url.Url, "url/non/valido")
        self.assertRaises(nxpy.svn.url.BadUrlError, nxpy.svn.url.Url, "file:///C:/Temp")

    def test_gettrunk_trunk_pass(self):
        trunk_url = nxpy.svn.url.Url(trunk_path)
        self.assertEqual(trunk_url, trunk_url.gettrunk())
        
    def test_gettrunk_tag_pass(self):
        tag_url = nxpy.svn.url.Url(tag_path)
        trunk_url = tag_url.gettrunk()
        self.assertTrue(trunk_url.istrunk())
        self.assertEqual(tag_url.name, trunk_url.name)

    def test_gettrunk_branch_pass(self):
        branch_url = nxpy.svn.url.Url(branch_path)
        trunk_url = branch_url.gettrunk()
        self.assertTrue(trunk_url.istrunk())
        self.assertEqual(branch_url.name, trunk_url.name)

    def test_gettag_trunk_pass(self):
        trunk_url = nxpy.svn.url.Url(trunk_path)
        tag_url = trunk_url.gettag("TAG")
        self.assertTrue(tag_url.istag("TAG"))
        self.assertNotEqual(tag_url, trunk_url)
        self.assertEqual(trunk_url.name, tag_url.name)
        
    def test_gettag_tag_pass(self):
        tag_url = nxpy.svn.url.Url(tag_path)
        self.assertEqual(tag_url, tag_url.gettag("TAG"))
        other_url = tag_url.gettag("OTHER")
        self.assertNotEqual(tag_url, other_url)
        self.assertEqual(tag_url.name, other_url.name)

    def test_gettag_branch_pass(self):
        branch_url = nxpy.svn.url.Url(branch_path)
        tag_url = branch_url.gettag("TAG")
        self.assertTrue(tag_url.istag("TAG"))
        self.assertNotEqual(tag_url, branch_url)
        self.assertEqual(branch_url.name, tag_url.name)

    def test_getbranch_trunk_pass(self):
        trunk_url = nxpy.svn.url.Url(trunk_path)
        branch_url = trunk_url.getbranch("BRANCH")
        self.assertTrue(branch_url.isbranch("BRANCH"))
        self.assertNotEqual(branch_url, trunk_url)
        self.assertEqual(trunk_url.name, branch_url.name)
        
    def test_getbranch_tag_pass(self):
        tag_url = nxpy.svn.url.Url(tag_path)
        branch_url = tag_url.getbranch("BRANCH")
        self.assertTrue(branch_url.isbranch("BRANCH"))
        self.assertNotEqual(branch_url, tag_url)
        self.assertEqual(tag_url.name, branch_url.name)

    def test_getbranch_branch_pass(self):
        branch_url = nxpy.svn.url.Url(branch_path)
        self.assertEqual(branch_url, branch_url.getbranch("BRANCH"))
        other_url = branch_url.getbranch("OTHER")
        self.assertNotEqual(branch_url, other_url)
        self.assertEqual(branch_url.name, other_url.name)
