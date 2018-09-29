# nxpy_temp_file --------------------------------------------------------------

# Copyright Nicola Musatti 2014 - 2018
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See https://github.com/nmusatti/nxpy/tree/master/libs/temp_file. ------------

r"""

"""

# Python 2.5 compatibility
from __future__ import with_statement    
from __future__ import absolute_import

import os
import os.path

import nxpy.core.temp_file
import nxpy.test.test


class TempFileTest(nxpy.test.test.TestCase):
    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_6)
    def testTempFile(self):
        with nxpy.core.temp_file.TempFile() as f:
            f.close()
            self.assertTrue(os.access(f.name, os.F_OK))
        self.assertFalse(os.access(f.name, os.F_OK))
    
    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_6)
    def testTempDir(self):
        with nxpy.core.temp_file.TempDir() as d:
            n = os.path.join(d.name, "a")
            f = open(n,"w+")
            f.close()
            self.assertTrue(os.access(n, os.F_OK))
        self.assertFalse(os.access(n, os.F_OK))
