# nxpy_sort -------------------------------------------------------------------

# Copyright Nicola Musatti 2010 - 2018
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See https://github.com/nmusatti/nxpy/tree/master/libs/sort. -----------------

r"""
Tests for the *sort* module.

"""

from __future__ import absolute_import

import nxpy.core.sort
import nxpy.test.test


class SortTest(nxpy.test.test.TestCase):
    def test_topological_sort_pass(self):
        pairs = ( ("s", "a"), ("o1", "o"), ("o2", "o"), ("o", "s"), ("s1", "s"), ("s2", "s"),
                  ("a1", "a"), ("a2","a"), ("a", "t") )
        res = nxpy.core.sort.topological_sort(pairs)
        self.assertEqual("t", res[0])
        