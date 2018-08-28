# nxpy.core._impl package ----------------------------------------------------

# Copyright Nicola Musatti 2010 - 2014
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See http://nxpy.sourceforge.net for library home page. ---------------------

r"""
This module should be imported in all modules that use the standard logging module

"""

from __future__ import absolute_import

import logging

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

logging.getLogger("nxpy").addHandler(NullHandler())
