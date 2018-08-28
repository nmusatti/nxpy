# nxpy.core package ----------------------------------------------------------

# Copyright Nicola Musatti 2008 - 2014
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See http://nxpy.sourceforge.net for library home page. ---------------------

r"""
Tests for the *memo* module.

"""

from __future__ import absolute_import

import nxpy.core.memo
import nxpy.test.test


class A(nxpy.core.memo.Memo):
    def __init__(self, name):
        self.name = name

    @staticmethod
    def _key(name):
        return name


class SubA(A):
    pass


class B(nxpy.core.memo.Memo):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    @staticmethod
    def _key(first, second):
        return first + second


class C(nxpy.core.memo.Memo):
    def __init__(self, name):
        self.name = name

    @staticmethod
    def _key(name):
        return name


class D(nxpy.core.memo.Memo):
    pass


class MemoTest(nxpy.test.test.TestCase):

    def testA(self):
        a = A("a")
        b = A("a")
        c = A("b")
        self.assertEqual(a.name, b.name)
        self.assertEqual(a, b)
        self.assertNotEqual(b.name, c.name)
        self.assertNotEqual(b, c)
        
    def testB(self):
        a = B(2,5)
        b = B(4,3)
        c = B(2,7)
        self.assertEqual(a.first + a.second, b.first + b.second)
        self.assertEqual(a, b)
        self.assertNotEqual(b.first + b.second, c.first + c.second)
        self.assertNotEqual(b, c)

    def test_two_classes_same_key(self):
        a = A("a")
        c = C("a")
        self.assertEqual(a.name, c.name)
        self.assertNotEqual(a, c)

    def test_equal_hashes(self):
        a1 = "a"
        a2 = "a"
        c1 = A
        c2 = A
        self.assertEqual(hash((c1, a1)),hash((c2, a2)))

    def test_different_hashes(self):
        self.assertNotEqual(hash((A, "a")),hash((SubA, "a")))

    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_6)
    def test_abstract_fail(self):
        self.assertRaises(TypeError, D)
