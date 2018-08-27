# nxpy.core package ----------------------------------------------------------

# Copyright Nicola Musatti 2008 - 2018
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See http://nxpy.sourceforge.net for library home page. ---------------------

r"""
Allow non-blocking interaction with a subprocess.

This module was taken from `this recipe 
<http://code.activestate.com/recipes/440554-module-to-allow-asynchronous-subprocess-use-on-win/>`_ 
in the `ActiveState Code Recipes website 
<http://code.activestate.com/recipes/langs/python/>`_, with only minor
modifications. This is the original description: ::

  Title:        Module to allow Asynchronous subprocess use on Windows and Posix platforms
  Submitter:    Josiah Carlson (other recipes)
  Last Updated: 2006/12/01
  Version no:   1.9
  Category:     System 

On Windows `pywin32 <https://pypi.python.org/pypi/pywin32>`_ is required.

"""

from __future__ import absolute_import

import os
import subprocess
import errno
import locale
import time
import sys

import six

import nxpy.core.past

if nxpy.core.past.V_2_5.at_most():
    def bytearray(s, e):
        return s
    
## PIPE = subprocess.PIPE

mswindows = (sys.platform == "win32")

if mswindows:
    from win32file import ReadFile, WriteFile
    from win32pipe import PeekNamedPipe
    import msvcrt
    import pywintypes
    
else:
    import select
    import fcntl

class NonblockingPopen(subprocess.Popen):
    r"""
    An asynchronous variant to :py:class:`subprocess.Popen`, which doesn't block on incomplete I/O 
    operations.
    
    Note that the terms input, output and error refer to the controlled program streams,
    so we receive from output or error and we send to input.
    
    """

    def __init__(self, cmd, encoding=None, **kwargs):
        r"""
        Execute *cmd* in a subprocess, using *encoding* to convert to and from binary data written
        or read from/to the subprocess's input, output and error streams.

        Additional keyword arguments are as specified by :py:func:`subprocess.Popen.__init__`
        method.

        """
        self._encoding = encoding
        if self._encoding is None:
            self._encoding = locale.getpreferredencoding()
        super(NonblockingPopen, self).__init__(cmd, **kwargs)

    def recv(self, maxsize=None):
        r"""Receive at most *maxsize* bytes from the subprocess's standard output."""
        return self._recv('stdout', maxsize)
    
    def recv_err(self, maxsize=None):
        r"""Receive at most *maxsize* bytes from the subprocess's standard error."""
        return self._recv('stderr', maxsize)

    def send_recv(self, input_='', maxsize=None):
        r"""
        Send *input_* to the subprocess's standard input and then receive at most *maxsize* bytes
        from both its standard output and standard error.

        """
        return self.send(input_), self.recv(maxsize), self.recv_err(maxsize)

    def get_conn_maxsize(self, which, maxsize):
        r"""
        Return *which* output pipe (either stdout or stderr) and *maxsize* constrained to the 
        [1, 1024] interval in a tuple.
        
        """
        if maxsize is None:
            maxsize = 1024
        elif maxsize < 1:
            maxsize = 1
        return getattr(self, which), maxsize
    
    def _close(self, which):
        getattr(self, which).close()
        setattr(self, which, None)
    
    if mswindows:
        def send(self, input_):
            r"""Send *input_* to the subprocess's standard input."""
            if not self.stdin:
                return None

            try:
                x = msvcrt.get_osfhandle(self.stdin.fileno())
                (errCode, written) = WriteFile(x, bytearray(input_, self._encoding))
            except ValueError:
                return self._close('stdin')
#            except (subprocess.pywintypes.error, Exception):
            except pywintypes.error:
                why = sys.exc_info()[1]
                if why.winerror in (109, errno.ESHUTDOWN):
                    return self._close('stdin')
                raise

            return written

        def _recv(self, which, maxsize):
            conn, maxsize = self.get_conn_maxsize(which, maxsize)
            if conn is None:
                return None
            
            try:
                x = msvcrt.get_osfhandle(conn.fileno())
                (read, nAvail, nMessage) = PeekNamedPipe(x, 0)
                if maxsize < nAvail:
                    nAvail = maxsize
                if nAvail > 0:
                    (errCode, read) = ReadFile(x, nAvail, None)
            except ValueError:
                return self._close(which)
#            except (subprocess.pywintypes.error, Exception):
            except pywintypes.error:
                why = sys.exc_info()[1]
                if why.winerror in (109, errno.ESHUTDOWN):
                    return self._close(which)
                raise
            
            if self.universal_newlines:
                read = self._translate_newlines(read, self._encoding)
            else:
                read = read.decode(self._encoding)
            return read

    else:
        def send(self, input_):
            r"""Send *input_* to the subprocess's standard input."""
            if not self.stdin:
                return None

            if not select.select([], [self.stdin], [], 0)[1]:
                return 0

            try:
                written = os.write(self.stdin.fileno(), bytearray(input_, self._encoding))
            except OSError:
                why = sys.exc_info()[1]
                if why[0] == errno.EPIPE: #broken pipe
                    return self._close('stdin')
                raise

            return written

        def _recv(self, which, maxsize):
            conn, maxsize = self.get_conn_maxsize(which, maxsize)
            if conn is None:
                return None
            
            flags = fcntl.fcntl(conn, fcntl.F_GETFL)
            if not conn.closed:
                fcntl.fcntl(conn, fcntl.F_SETFL, flags| os.O_NONBLOCK)
            
            try:
                if not select.select([conn], [], [], 0)[0]:
                    return ''
                
                r = conn.read(maxsize)
                if not r:
                    return self._close(which)
    
                if self.universal_newlines:
                    r = self._translate_newlines(r)
                else:
                    r = r.decode(self._encoding)
                return r
            finally:
                if not conn.closed:
                    fcntl.fcntl(conn, fcntl.F_SETFL, flags)

message = "Other end disconnected!"

def recv_some(p, t=.1, e=1, tr=5, stderr=0):
    r"""
    Try and receive data from :py:class:`.NonblockingPopen` object *p*'s stdout in at most *tr* tries and
    with a timeout of *t*. If *stderr* is True receive from the subprocess's stderr instead.
    
    """
    if tr < 1:
        tr = 1
    x = time.time()+t
    y = []
    r = six.b('')
    pr = p.recv
    if stderr:
        pr = p.recv_err
    while time.time() < x or r:
        r = pr()
        if r is None:
            if e:
                raise Exception(message)
            else:
                break
        elif r:
            y.append(r)
        else:
            time.sleep(max((x-time.time())/tr, 0))
    return ''.join(y)
    
def send_all(p, data):
    r"""Send all of *data* to :py:class:`.NonblockingPopen` object *p*'s stdin."""
    while len(data):
        sent = p.send(data)
        if sent is None:
            raise Exception(message)
        data = data[sent:-1]
