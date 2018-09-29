Nxpy Past
=========

*Nxpy_past* provides ways to express conditions on the current Python version to help handling
version differences::

   import nxpy.core.past
   
   if nxpy.core.past.V_2_6.at_least():
       import abc
   else:
       class abc(object):
           class ABCMeta(type):
               def __new__(mcs, name, bases, dict):
                   return type.__new__(mcs, name, bases, dict)

It is also possible to express assertions on the current version to better document why some code
fails::

   import nxpy.core.past
   
   nxpy.core.past.enforce_at_least(nxpy.core.past.V_2_6)
