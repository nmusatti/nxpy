# nxpy_past -------------------------------------------------------------------

# Copyright Nicola Musatti 2013 - 2019
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See https://github.com/nmusatti/nxpy/tree/master/libs/past. -----------------

r"""
Identification and enforcement of supported Python releases.

"""

from __future__ import absolute_import

import sys


class Version(object):
    r"""Identifies a Python release in a way that is convenient for comparison and printing."""
    
    def __init__(self, version):
        self.version = version

    def at_least(self):
        r"""Return *True* if the current Python version is equal or higher than *self*."""
        return sys.hexversion >= self.version
    
    def at_most(self):
        r"""Return *True* if the current Python version is equal or lower than *self*."""
        return sys.hexversion < ( self.version | 0xff00 )
    
    def __str__(self):
        v = hex(self.version)
        return v[2] + "." + v[4] + "." + v[6]

V_3_8 = Version(0x030800f0)

V_3_7 = Version(0x030700f0)

V_3_6 = Version(0x030600f0)

V_3_5 = Version(0x030500f0)

V_3_4 = Version(0x030400f0)

V_3_3 = Version(0x030300f0)

V_3_2 = Version(0x030200f0)

V_2_7 = Version(0x020700f0)

V_2_6 = Version(0x020600f0)

V_2_5 = Version(0x020500f0)

def enforce_at_least(version):
    r"""Assert that the current Python version is equal or higher than *version*."""
    assert version.at_least(), "Requires at least Python " + str(version)
 
def enforce_at_most(version):
    r"""Assert that the current Python version is equal or lower than *version*."""
    assert version.at_most(), "Requires at most Python " + str(version)
        