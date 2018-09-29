# nxpy_past -------------------------------------------------------------------

# Copyright Nicola Musatti 2014 - 2018
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See https://github.com/nmusatti/nxpy/tree/master/libs/past. -----------------

r"""
Tests for the past module.

"""

from __future__ import absolute_import

import sys

import nxpy.core.past
import nxpy.test.test


class PastTest(nxpy.test.test.TestCase):
    def test_pass(self):
        v = nxpy.core.past.Version(sys.hexversion)
        self.assertTrue(v.at_least())
        self.assertTrue(v.at_most())
        nxpy.core.past.enforce_at_least(v)
        nxpy.core.past.enforce_at_most(v)
