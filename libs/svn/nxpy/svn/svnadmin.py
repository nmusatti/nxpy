# nxpy_svn --------------------------------------------------------------------

# Copyright Nicola Musatti 2010 - 2018
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See https://github.com/nmusatti/nxpy/tree/master/libs/svn. ------------------

r"""
Subversion administration tool wrapper.

"""

from __future__ import absolute_import

import os

import nxpy.command.command
import nxpy.command.option


_config = nxpy.command.option.Config()

class SvnAdmin(nxpy.command.command.Command):
    def __init__(self, debug=None):
        super(SvnAdmin, self).__init__("svnadmin", debug)
    
    def create(self, path, debug=None):
        op = nxpy.command.option.Parser(_config, "create", ( path, ), {})
        self.run(op, debug)
        return "file:///" + path.replace(os.sep, "/").lstrip("/")
