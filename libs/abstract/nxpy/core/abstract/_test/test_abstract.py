# nxpy_abstract ---------------------------------------------------------------

# Copyright Nicola Musatti 2014 - 2018
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See https://github.com/nmusatti/nxpy/tree/master/libs/abstract. -------------

r"""
Tests for the *abstract* module

"""

from __future__ import absolute_import

import nxpy.core.past

# ensures tests are skipped in Python 2.5 rather than cause an error
if nxpy.core.past.V_2_6.at_least():
    import abc
else:
    class abc(object):
        class ABCMeta(type):
            def __new__(mcs, name, bases, dict):
                return type.__new__(mcs, name, bases, dict)


import six

import nxpy.core.abstract
import nxpy.test.test


class A(six.with_metaclass(abc.ABCMeta, object)):
    @nxpy.core.abstract.abstractstatic
    def f():
        pass

class B(A):
    pass

class AbstractTest(nxpy.test.test.TestCase):
    @nxpy.test.test.skipIfNotAtLeast(nxpy.core.past.V_2_6)
    def testPass(self):
        self.assertRaises(TypeError, B)
