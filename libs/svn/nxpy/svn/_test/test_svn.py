# nxpy_svn --------------------------------------------------------------------

# Copyright Nicola Musatti 2010 - 2021
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See https://github.com/nmusatti/nxpy/tree/master/libs/svn. ------------------

r"""
Tests for the svn module

"""

# Python 2.5 compatibility
from __future__ import with_statement    
from __future__ import absolute_import

import getpass
import logging
import os.path
import sys

import nxpy.core.past
import nxpy.core.temp_file
import nxpy.svn.svn
import nxpy.svn.svnadmin
import nxpy.svn.url
import nxpy.command.command
import nxpy.test.env
import nxpy.test.test


logging.basicConfig(stream=sys.__stderr__, level=logging.INFO)


class SvnTest(nxpy.test.test.TestCase):
    def setUp(self):
        self.env = nxpy.test.env.get_env(self, "maven")
        self.svn = nxpy.svn.svn.Svn()
        if self.env:
            self.dir = os.path.join(self.env.wcopy, "aggregator")

    def test_version_pass(self):
        version = self.svn.version()
        self.assertTrue(version[0] == 1 and version[1] in ( 6, 7, 8, 9, 10, 11, 12, 13 ))

    def test_info_pass(self):
        info = self.svn.info(self.dir)
        self.assertEqual(self.dir, info.path)

    def test_status_pass(self):
        self.assertFalse(self.svn.status(self.dir))

    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_6)
    def test_checkout(self):
        with nxpy.core.temp_file.TempDir(prefix="test_svn_") as d:
            path = os.path.join(d.name, "first")
            u = self.env.repo + "/first/trunk"
            self.svn.checkout(u, path)
            info = self.svn.info(path)
            self.assertEqual(u.lower(), info.url.lower())

    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_6)
    def test_import_pass(self):
        with nxpy.core.temp_file.TempDir(prefix="test_svn_") as d:
            repo = os.path.join(d.name, "repo")
            u = nxpy.svn.svnadmin.SvnAdmin().create(repo)
            path = os.path.join(self.env.backup, "first")
            u += "/first"
            self.svn.import_(path, u, username=getpass.getuser())
            info = self.svn.info(u)
            self.assertEqual(u.lower(), info.url.lower())

    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_6)
    def test_export_pass(self):
        with nxpy.core.temp_file.TempDir(prefix="test_svn_") as d:
            repo = os.path.join(d.name, "repo")
            u = nxpy.svn.svnadmin.SvnAdmin().create(repo)
            path = os.path.join(self.env.backup, "first")
            u += "/first"
            self.svn.import_(path, u, username=getpass.getuser())
            exp = os.path.join(d.name, "export")
            self.svn.export(u + "/trunk", exp)
            pom = os.path.join(exp, "pom.xml")
            self.assertTrue(os.access(pom, os.R_OK))
            f = open(pom, "r").read()
            self.assertNotEqual(f.find("0.0.1-SNAPSHOT"), -1)
            
    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_6)
    def test_copy_pass(self):
        with nxpy.core.temp_file.TempDir(prefix="test_svn_") as d:
            repo = os.path.join(d.name, "repo")
            u = nxpy.svn.svnadmin.SvnAdmin().create(repo)
            path = os.path.join(self.env.backup, "first")
            u += "/first"
            self.svn.import_(path, u)
            self.svn.mkdir(u + "/tags", u + "/branches")
            trunk = u + "/trunk"
            branch = u + "/branches/BRANCH"
            self.svn.copy(trunk, branch)
            tu = nxpy.svn.url.Url(trunk)
            bu = tu.getbranch("BRANCH")
            info = self.svn.info(branch)
            self.assertEqual(str(bu).lower(), info.url.lower())

    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_6)
    def test_move_pass(self):
        with nxpy.core.temp_file.TempDir(prefix="test_svn_") as d:
            repo = os.path.join(d.name, "repo")
            u = nxpy.svn.svnadmin.SvnAdmin().create(repo)
            path = os.path.join(self.env.backup, "first")
            u += "/first"
            self.svn.import_(path, u)
            self.svn.mkdir(u + "/tags", u + "/branches")
            trunk = u + "/trunk"
            branch = u + "/branches/BRANCH"
            branch2 = u + "/branches/BRANCH2"
            self.svn.copy(trunk, branch)
            self.svn.move(branch, branch2)
            tu = nxpy.svn.url.Url(trunk)
            try:
                info = self.svn.info(branch)
                self.fail("Should have raised 'nxpy.command.command.Error'")
            except nxpy.command.command.Error:
                pass
            bu2 = tu.getbranch("BRANCH2")
            info2 = self.svn.info(branch2)
            self.assertEqual(str(bu2).lower(), info2.url.lower())

    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_6)
    def test_delete_pass(self):
        with nxpy.core.temp_file.TempDir(prefix="test_svn_") as d:
            repo = os.path.join(d.name, "repo")
            u = nxpy.svn.svnadmin.SvnAdmin().create(repo)
            path = os.path.join(self.env.backup, "first")
            u += "/first"
            self.svn.import_(path, u)
            self.svn.delete(u)
            self.assertRaises(nxpy.command.command.Error, self.svn.info, u)            

    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_6)
    def test_delete_path_pass(self):
        with nxpy.core.temp_file.TempDir(prefix="test_svn_") as d:
            repo = os.path.join(d.name, "repo")
            u = nxpy.svn.svnadmin.SvnAdmin().create(repo)
            path = os.path.join(self.env.backup, "first")
            u += "/first"
            self.svn.import_(path, u)
            u += "/trunk"
            wc = os.path.join(d.name, "first")
            self.svn.checkout(u, wc)
            s = os.path.join(wc, "src")
            self.svn.delete(s)
            self.svn.commit(wc)
            self.assertRaises(nxpy.command.command.Error, self.svn.info, u + "/src")            

    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_6)
    def test_externals_pass(self):
        with nxpy.core.temp_file.TempDir(prefix="test_svn_") as d:
            repo = os.path.join(d.name, "repo")
            u = nxpy.svn.svnadmin.SvnAdmin().create(repo)
            fbackup = os.path.join(self.env.backup, "first")
            furl = u + "/first"
            self.svn.import_(fbackup, furl)
            self.svn.mkdir(furl + "/tags", furl + "/branches")
            abackup = os.path.join(self.env.backup, "aggregator")
            aurl = u + "/aggregator"
            apath = os.path.join(d.name, "aggregator")
            fpath = os.path.join(apath, "first")
            self.svn.import_(abackup, aurl)
            self.svn.mkdir(aurl + "/tags", aurl + "/branches")
            self.svn.checkout(aurl + "/trunk", apath)
            self.svn.setexternals({ "first" : furl + "/trunk" }, apath)
            self.svn.update(apath, ignore_externals=False)
            info = self.svn.info(fpath)
            self.assertEqual((furl + "/trunk").lower(), info.url.lower())
            ext = self.svn.getexternals(apath)
            self.assertEqual(ext["first"], furl + "/trunk")            

    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_6)
    def test_ignore_pass(self):
        with nxpy.core.temp_file.TempDir(prefix="test_svn_") as d:
            repo = os.path.join(d.name, "repo")
            u = nxpy.svn.svnadmin.SvnAdmin().create(repo)
            fbackup = os.path.join(self.env.backup, "first")
            furl = u + "/first"
            self.svn.import_(fbackup, furl)
            self.svn.mkdir(furl + "/tags", furl + "/branches")
            fpath = os.path.join(d.name, "first")
            self.svn.checkout(furl + "/trunk", fpath)
            self.svn.setignore(( "test", ), fpath)
            tpath = os.path.join(fpath, "test")
            with open(tpath, "w"):
                pass
            #self.svn.commit(fpath)
            status = self.svn.status(fpath, quiet=False, ignore=False)
            nd = os.path.normcase(tpath)
            v = ' '
            for s in status:
                if os.path.normcase(s.item) == nd:
                    v = s.state
                    break
            self.assertEqual(v, 'I')

    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_6)
    def test_diff(self):
        with nxpy.core.temp_file.TempDir(prefix="test_svn_") as d:
            repo = os.path.join(d.name, "repo")
            u = nxpy.svn.svnadmin.SvnAdmin().create(repo)
            path = os.path.join(self.env.backup, "first")
            u += "/first"
            trunk = u + "/trunk"
            self.svn.import_(path, u)
            wcopy = os.path.join(d.name, "wcopy")
            self.svn.checkout(trunk, wcopy)
            pom = os.path.join(wcopy, "pom.xml")
            with open(pom, "a") as f:
                f.write("--- This is a new line ---\n")
            out = self.svn.diff(wcopy)
            self.assertTrue(out != "")
            self.svn.commit(pom)
            out = self.svn.diff(trunk + "@1", trunk + "@2", summarize=True)
            self.assertTrue(out != "")
