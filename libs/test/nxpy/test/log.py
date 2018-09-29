# nxpy_test -------------------------------------------------------------------

# Copyright Nicola Musatti 2011 - 2018
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See https://github.com/nmusatti/nxpy/tree/master/libs/test. -----------------

r"""
Logging configuration for tests.

"""

from __future__ import absolute_import

import logging
import os
import sys

_level = logging.INFO

try:
    _level = logging.__dict__[os.environ["NXPY_TEST_LOG_LEVEL"]]
except KeyError:
    pass

logging.basicConfig(stream=sys.__stderr__, level=_level)
