# nxpy.command package -------------------------------------------------------

# Copyright Nicola Musatti 2010 - 2014
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See http://nxpy.sourceforge.net for library home page. ---------------------

r"""
Non interactive command driver.

"""

from __future__ import absolute_import

import logging
import os
import subprocess

import nxpy.core._impl.log


_log = logging.getLogger(__name__)


class Error(Exception):
    r"""Raised when command execution fails."""
    def __init__(self, cmd, returncode, err):
        r"""Takes the command line, the error code and the contents of the error stream."""
        self.cmd = cmd
        self.returncode = returncode
        self.stderr = err
        super(Error, self).__init__("%s(%d):\n%s" % ( cmd, returncode, err))


class Command(object):
    r"""
    Represents the command to be executed.
    Typically you would derive from this class and provide a different method for each alternative
    way of invoking the program. If the program you want to execute has many sub-commands you
    might provide a different method for each sub-command. You can use the 
    :py:class:`.option.Config` class to declare the options supported by your command and then use
    the :py:class:`.option.Parser` class to validate your methods' arguments and generate the
    resulting command line. A debug mode is available in which commands are echoed rather than run.
    This can be enabled globally or separately for each invocation.
    
    """
    def __init__(self, cmd, debug=False):
        r"""
        Takes as arguments the command name and a boolean value indicating whether debug mode
        should be activated for all executions of this command.
        
        """
        self.cmd = cmd
        self.debug = debug
    
    def run(self, parser, debug=False):
        r"""
        Executes the command.
        Takes as arguments a command line parser (see the *option* module) and a boolean
        indicating whether debug mode should be used for this execution.
        
        """
        os.environ["LANG"] = "C"
        cmdline = []
        if debug or self.debug:
            cmdline.append("echo")
        cmdline.append(self.cmd)
        cmdline.append(parser.getCommandLine())
        cmd = " ".join(cmdline)
        _log.debug(cmd)
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, 
                                 universal_newlines=True)
        out, err = popen.communicate(None)
        _log.debug("----- OUTPUT -----")
        _log.debug(out)
        _log.debug("----- ERROR -----")
        _log.debug(err)
        if popen.returncode != 0:
            raise Error(cmd, popen.returncode, err)
        return out, err
