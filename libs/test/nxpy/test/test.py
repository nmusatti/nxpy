# nxpy.test package ----------------------------------------------------------

# Copyright Nicola Musatti 2008 - 2014
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See http://nxpy.sourceforge.net for library home page. ---------------------

r"""
Unittest utility functions.

"""

from __future__ import absolute_import

import sys

import nxpy.core.past


if nxpy.core.past.V_2_6.at_most():
    import unittest2
    TestCase = unittest2.TestCase
    TestLoader = unittest2.TestLoader
    TestSuite = unittest2.TestSuite
    TextTestRunner = unittest2.TextTestRunner
    main = unittest2.main
    skip = unittest2.skip
else:
    import unittest
    TestCase = unittest.TestCase
    TestLoader = unittest.TestLoader
    TestSuite = unittest.TestSuite
    TextTestRunner = unittest.TextTestRunner
    main = unittest.main
    skip = unittest.skip


def testModules(*modules):
    r"""Runs all tests defined in the given *modules*."""
    loader = TestLoader()
    loader.sortTestMethodsUsing = None
    suite = TestSuite()
    for m in modules:
        suite.addTests(loader.loadTestsFromModule(sys.modules[m]))
    TextTestRunner(verbosity=2).run(suite)


def testClasses(*classes):
    r"""Runs all tests defined in the given *classes*."""
    loader = TestLoader()
    loader.sortTestMethodsUsing = None
    suite = TestSuite()
    for c in classes:
        suite.addTests(loader.loadTestsFromTestCase(c))
    TextTestRunner(verbosity=2).run(suite)


def skipIfNotAtLeast(version):
    r"""Skip the current test if the current Python release is lower than *version*."""
    if version.at_least():
        return lambda func: func
    return skip("Requires at least Python " + str(version))


def skipIfNotAtMost(version):
    r"""Skip the current test if the current Python release is higher than *version*."""
    if version.at_most():
        return lambda func: func
    return skip("Requires at most Python " + str(version))
