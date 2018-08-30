# nxpy.ply package -----------------------------------------------------------

# Copyright Nicola Musatti 2010 - 2014
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See http://nxpy.sourceforge.net for library home page. ---------------------

r"""
Class wrapper for PLY's lex module.

"""

from __future__ import absolute_import

import re

import ply.lex


class Scanner(object):
    def __init__(self, debug=False, ignorecase=False):
        self.debug = debug
        reflags = 0
        if ignorecase:
            reflags = re.IGNORECASE 
        self.lexer = ply.lex.lex(module=self, debug=self.debug, reflags=reflags)

    def reset(self, input_):
        self.lexer.input(input_)
    
    def token(self):
        return self.lexer.token()
