# nxpy_ply --------------------------------------------------------------------

# Copyright Nicola Musatti 2010 - 2018
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See https://github.com/nmusatti/nxpy/tree/master/libs/ply. ------------------

r"""
Class wrapper for PLY's yacc module.

"""

from __future__ import absolute_import

import ply.yacc


class Parser(object):
    def __init__(self, scanner, debug=False):
        self.scanner = scanner
        self.debug = debug
        Parser.tokens = self.scanner.tokens
        self.parser = ply.yacc.yacc(module=self, debug=self.debug)

    def parse(self, input_):
        self.scanner.reset(input_)
        return self.parser.parse(lexer=self.scanner.lexer)
