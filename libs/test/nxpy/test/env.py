# nxpy.test package ----------------------------------------------------------

# Copyright Nicola Musatti 2010 - 2014
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See http://nxpy.sourceforge.net for library home page. ---------------------

r"""
Environment configuration for tests that interact with the system.

"""

from __future__ import absolute_import

import os
import os.path

import nxpy.core.memo


class TestEnvNotSetError(Exception):
    r"""Raised when the test environment hasn't been setup, i.e. NXPY_TEST_DIR is not set."""


class _Dir(nxpy.core.memo.Memo):
    def __init__(self):
        if getattr(self, "base", None) is None:
            try:
                self.base = os.environ["NXPY_TEST_DIR"]
                if not os.path.isdir(self.base):
                    self.base = None
            except KeyError:
                self.base = None

    @staticmethod
    def _key(*args, **kwargs):
        return super(_Dir, _Dir)._key(*args, **kwargs)


class EnvBase(object):
    def __init__(self, elem):
        self._dir = _Dir()
        if self._dir.base is None:
            raise TestEnvNotSetError()
        self.elem = elem
        self.elem_dir = os.path.join(self._dir.base, elem)

    
class Data(EnvBase):
    def __init__(self, package):
        EnvBase.__init__(self, "data")
        self.data = os.path.join(self.elem_dir, package)


def get_data(test, package):
    try:
        return Data(package)
    except TestEnvNotSetError:
        test.skipTest("Test environment not set")
        return None


class Env(EnvBase):
    def __init__(self, package):
        EnvBase.__init__(self, "wcopy")
        self.wcopy = os.path.join(self.elem_dir, package)
        rd = self._dir.base
        repo_dir = []
        while True:
            rd, d = os.path.split(rd)
            if d:
                repo_dir.append(d)
            else:
                rd = rd.replace(os.path.sep, "")
                if rd:
                    repo_dir.append(rd)
                break
        repo_dir.reverse()
        repo_dir.extend(("repo", package))
        self.repo = "file:///" + "/".join(repo_dir)
        self.backup = os.path.join(self._dir.base, "backup", package)


def get_env(test, package):
    try:
        return Env(package)
    except TestEnvNotSetError:
        test.skipTest("Test environment not set")
        return None
