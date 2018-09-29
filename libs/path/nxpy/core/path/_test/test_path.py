# nxpy_path -------------------------------------------------------------------

# Copyright Nicola Musatti 2014 - 2018
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See https://github.com/nmusatti/nxpy/tree/master/libs/path. -----------------

r"""
Tests for the path module.

"""

# Python 2.5 compatibility
from __future__ import with_statement    
from __future__ import absolute_import

import os
import os.path
import stat

import nxpy.core.path
import nxpy.core.temp_file
import nxpy.test.test


class PathTest(nxpy.test.test.TestCase):
    def testBlasttreePass(self):
        with nxpy.core.temp_file.TempDir() as td:
            d = os.path.join(td.name, "a")
            os.mkdir(d)
            fp = os.path.join(d, "b")
            with open(fp, "w+") as f:
                f.write("abcd")
            os.chmod(fp, stat.S_IREAD)
            nxpy.core.path.blasttree(d)
            self.assertFalse(os.access(d, os.F_OK))

    def testCurrentDirectory(self):
        with nxpy.core.temp_file.TempDir() as td:
            d = os.path.join(os.path.realpath(td.name), "a")
            os.mkdir(d)
            wd = os.getcwd()
            with nxpy.core.path.CurrentDirectory(d) as cd:
                self.assertEqual(cd._prev, wd)
                self.assertEqual(cd.current, os.getcwd())
                self.assertEqual(cd.current, cd._path)
            self.assertEqual(wd, os.getcwd())
