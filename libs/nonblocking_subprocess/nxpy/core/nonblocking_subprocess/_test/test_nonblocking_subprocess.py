# nxpy.core package ----------------------------------------------------------

# Copyright Nicola Musatti 2014
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See http://nxpy.sourceforge.net for library home page. ---------------------


r"""
Tests for the nonblocking_subprocess module.

"""

from __future__ import absolute_import

# print_function is not available in Python 2.5
#from __future__ import print_function
import logging
import subprocess
import sys

import nxpy.core.nonblocking_subprocess
import nxpy.core._impl.log
import nxpy.test.test


_log = logging.getLogger(__name__)


class NonblockingPopenTest(nxpy.test.test.TestCase):
    def test(self):
        if sys.platform == 'win32':
            shell, commands, tail = ('cmd', ('dir /w', 'echo HELLO WORLD'), '\r\n')
        else:
            shell, commands, tail = ('sh', ('ls', 'echo HELLO WORLD'), '\n')
        
        a = nxpy.core.nonblocking_subprocess.NonblockingPopen(shell, stdin=subprocess.PIPE,
                stdout=subprocess.PIPE)
        _log.info(nxpy.core.nonblocking_subprocess.recv_some(a))
        for cmd in commands:
            nxpy.core.nonblocking_subprocess.send_all(a, cmd + tail)
            _log.info(nxpy.core.nonblocking_subprocess.recv_some(a))
        nxpy.core.nonblocking_subprocess.send_all(a, 'exit' + tail)
        _log.info(nxpy.core.nonblocking_subprocess.recv_some(a, e=0))
        self.assertEqual(a.wait(), 0)
