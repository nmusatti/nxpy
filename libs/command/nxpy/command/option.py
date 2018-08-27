# nxpy.command package -------------------------------------------------------

# Copyright Nicola Musatti 2010 - 2014
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See http://nxpy.sourceforge.net for library home page. ---------------------

r"""
Function argument to command line option conversion.
Provides means to describe commands with complicated syntaxes, which often combine sub-commands, 
options and arguments. Typical examples include subversion and ftp.

"""

from __future__ import absolute_import

import nxpy.core.sequence


class InvalidOptionError(Exception):
    r"""Raised when an option is not supported."""


class Config(object):
    r"""
    Command option definitions.
    Provides a single definition point for all the options supported by a command. 
    
    """
    def __init__(self, prefix="--", separator=" ", bool_opts=(), value_opts=(), iterable_opts=(), 
                 format_opts={}, mapped_opts={}, opposite_opts={}):
        r"""
        Constructor. Its arguments are used to specify all the valid options.
        Each option is prefixed by *prefix*. When an option takes multiple arguments these are
        separated by a *separator*. *bool_opts* must be specified on the command line when they
        are *True*. *value_opts* take a single argument; *iterable_opts* take multiple arguments;
        *format_opts* have their syntax specified by means of a format string;
        *mapped_opts* require some form of translation, usually because they are not valid
        Python identifiers; *opposite_opts* must be specified on the command line when they
        are *False*.
        
        """
        self.prefix = prefix
        self.separator = separator
        self.bool_opts = bool_opts
        self.value_opts = value_opts
        self.iterable_opts = iterable_opts
        self.format_opts = format_opts
        self.mapped_opts = mapped_opts
        self.opposite_opts = opposite_opts
        
        self.opts = set(nxpy.core.sequence.make_tuple(bool_opts))
        self.opts.update(nxpy.core.sequence.make_tuple(value_opts))
        self.opts.update(nxpy.core.sequence.make_tuple(iterable_opts))
        self.opts.update(format_opts.keys())
        self.opts.difference_update(mapped_opts.keys())


class Parser(object):
    r"""
    Constructs a complex command line from the provided *command* and its *options* and
    *arguments*. Uses a :py:class:`.Config` instance, *config*, to provide means to check conditions
    on the supplied options. Other constraints on how options should be used may be expressed and
    verified by means of the *check* methods.
    
    """
    def __init__(self, config, command, arguments, options, **defaults):
        r"""
        Takes an instance of :py:class:`.Config`, a *command* to execute, an iterable of *arguments*
        and a mapping of *options* and their actual values. The remaining keyword arguments indicate
        the options supported by *command* with their default values. 
        
        """
        invalid = set(options.keys()).difference(defaults.keys())
        if len(invalid) > 0:
            raise InvalidOptionError(", ".join(invalid) + 
                    ": invalid option(s)")
        self.config = config
        self.command = command
        self.arguments = arguments
        self.options = {}
        self.options.update(defaults)
        self.options.update(options)
        self.cmd_line = []

    def getCommandLine(self):
        r"""Returns the command line to be executed."""
        if not self.cmd_line:
            self._applyOptions()
            if self.arguments:
                self.cmd_line.extend(self.arguments)
        return " ".join(self.cmd_line)

    def checkMandatoryOptions(self, *options):
        r"""Checks that all compulsory options have been specified."""
        if not all([ bool(self.options[o]) for o in options ]):
            raise InvalidOptionError(", ".join(options) +
                    ": mandatory options")

    def checkExclusiveOptions(self, *options):
        r"""Checks that at most one in a set of mutually exclusive options has been specified."""
        if sum([ bool(self.options[o]) for o in options ]) > 1:
            raise InvalidOptionError(", ".join(options) + 
                    ": mutually exclusive options")

    def checkExactlyOneOption(self, *options):
        r"""
        Checks that one and only one in a set of mutually exclusive options has been specified.
        
        """
        s = sum([ bool(self.options[o]) for o in options ])
        if s != 1:
            raise InvalidOptionError(", ".join(options) + 
                    ": only one among these options should be specified")

    def checkNotBothOptsAndArgs(self, *options):
        r"""
        Checks that options incompatible with arguments haven't been specified if any argument is
        present.
        
        """
        if any([ bool(self.options[o]) for o in options ]) and self.arguments:
            raise InvalidOptionError(", ".join(options) + 
                    ": This/these option(s) is/are invalid when arguments are specified")

    def checkOneBetweenOptsAndArgs(self, *options):
        r"""
        Checks that either at least one in a set of options or some arguments have been specified,
        but not both.
        
        """
        if ( any([ bool(self.options[o]) for o in options ]) + 
                bool(self.arguments) ) != 1:
            raise InvalidOptionError(", ".join(options) + 
                    ": This/these option(s) is/are mutually exclusive with arguments")

    def _applyOptions(self):
        r"""Translates options specified as function parameters into command line arguments."""
        if self.command is not None:
            self.cmd_line.append(self.command)
        for opt in self.options.keys():
            if self.options[opt]:
                if opt in self.config.opts:
                    self.cmd_line.append(self.config.prefix + opt)
                elif opt in self.config.mapped_opts:
                    self.cmd_line.append(self.config.mapped_opts[opt])
                
                if opt in self.config.value_opts:
                    self.cmd_line.append(self.options[opt])
                elif opt in self.config.iterable_opts:
                    self.cmd_line.append(self.config.separator.join(self.options[opt]))
                elif opt in self.config.format_opts.keys():
                    self.cmd_line.append(
                            self.config.format_opts[opt] % self.options[opt])
            elif opt in self.config.opposite_opts.keys():
                self.cmd_line.append(self.config.opposite_opts[opt])
