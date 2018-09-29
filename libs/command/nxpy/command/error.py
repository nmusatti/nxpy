# nxpy_command ----------------------------------------------------------------

# Copyright Nicola Musatti 2010 - 2018
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See https://github.com/nmusatti/nxpy/tree/master/libs/command. --------------

r"""
Exception classes for the nxpy.command package.

"""


class Error(Exception):
    r"""Package exceptions' base class."""


class BadLogFormat(Error):
    r"""Raised if the requested formatting option is unknown."""


class ExpectError(Exception):
    """Raised on invalid input from stdout or stderr."""


class TimeoutError(Exception):
    """Raised when expect didn't satisfy a timing constraint."""


class TimerError(Exception):
    """Raised on misuse of the Timer class."""
