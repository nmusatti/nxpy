# nxpy.core package ----------------------------------------------------------

# Copyright Nicola Musatti 2008 - 2015
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See http://nxpy.sourceforge.net for library home page. ---------------------

r"""
Backup a file or directory to make editing reversible.

Implement the context manager protocol, so as to be suitable to be used with
the *with* statement. When used in this fashion changes are discarded when an 
exception is thrown.

"""

from __future__ import absolute_import

import os.path
import shutil
import tempfile

import six

import nxpy.core.error
import nxpy.core.file_object
import nxpy.core.path


class NotSavedError(Exception):
    r"""
    Raised when commit or rollback is called on an inactive *BackUpFile* or *BackUpDirectory*.
    
    """


class SaveError(Exception):
    r"""Raised when a backup file or directory could not be created."""


class RemovalError(Exception):
    r"""Raised to signal errors in the removal of backup files or directories."""


class MissingBackupError(Exception):
    r"""raised when a backup file or directory isn't found."""


class BackupFile(nxpy.core.file_object.ReadOnlyFileObject):
    r"""
    Implements a read only file object used to automatically back up a file that has to be
    modified.
    
    """
    _prefix = "_BackupFile"

    MOVE = 1
    COPY = 2
    
    def __init__(self, file_, ext=".BAK", dir=".", mode=COPY):
        r"""
        Prepare to backup *file_*, either a file-like object or a path. 
        
        The backup file will be created in directory *dir* with extension *ext*. If *mode* is 
        *COPY* the original file will be copied to the backup destination; if *mode* is *MOVE* it 
        will be moved there.
        
        """
        super(BackupFile, self).__init__()
        if mode not in ( BackupFile.MOVE, BackupFile.COPY ):
            raise nxpy.core.error.ArgumentError(self.mode + ": Invalid mode")
        if isinstance(file_, six.string_types):
            self._orig_name = file_
            self._orig_file = None
            self._bck_name = os.path.join(dir, self._orig_name) + ext            
        else:
            self._orig_name = None
            self._orig_file = file_
            self._bck_name = tempfile.mktemp(ext, BackupFile._prefix, dir)
        if mode == BackupFile.MOVE and self._orig_name is None:
            raise nxpy.core.error.ArgumentError("Mode can only be MOVE when file_ is a path.")
        self._bck_file = None
        self._mode = mode
        self._saved = False

    @property
    def name(self):
        r"""The name of the file to be backed up."""
        if self._orig_name is not None:
            return self._orig_name
        else:
            return self._orig_file.name

    def __enter__(self):
        r"""When the controlling *with* statement is entered, create the backup file."""
        self.save()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        r"""
        When the controlling *with* statement is exited normally discard the backup file,
        otherwise restore it to its original place.
        
        """
        if self._saved:
            if exc_type is None:
                self.commit()
            else:
                self.rollback()
        return False

    def save(self):
        r"""
        Create a backup copy of the original file.
        
        Throw *SaveError* if it wasn't possible.
        """
        self.close()
        if self._mode == BackupFile.MOVE:
            try:
                shutil.move(self._orig_name, self._bck_name)
            except:
                raise SaveError()
        elif self._mode == BackupFile.COPY:
            try:
                if self._orig_file is None:
                    self._orig_file = open(self._orig_name, "r+")
                    self._tell = self._orig_file.tell()
                else:
                    self._tell = self._orig_file.tell()
                    self._orig_file.seek(0, os.SEEK_SET)
                self._bck_file = open(self._bck_name,"w+")
                shutil.copyfileobj(self._orig_file, self._bck_file, -1)
                self._orig_file.seek(self._tell, os.SEEK_SET)
                self._bck_file.close()
                self._bck_file = None
            except:
                raise SaveError("Could not backup file " + self._orig_name
                        if self._orig_name is not None else self._bck_name)
        self._saved = True

    def commit(self):
        r"""Discard the backup, i.e. keep the supposedly modified file."""
        if not self._saved:
            raise NotSavedError(self._orig_name + ": File not saved")
        self.close()
        try:
            os.remove(self._bck_name)
        except:
            raise RemovalError("Error removing file " + self._bck_name)
        self._saved = False

    def rollback(self):
        r"""Replace the original file with the backup copy."""
        if not self._saved:
            raise NotSavedError(self._orig_name + ": File not saved")
        self.close()
        try:
            if self._mode == BackupFile.MOVE:
                shutil.move(self._bck_name, self._orig_name)
            elif self._mode == BackupFile.COPY:
                self._bck_file = open(self._bck_name,"r")
                self._orig_file.seek(0, os.SEEK_SET)
                shutil.copyfileobj(self._bck_file, self._orig_file, -1)
                if self._orig_name is None:
                    self._orig_file.seek(self._tell, os.SEEK_SET)
                else:
                    self._orig_file.close()
                self._bck_file.close()
                self._bck_file = None
                os.remove(self._bck_name)
        except:
            raise MissingBackupError("File " + self._bck_name + 
                        " not found")
        self._saved = False

    BINARY = 3
    TEXT = 4
    
    def open(self, mode=TEXT):
        r"""Open the backup file for reading. *mode* may be either *TEXT* or *BINARY*."""
        if not self._saved:
            raise NotSavedError(self._name + ": File not saved")
        if mode == BackupFile.TEXT:
            self._bck_file = open(self._bck_name,"r")
        elif mode == BackupFile.BINARY:
            self._bck_file = open(self._bck_name,"rb")
        self.setFile(self._bck_file)

    def close(self):
        r"""
        Close the backup file and release the corresponding reference.
        
        The backup file may not be reopened.
        
        """
        if self._bck_file:
            self._bck_file.close()
            self._bck_file = None
            self.setFile(None)


class BackupDir(object):
    r"""
    Move or copy a directory that needs to be recreated or modified.
    
    """
    MOVE = 1
    COPY = 2
    
    def __init__(self, dir_, ext=".BAK", mode=MOVE):
        r"""
        Prepare to backup the *dir_* directory. 
        
        The backup will be created in *dir_*'s parent directory, which must be writable, with 
        extension *ext*. If *mode* is *MOVE*, the default, the original directory will be moved to
        the backup destination; if *mode* is *COPY* it will be copied there.
        
        """
        if mode not in ( BackupDir.MOVE, BackupDir.COPY ):
            raise nxpy.core.error.ArgumentError(self.mode + ": Invalid mode")
        self._orig_dir = dir_
        self._bck_dir = dir_ + ext
        self._mode = mode
        self._saved = False

    def __enter__(self):
        r"""When the controlling *with* statement is entered, create the backup directory."""
        self.save()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        r"""
        When the controlling *with* statement is exited normally discard the backup directory,
        otherwise restore it to its original place.
        
        """
        if self._saved:
            if exc_type is None:
                self.commit()
            else:
                self.rollback()
        return False

    def save(self):
        r"""Create a backup copy of the original directory."""
        if self._mode == BackupFile.MOVE:
            try:
                shutil.move(self._orig_dir, self._bck_dir)
            except:
                raise SaveError("Could not backup directory " + self._orig_dir)
        elif self._mode == BackupFile.COPY:
            try:
                shutil.copytree(self._orig_dir, self._bck_dir)
            except:
                raise SaveError("Could not backup directory " + self._orig_dir)
        self._saved = True

    def commit(self):
        r"""Discard the backup, i.e. keep the supposedly modified file."""
        if not self._saved:
            raise NotSavedError(self._orig_dir + ": directory not saved")
        try:
            nxpy.core.path.blasttree(self._bck_dir)
        except:
            raise RemovalError("Error removing directory " + self._bck_dir)
        self._saved = False

    def rollback(self):
        r"""Replace the original file with the backup copy."""
        if not self._saved:
            raise NotSavedError(self._orig_dir + ": directory not saved")
        try:
            temp_dir = None
            if os.path.isdir(self._orig_dir):
                temp_dir = self._orig_dir + ".NEW"
                shutil.copytree(self._orig_dir, temp_dir)
            nxpy.core.path.blasttree(self._orig_dir)
            shutil.copytree(self._bck_dir, self._orig_dir)
            if temp_dir is not None:
                nxpy.core.path.blasttree(temp_dir)
        except:
            raise MissingBackupError("Directory " + self._bck_dir + " not found")
        self._saved = False
