# nxpy.core package ----------------------------------------------------------

# Copyright Nicola Musatti 2008 - 2015
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See http://nxpy.sourceforge.net for library home page. ---------------------

r"""
Tests for the *backup_file* module.

"""

# Python 2.5 compatibility
from __future__ import with_statement    
from __future__ import absolute_import

import os
import tempfile

import six

import nxpy.core.backup_file
import nxpy.core.temp_file
import nxpy.test.test


orig_text = "Original File"
mod_text = "Modified File"
tempDir = tempfile.gettempdir()


class BackupFileTest(nxpy.test.test.TestCase):
    
    def _makeFile(self):
        self._file = tempfile.NamedTemporaryFile(mode="w+")
        self._file.write(orig_text)
        self._file.seek(0, os.SEEK_SET)

    def _checkFile(self, value):
        self._file.seek(0, os.SEEK_SET)
        self.assertEqual(self._file.read(), value)
        
    def _makeName(self, missing=False):
        self._name = tempfile.mktemp("", "BackupFileTest")
        if not missing:
            file_ = open(self._name, "w+")
            file_.write(orig_text)
            file_.close()

    def _writeName(self):
        file_ = open(self._name, "w+")
        file_.write(mod_text)
        file_.close()

    def _checkName(self, value=True):
        if isinstance(value, six.string_types):
            with open(self._name, "r") as file_:
                self.assertEqual(file_.read(), value)
        else:
            self.assertEqual(os.access(self._name, os.R_OK), value)
        
    def setUp(self):
        self._file = None
        self._name = None
    
    def tearDown(self):
        if self._file is not None:
            self._file.close()
            del self._file
        if self._name is not None and os.access(self._name, os.F_OK):
            os.remove(self._name)

    
    def testPlainCopyObjNothing(self):
        self._makeFile()
        bck = nxpy.core.backup_file.BackupFile(self._file, 
                mode=nxpy.core.backup_file.BackupFile.COPY, dir=tempDir)
        bck.save()
        self._file.write(mod_text)
        self._checkFile(mod_text)
        bck.close()

    def testPlainCopyObjCommit(self):
        self._makeFile()
        bck = nxpy.core.backup_file.BackupFile(self._file, 
                mode=nxpy.core.backup_file.BackupFile.COPY, dir=tempDir)
        bck.save()
        self._file.write(mod_text)
        bck.commit()
        self._checkFile(mod_text)
        bck.close()

    def testPlainCopyObjRollback(self):
        self._makeFile()
        bck = nxpy.core.backup_file.BackupFile(self._file, 
                mode=nxpy.core.backup_file.BackupFile.COPY, dir=tempDir)
        bck.save()
        self._file.write(mod_text)
        bck.rollback()
        self._checkFile(orig_text)
        bck.close()

    def testPlainCopyNameNothing(self):
        self._makeName()
        bck = nxpy.core.backup_file.BackupFile(self._name, 
                mode=nxpy.core.backup_file.BackupFile.COPY)
        bck.save()
        self._checkName()
        self._writeName()
        self._checkName(mod_text)
        bck.close()

    def testPlainCopyNameCommit(self):
        self._makeName()
        bck = nxpy.core.backup_file.BackupFile(self._name, 
                mode=nxpy.core.backup_file.BackupFile.COPY)
        bck.save()
        self._checkName()
        self._writeName()
        bck.commit()
        self._checkName(mod_text)
        bck.close()

    def testPlainCopyNameRollback(self):
        self._makeName()
        bck = nxpy.core.backup_file.BackupFile(self._name, 
                mode=nxpy.core.backup_file.BackupFile.COPY)
        bck.save()
        self._checkName()
        self._writeName()
        bck.rollback()
        self._checkName(orig_text)
        bck.close()

    def testPlainMoveNameNothing(self):
        self._makeName()
        bck = nxpy.core.backup_file.BackupFile(self._name, 
                mode=nxpy.core.backup_file.BackupFile.MOVE)
        bck.save()
        self._checkName(False)
        self._writeName()
        self._checkName(mod_text)
        bck.close()

    def testPlainMoveNameCommit(self):
        self._makeName()
        bck = nxpy.core.backup_file.BackupFile(self._name, 
                mode=nxpy.core.backup_file.BackupFile.MOVE)
        bck.save()
        self._checkName(False)
        self._writeName()
        bck.commit()
        self._checkName(mod_text)
        bck.close()

    def testPlainMoveNameRollback(self):
        self._makeName()
        bck = nxpy.core.backup_file.BackupFile(self._name, 
                mode=nxpy.core.backup_file.BackupFile.MOVE)
        bck.save()
        self._checkName(False)
        self._writeName()
        bck.rollback()
        self._checkName(orig_text)
        bck.close()

    def testWithCopyObjNothing(self):
        self._makeFile()
        with nxpy.core.backup_file.BackupFile(self._file, 
                mode=nxpy.core.backup_file.BackupFile.COPY, dir=tempDir):
            self._file.write(mod_text)
        self._checkFile(mod_text)

    def testWithCopyObjCommit(self):
        self._makeFile()
        with nxpy.core.backup_file.BackupFile(self._file, 
                mode=nxpy.core.backup_file.BackupFile.COPY, dir=tempDir) as bck:
            self._file.write(mod_text)
            bck.commit()
        self._checkFile(mod_text)

    def testWithCopyObjRollback(self):
        self._makeFile()
        with nxpy.core.backup_file.BackupFile(self._file, 
                mode=nxpy.core.backup_file.BackupFile.COPY, dir=tempDir) as bck:
            self._file.write(mod_text)
            bck.rollback()
        self._checkFile(orig_text)

    def testWithCopyObjRaise(self):
        self._makeFile()
        try:
            with nxpy.core.backup_file.BackupFile(self._file, 
                    mode=nxpy.core.backup_file.BackupFile.COPY, dir=tempDir):
                self._file.write(mod_text)
                raise RuntimeError("Expected")
        except:
            pass
        self._checkFile(orig_text)

    def testWithCopyNameNothing(self):
        self._makeName()
        with nxpy.core.backup_file.BackupFile(self._name, 
                mode=nxpy.core.backup_file.BackupFile.COPY):
            self._checkName()
            self._writeName()
        self._checkName(mod_text)

    def testWithCopyNameCommit(self):
        self._makeName()
        with nxpy.core.backup_file.BackupFile(self._name, 
                mode=nxpy.core.backup_file.BackupFile.COPY) as bck:
            self._checkName()
            self._writeName()
            bck.commit()
        self._checkName(mod_text)

    def testWithCopyNameRollback(self):
        self._makeName()
        with nxpy.core.backup_file.BackupFile(self._name, 
                mode=nxpy.core.backup_file.BackupFile.COPY) as bck:
            self._checkName()
            self._writeName()
            bck.rollback()
        self._checkName(orig_text)

    def testWithCopyNameThrow(self):
        self._makeName()
        try:
            with nxpy.core.backup_file.BackupFile(self._name, 
                    mode=nxpy.core.backup_file.BackupFile.COPY, dir=tempDir):
                self._checkName()
                self._writeName()
                raise RuntimeError("Expected")
        except:
            pass
        self._checkName(orig_text)

    def testWithMoveNameNothing(self):
        self._makeName()
        with nxpy.core.backup_file.BackupFile(self._name, 
                mode=nxpy.core.backup_file.BackupFile.MOVE):
            self._checkName(False)
            self._writeName()
        self._checkName(mod_text)

    def testWithMoveNameCommit(self):
        self._makeName()
        with nxpy.core.backup_file.BackupFile(self._name, 
                mode=nxpy.core.backup_file.BackupFile.MOVE) as bck:
            self._checkName(False)
            self._writeName()
            bck.commit()
        self._checkName(mod_text)

    def testWithMoveNameRollback(self):
        self._makeName()
        with nxpy.core.backup_file.BackupFile(self._name, 
                mode=nxpy.core.backup_file.BackupFile.MOVE) as bck:
            self._checkName(False)
            self._writeName()
            bck.rollback()
        self._checkName(orig_text)

    def testWithMoveNameThrow(self):
        self._makeName()
        try:
            with nxpy.core.backup_file.BackupFile(self._name, 
                    mode=nxpy.core.backup_file.BackupFile.MOVE, dir=tempDir):
                self._checkName(False)
                self._writeName()
                raise RuntimeError("Expected")
        except:
            pass
        self._checkName(orig_text)

    def testMissingCopyNameNothing(self):
        self._makeName(True)
        bck = nxpy.core.backup_file.BackupFile(self._name, 
                mode=nxpy.core.backup_file.BackupFile.COPY)
        self.assertRaises(nxpy.core.backup_file.SaveError, bck.save)
        self._checkName(False)
        self._writeName()
        self._checkName(mod_text)

    def testMissingCopyNameCommit(self):
        self._makeName(True)
        bck = nxpy.core.backup_file.BackupFile(self._name, 
                mode=nxpy.core.backup_file.BackupFile.COPY)
        self.assertRaises(nxpy.core.backup_file.SaveError, bck.save)
        self._checkName(False)
        self._writeName()
        self.assertRaises(nxpy.core.backup_file.NotSavedError, bck.commit)
        self._checkName(mod_text)

    def testMissingCopyNameRollback(self):
        self._makeName(True)
        bck = nxpy.core.backup_file.BackupFile(self._name, 
                mode=nxpy.core.backup_file.BackupFile.COPY)
        self.assertRaises(nxpy.core.backup_file.SaveError, bck.save)
        self._checkName(False)
        self._writeName()
        self.assertRaises(nxpy.core.backup_file.NotSavedError, bck.rollback)
        self._checkName(True)

    def testMissingMoveNameNothing(self):
        self._makeName(True)
        bck = nxpy.core.backup_file.BackupFile(self._name, 
                mode=nxpy.core.backup_file.BackupFile.MOVE)
        self.assertRaises(nxpy.core.backup_file.SaveError, bck.save)
        self._checkName(False)
        self._writeName()
        self._checkName(mod_text)

    def testMissingMoveNameCommit(self):
        self._makeName(True)
        bck = nxpy.core.backup_file.BackupFile(self._name, 
                mode=nxpy.core.backup_file.BackupFile.MOVE)
        self.assertRaises(nxpy.core.backup_file.SaveError, bck.save)
        self._checkName(False)
        self._writeName()
        self.assertRaises(nxpy.core.backup_file.NotSavedError, bck.commit)
        self._checkName(mod_text)

    def testMissingMoveNameRollback(self):
        self._makeName(True)
        bck = nxpy.core.backup_file.BackupFile(self._name, 
                mode=nxpy.core.backup_file.BackupFile.MOVE)
        self.assertRaises(nxpy.core.backup_file.SaveError, bck.save)
        self._checkName(False)
        self._writeName()
        self.assertRaises(nxpy.core.backup_file.NotSavedError, bck.rollback)
        self._checkName(True)


class BackupDirTest(nxpy.test.test.TestCase):
    def _makePaths(self, dir_name):
        self._orig_dir = os.path.join(dir_name, "original")
        self._orig_file = os.path.join(self._orig_dir, "file")

    def _makeDir(self, text, create=True):
        if create:
            os.mkdir(self._orig_dir)
        with open(self._orig_file, "w+") as f:
            f.write(text)

    def testMoveCommit(self):
        with nxpy.core.temp_file.TempDir(prefix="test_backup_file_") as base_dir:
            self._makePaths(base_dir.name)
            self._makeDir(orig_text)
            with nxpy.core.backup_file.BackupDir(self._orig_dir):
                self._makeDir(mod_text)
            self.assertEqual(open(self._orig_file).read(), mod_text)

    def testMoveRollback(self):
        with nxpy.core.temp_file.TempDir(prefix="test_backup_file_") as base_dir:
            self._makePaths(base_dir.name)
            self._makeDir(orig_text)
            try:
                with nxpy.core.backup_file.BackupDir(self._orig_dir):
                    self._makeDir(mod_text)
                    raise Exception()
            except:
                pass
            self.assertEqual(open(self._orig_file).read(), orig_text)

    def testCopyCommit(self):
        with nxpy.core.temp_file.TempDir(prefix="test_backup_file_") as base_dir:
            self._makePaths(base_dir.name)
            self._makeDir(orig_text)
            with nxpy.core.backup_file.BackupDir(self._orig_dir, 
                    mode=nxpy.core.backup_file.BackupDir.COPY):
                self._makeDir(mod_text, False)
            self.assertEqual(open(self._orig_file).read(), mod_text)

    def testCopyRollback(self):
        with nxpy.core.temp_file.TempDir(prefix="test_backup_file_") as base_dir:
            self._makePaths(base_dir.name)
            self._makeDir(orig_text)
            try:
                with nxpy.core.backup_file.BackupDir(self._orig_dir, 
                        mode=nxpy.core.backup_file.BackupDir.COPY):
                    self._makeDir(mod_text, False)
                    raise Exception()
            except:
                pass
            self.assertEqual(open(self._orig_file).read(), orig_text)
