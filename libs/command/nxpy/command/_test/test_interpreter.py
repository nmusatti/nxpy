# nxpy_command ----------------------------------------------------------------

# Copyright Nicola Musatti 2014 - 2018
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See https://github.com/nmusatti/nxpy/tree/master/libs/command. --------------

r"""
Tests for the interpreter module.

"""

from __future__ import absolute_import

import sys

import nxpy.command.interpreter
import nxpy.test.test


class InterpreterTest(nxpy.test.test.TestCase):
    
    def testPass(self):
        if sys.platform == 'win32':
            shell, command = ('cmd', 'echo HELLO WORLD\r\n')
        else:
            shell, command = ('sh', 'echo HELLO WORLD\n')
        i = nxpy.command.interpreter.Interpreter(shell)
        self.assertTrue(i is not None)
        i.send_cmd(command)
        out, err = i.expect_lines()
        self.assertTrue("HELLO WORLD" in out)
