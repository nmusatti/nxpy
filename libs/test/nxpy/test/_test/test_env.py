# nxpy.test package ----------------------------------------------------------

# Copyright Nicola Musatti 2011 - 2014
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See http://nxpy.sourceforge.net for library home page. ---------------------

# Python 2.5 compatibility
from __future__ import with_statement    
from __future__ import absolute_import

import logging
import os
import sys

import nxpy.core.temp_file
import nxpy.svn.svn
import nxpy.test.env
import nxpy.test.test

_log = logging.getLogger(__name__)

try:
    import setup_test_env
except ImportError:
    pass

logging.basicConfig(stream=sys.__stderr__, level=logging.INFO)

class EnvTest(nxpy.test.test.TestCase):
    @nxpy.test.test.skip("When this test is run first it breaks many other tests")
    def test_pass(self):
        if "setup_test_env" not in sys.modules:
            self.skipTest("Could not import setup_test_env.py")
        with nxpy.core.temp_file.TempDir(prefix="test_env_") as dir_:
            os.environ["NXPY_TEST_DIR"] = dir_.name
            setup_test_env.main()
            env = nxpy.test.env.Env("maven")
            self.assertTrue(os.path.isdir(env.backup))
            self.assertTrue(os.path.isdir(env.wcopy))
            svn = nxpy.svn.svn.Svn()
            self.assertTrue(svn.info(os.path.join(env.wcopy, "aggregator")))
            self.assertTrue(svn.info(env.repo))
