# nxpy.core package ----------------------------------------------------------

# Copyright Nicola Musatti 2008 - 2014
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See http://nxpy.sourceforge.net for library home page. ---------------------

r"""
Utility functions that deal with non-string sequences.

"""

from __future__ import absolute_import

import six


def make_tuple(arg):
    r"""An alternate way of creating tuples from a single argument.
    
    A single string argument is turned into a single element tuple and a dictionary argument is 
    turned into a tuple of its items. Otherwise it works like the standard tuple constructor.
    
    """
    try:
        if isinstance(arg, six.string_types):
            return ( arg, )
        elif isinstance(arg, dict):
            return tuple(arg.items())
        else:
            return tuple(arg)
    except TypeError:
        return ( arg, )
