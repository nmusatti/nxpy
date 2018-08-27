# nxpy.command package -------------------------------------------------------

# Copyright Nicola Musatti 2008 - 2014
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See http://nxpy.sourceforge.net for library home page. ---------------------

r"""
test_interpreter_format.py - tests for the interpreter._format function
"""

from __future__ import absolute_import

import os

import six

import nxpy.command.interpreter
import nxpy.command.error
import nxpy.test.test


in_string = r"""this
is
text
"""

def getFormatted(type_):
    out = []
    for l in in_string.split('\n'):
        if l:
            out.extend("".join((type_, l, '\n')))
    return "".join(out)

in_file = six.StringIO(in_string)

def getOutFile():
    out_file = six.StringIO(in_string)
    out_file.seek(0, os.SEEK_END)
    return out_file

def getOutput(out):
    out.seek(0)
    return "".join(out)

class formatTest(nxpy.test.test.TestCase):
    
    def test_format_str_none(self):
        self.assertEqual(nxpy.command.interpreter._format(in_string), 
                getFormatted(nxpy.command.interpreter.OUTPUT))
    
    def test_format_file_none(self):
        self.assertEqual(
                nxpy.command.interpreter._format(in_file, type_=nxpy.command.interpreter.COMMAND), 
                getFormatted(nxpy.command.interpreter.COMMAND))

    def test_format_str_FILE(self):
        self.assertEqual(getOutput(nxpy.command.interpreter._format(in_string, 
                        nxpy.command.interpreter.FILE, nxpy.command.interpreter.ERROR)),
                getFormatted(nxpy.command.interpreter.ERROR))

    def test_format_str_file(self):
        out = getOutFile()
        out.write(getFormatted(nxpy.command.interpreter.ERROR))
        self.assertEqual(getOutput(nxpy.command.interpreter._format(in_string, getOutFile(), 
                        nxpy.command.interpreter.ERROR)), 
                getOutput(out))

    def test_format_fail(self):
        self.assertRaises(nxpy.command.error.BadLogFormat, nxpy.command.interpreter._format, 
                in_string, type_=3)
