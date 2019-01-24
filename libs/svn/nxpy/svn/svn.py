# nxpy_svn --------------------------------------------------------------------

# Copyright Nicola Musatti 2010 - 2019
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See https://github.com/nmusatti/nxpy/tree/master/libs/svn. ------------------

r"""
Subversion client wrapper.

Only supports versions 1.6, 1.7 and 1.8, others might work but have not been
tested.
Requires at least Python 2.6.

"""

# Ensures that tests are skipped rather than broken when run with Python 2.5
from __future__ import with_statement
from __future__ import absolute_import
 
import logging
import os
import os.path
import re

import six

import nxpy.command.command
import nxpy.command.option
import nxpy.core.error
import nxpy.core.past
import nxpy.core.temp_file
import nxpy.svn.url

import nxpy.core._impl.log

_log = logging.getLogger(__name__)


class Info(object):
    r"""Represents the output of the ``svn info`` command in a structured way."""
    _outRe = re.compile(r"([^:]+):\s+(.*)")
    
    def __init__(self, out):
        for l in out.split("\n"):
            match = Info._outRe.match(l)
            if match:
                if match.group(1) == "Path":
                    self.path = os.path.realpath(match.group(2))
                elif match.group(1) == "URL":
                    self.url = match.group(2)
                elif match.group(1) == "Repository Root":
                    self.root = match.group(2)
    
    def __str__(self):
        return " - ".join((self.path, str(self.url), self.root))


class Status(object):
    r"""Represents the output of one line of the ``svn status`` command in a structured way."""
    
    def __init__(self, line):
        self.item = line[8:]
        self.state = line[0]
        self.properties = line[1]
        self.locked = line[2] == 'L'
        self.add_with_history = line[3] == '+'
        self.switched = line[4] == 'S'
        self.lock = line[5]
        self.tree_conflict = line[6] == 'C'

    def __str__(self):
        return ( self.state + self.properties + ( 'L' if self.locked else ' ') + 
                ( '+' if self.add_with_history else ' ' ) + ( 'S' if self.switched else ' ' ) +
                self.lock + ( 'C' if self.tree_conflict else ' ' ) + ' ' + self.item )


_config = nxpy.command.option.Config(
        bool_opts = ( "ignore_externals", "keep_local", "parents", "quiet", "stop_on_copy", 
                "summarize", "verbose", "version", "xml" ),
        value_opts = ( "file", "message", "password", "revision", "username", "value" ),
        opposite_opts = { "ignore" : "--no-ignore" },
        mapped_opts = { "ignore_externals" : "--ignore-externals",
                        "keep_local" : "--keep-local",
                        "stop_on_copy" : "--stop-on-copy",
                        "value" : "",
                        "version" : "--version" } )


class Parser(nxpy.command.option.Parser):
    r"""Allows passing *nxpy.svn.url.Url* instances as arguments to *Svn*'s methods."""
    def __init__(self, command, arguments, options, **defaults):
        super(Parser, self).__init__(_config, command, 
                [ self._pathtostring(a) for a in arguments ], options, **defaults)
    
    def _pathtostring(self, path):
        if isinstance(path, nxpy.svn.url.Url):
            return str(path)
        elif isinstance(path, six.string_types):
            return path
        else:
            raise nxpy.core.error.ArgumentError()
        

class Svn(nxpy.command.command.Command):
    r"""The actual wrapper."""
    def __init__(self, debug=False):
        super(Svn, self).__init__("svn --non-interactive", debug)
        self._version = None
    
    _versionRe = re.compile(r"(\d+)\.(\d+)\.(\d+)")
    
    def version(self):
        op = Parser("", (), {}, version=True)
        out = self.run(op)[0]
        match = Svn._versionRe.search(out)
        version = ( int(match.group(1)), int(match.group(2)), int(match.group(3)))
        return version

    def info(self, *targets):
        op = Parser("info", targets, {})
        out = self.run(op)[0]
        return Info(out)

    def list(self, *targets):
        op = Parser("list", targets, {})
        out = self.run(op)[0]
        return out.split()
    
    def mkdir(self, *targets, **options):
        debug = options.get("debug")
        if debug is not None:
            del options["debug"]
        op = Parser("mkdir", targets, options, parents=False, username="", password="",
                message="\"[" + __name__ + "] Make dir(s) " + ", ".join(targets) + "\"")
        self.run(op, debug)

    def status(self, *targets, **options):
        op = Parser("status", targets, options, ignore=True, quiet=True, ignore_externals=True)
        out = self.run(op)[0]
        ignore_externals = options.get('ignore_externals', True)
        res = []
        for l in out.split("\n"):
            if len(l) > 0 and ( not ignore_externals or l[0] != "X" ):
                res.append(Status(l))
        return res

    def import_(self, src, dest, debug=False, **options):
        op = Parser("import", ( src, dest ), options, username="", password="", 
                    message="\"[" + __name__ + "] Import from " + src + "\"")
        self.run(op, debug)

    def export(self, src, dest, **options):
        op = Parser("export", ( src, dest ), options)
        self.run(op)

    def checkout(self, src, dest, debug=False, **options):
        op = Parser("checkout", ( src, dest ), options, username="", password="", 
                ignore_externals=True)
        self.run(op, debug)

    def update(self, *targets, **options):
        debug = options.get("debug")
        if debug is not None:
            del options["debug"]
        op = Parser("update", targets, options, ignore_externals=True)
        self.run(op, debug)

    def commit(self, src, debug=False, **options):
        op = Parser("commit", ( src, ), options, username="", password="", 
                    message="\"[" + __name__ + "] Commit from " + src + "\"")
        self.run(op, debug)

    def copy(self, src, dest, debug=False, **options):
        op = Parser("copy", ( src, dest ), options, ignore_externals=True, username="", password="", 
                    message="\"[" + __name__ + "] Copy from " + src + "\"")
        self.run(op, debug)

    def move(self, src, dest, debug=False, **options):
        op = Parser("move", ( src, dest ), options, username="", password="", 
                    message="\"[" + __name__ + "] Move from " + src + " to " + dest + "\"")
        self.run(op, debug)

    def _delete_paths(self, debug, *paths, **options):
        op = Parser("delete", paths, options, keep_local=False)
        self.run(op, debug)

    def _delete_urls(self, debug, *urls, **options):
        op = Parser("delete", urls, options, username="", password="", 
                message="\"[" + __name__ + "] Delete " + ", ".join([ str(u) for u in urls ]) + "\"")
        self.run(op, debug)

    def delete(self, *targets, **options):
        debug = options.get("debug")
        if debug is not None:
            del options["debug"]
        paths = []
        urls = []
        for t in targets:
            if not isinstance(t, nxpy.svn.url.Url) and os.access(t, os.R_OK):
                paths.append(t)
            else:
                urls.append(t)
        if len(paths) > 0:
            self._delete_paths(debug, *paths, **options)
        if len(urls) > 0:
            self._delete_urls(debug, *urls, **options)
    
    def propget(self, name, *targets):
        op = Parser("propget", ( name, ) + targets, {})
        out = self.run(op)[0]
        return out.strip()

    def getexternals(self, d):
        r"""
        Return *d*'s ``svn:externals`` property as a dictionary of directory - URL pairs.

        Note that only a limited subset of the externals syntax is supported: either the pre-svn 1.5
        one (directory - URL) or the same with inverted elements.
        Throw *nxpy.svn.url.BadUrlError* if an external URL is malformed.

        """
        out = self.propget("svn:externals", d)
        res = {}
        for l in out.split("\n"):
            # Python 2.7 incompatibility
            # dir, url = l.rsplit(maxsplit=1)
            dir, url = l.rsplit(None, 1)
            try:
                nxpy.svn.url.Url(url)
            except IndexError:
                # Python 2.7 incompatibility
                # url, dir = l.split(maxsplit=1)
                url, dir = l.split(None, 1)
                nxpy.svn.url.Url(url)
            res[dir] = url
        return res

    def getignore(self, d):
        out = self.propget("svn:ignore", d)
        return list(out.split("\n"))
    
    def propset(self, name, *targets, **options):
        debug = options.get("debug")
        if debug is not None:
            del options["debug"]
        value = options.get("value")
        if value:
            del options["value"]
            op = Parser("propset", ( name, value ) + targets, options, username="", password="")
        else:
            op = Parser("propset", ( name, ) + targets, options, file="", username="", password="")
        self.run(op, debug)
        
    def setexternals(self, externals, d, username="", password="", debug=False):
        nxpy.core.past.enforce_at_least(nxpy.core.past.V_2_6)
        with nxpy.core.temp_file.TempFile(mode="w+", prefix="svn_setexternals") as f:
            for k, v in six.iteritems(externals):
                f.write(k + "\t" + v + "\n")
            f.seek(0, os.SEEK_SET)
            _log.debug(f.read())
            f.close()
            self.propset("svn:externals", d, file=f.name, username=username, password=password, debug=debug)

    def setignore(self, ignore, d, username="", password="", debug=False):
        nxpy.core.past.enforce_at_least(nxpy.core.past.V_2_6)
        with nxpy.core.temp_file.TempFile(mode="w+", prefix="svn_setignore") as f:
            for v in ignore:
                f.write(v + "\n")
            f.seek(0, os.SEEK_SET)
            _log.debug(f.read())
            f.close()
            self.propset("svn:ignore", d, file=f.name, username=username, password=password, debug=debug)

    def diff(self, *targets, **options):
        op = Parser("diff", targets, options, summarize=False, revision=None)
        out = self.run(op)[0]
        return out

    def cat(self, *targets, **options):
        op = Parser("cat", targets, options, revision=None)
        out = self.run(op)[0]
        return out

    def log(self, src, **options):
        op = Parser("log", ( src, ), options, verbose=False, stop_on_copy=False, revision=None, 
                xml=False)
        out = self.run(op)[0]
        return out
