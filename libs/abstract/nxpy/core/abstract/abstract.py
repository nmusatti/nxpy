# nxpy.core package ----------------------------------------------------------

# Copyright Nicola Musatti 2013 - 2014
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See http://nxpy.sourceforge.net for library home page. ---------------------

r"""
Helpers for the standard :py:mod:`abc` module.

"""

from __future__ import absolute_import

import nxpy.core.past


if nxpy.core.past.V_2_7.at_most():
    
    class abstractstatic(staticmethod):
        r"""
        Decorator that combines :py:obj:`staticmethod` and :py:obj:`abc.abstractmethod`.
        
        Copied from `this answer <http://stackoverflow.com/a/4474495/838975>`_ to `this StackOverflow
        question
        <http://stackoverflow.com/questions/4474395/staticmethod-and-abc-abstractmethod-will-it-blend>`_.
        
        """
        __slots__ = ()
        
        def __init__(self, function):
            super(abstractstatic, self).__init__(function)
            function.__isabstractmethod__ = True
    
        __isabstractmethod__ = True

elif nxpy.core.past.V_3_2.at_least():
    
    import abc
    
    abstractstatic = abc.abstractstaticmethod
    