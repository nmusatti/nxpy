# nxpy_sequence ---------------------------------------------------------------

# Copyright Nicola Musatti 2008 - 2018
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See https://github.com/nmusatti/nxpy/tree/master/libs/sequence. -------------

r"""
Tests for the *sequence* module.

"""

from __future__ import absolute_import

import nxpy.core.sequence
import nxpy.test.test

import six

class SequenceTest(nxpy.test.test.TestCase):
    
    def test_makeTupleScalar(self):
        a = 2
        t = nxpy.core.sequence.make_tuple(a)
        self.assertTrue(isinstance(t, tuple))
        self.assertEqual(t, ( 2, ))

    def test_makeTupleString(self):
        a = "abc"
        t = nxpy.core.sequence.make_tuple(a)
        self.assertTrue(isinstance(t, tuple))
        self.assertEqual(t, ( "abc", ))

    def test_makeTupleUnicodeString(self):
        a = six.u("abc")
        t = nxpy.core.sequence.make_tuple(a)
        self.assertTrue(isinstance(t, tuple))
        self.assertEqual(t, ( six.u("abc"), ))

    def test_makeTupleTuple(self):
        a = ( 1, 2, 3 )
        t = nxpy.core.sequence.make_tuple(a)
        self.assertTrue(isinstance(t, tuple))
        self.assertEqual(t, ( 1, 2, 3 ))

    def test_makeTupleDict(self):
        a = { "a" : 1, "b" : 2, "c" : 3 }
        t = nxpy.core.sequence.make_tuple(a)
        self.assertTrue(isinstance(t, tuple))
        self.assertEqual(set(t), set((('a', 1), ('c', 3), ('b', 2))))
