# nxpy.core package ----------------------------------------------------------

# Copyright Nicola Musatti 2008 - 2014
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See http://nxpy.sourceforge.net for library home page. ---------------------

r"""
Memoize class instances according to a given key.
 
By default the key only assumes the *True* value, thus implementing a singleton. 

"""

from __future__ import absolute_import

import nxpy.core.abstract
import nxpy.core.past

if nxpy.core.past.V_2_6.at_least():
    import abc
    import six


class Memo(object):
    r"""
    Base class for classes that require memoization.
    
    Subclasses should override the *_key(\*args, \*\*kwargs)* method to compute a key on the
    constructor's arguments.
    
    Care should be taken to avoid calling *__init__()* again for entities already constructed.
    
    """
    #if nxpy.core.past.V_2_6.at_least():
    #    __metaclass__ = abc.ABCMeta
    
    _dict = {}
    
    def __new__(cls, *args, **kwargs):
        r"""
        Return the instance corresponding to the given key, creating it if it doesn't exist.
        
        """
        k = cls._key(*args, **kwargs)
        try:
            return Memo._dict[(cls, k)]
        except KeyError:
            i = super(Memo, cls).__new__(cls)
            Memo._dict[(cls, k)] = i
            return i

    if nxpy.core.past.V_2_6.at_least():
        @nxpy.core.abstract.abstractstatic
        def _key(*args, **kwargs):
            r"""
            Returns the key by which instances are memoized.
    
            Subclasses should override it as a function of their construction arguments.
            
            """
            return True
    else:
        @staticmethod
        def _key(*args, **kwargs):
            return True


if nxpy.core.past.V_2_6.at_least():
    Memo = six.add_metaclass(abc.ABCMeta)(Memo)
