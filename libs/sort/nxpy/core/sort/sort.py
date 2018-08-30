# nxpy.core package ----------------------------------------------------------

# Copyright Nicola Musatti 2010 - 2014
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See http://nxpy.sourceforge.net for library home page. ---------------------

r"""
Sort functions.

"""

def topological_sort(pairs):
    r"""
    Provide a topological ordering of the supplied pair elements.
    
    *pairs* is a sequence of two element sequences, in which the first element comes before
    the second according to the desired ordering criterium.
    
    """
    res = []
    top = set()
    nodes = {}
    for end, start in pairs:
        if end not in nodes:
            nodes[end] = []
        nodes[end].append(start)
    for end, start in pairs:
        if start not in nodes:
            top.add(start)
    while len(top) > 0:
        s = top.pop()
        res.append(s)
        for e in nodes:
            try:
                nodes[e].remove(s)
                if len(nodes[e]) == 0:
                    top.add(e)
            except ValueError:
                pass
        for e in top:
            try:
                del nodes[e]
            except:
                pass
    if len(nodes) > 0:
        return None
    else:
        return res
