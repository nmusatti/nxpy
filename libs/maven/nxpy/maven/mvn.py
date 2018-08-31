# nxpy.maven package ---------------------------------------------------------

# Copyright Nicola Musatti 2010 - 2014
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See http://nxpy.sourceforge.net for library home page. ---------------------

r"""
Maven wrapper.

"""

from __future__ import absolute_import

import logging

import nxpy.command.command
import nxpy.command.option
import nxpy.core.sequence

import nxpy.core._impl.log

_log = logging.getLogger(__name__)

_config = nxpy.command.option.Config(
        separator = ",",
        iterable_opts = ( "projects" ), )


class Mvn(nxpy.command.command.Command):
    def __init__(self, debug=None):
        super(Mvn, self).__init__("mvn", debug)

    def _make_options(self, projects):
        kwargs = {}
        if projects is not None:
            kwargs["projects"] = nxpy.core.sequence.make_tuple(projects)
        return kwargs
    
    def clean(self, projects=None, debug=None):
        op = nxpy.command.option.Parser(_config, None, ( "clean", ), {},
                **self._make_options(projects))
        self.run(op, debug)

    def deploy(self, projects=None, debug=None):
        op = nxpy.command.option.Parser(_config, None, ( "deploy", ), {},
                **self._make_options(projects))
        self.run(op, debug)

    def package(self, projects=None, debug=None):
        op = nxpy.command.option.Parser(_config, None, ( "package", ), {},
                **self._make_options(projects))
        self.run(op, debug)
