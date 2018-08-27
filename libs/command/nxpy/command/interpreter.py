# nxpy.core package ----------------------------------------------------------

# Copyright Nicola Musatti 2008 - 2014
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See http://nxpy.sourceforge.net for library home page. ---------------------

r"""
Interactive program driver.

"""

from __future__ import absolute_import

import os
import re
import subprocess
import sys
import time

import six

import nxpy.core.async_subprocess
import nxpy.command.error


# Output prefixes

OUTPUT  = "OUT> "
ERROR   = "ERR> "
EXCEPT  = "EXC> "
COMMAND = "CMD> "


# Type of output

FILE = 0
STRING = 1


def _format(input_, output=STRING, type_=OUTPUT):
    r"""
    Prepends a prefix to each *input_* line as specified by *type_* and copies it to *output*.
    Returns *output*.

    """
    if type_ not in ( OUTPUT, ERROR, EXCEPT, COMMAND ):
        raise nxpy.command.error.BadLogFormat(str(type_) + ": Unknown format")
    if isinstance(input_, six.string_types):
        if input_ and input_[-1] != '\n':
            input_ = input_ + '\n'
        input_ = six.StringIO(input_)
    if output in ( FILE, STRING ):
        out = six.StringIO()
    else:
        out = output
    for line in input_:
        out.write(type_)
        out.write(line)
    if output == STRING:
        return out.getvalue()
    return out


class BadCommand(Exception):
    r"""Raised on a command execution failure"""
    
    def __init__(self, cmd, err):
        r"""Takes the failed command and the contents of the error stream."""
        self.command = cmd
        self.stderr = err
        msg = _format(cmd, FILE, COMMAND)
        if err:
            msg = _format(err, msg, ERROR)
        super(BadCommand, self).__init__("".join(msg))


EXP_OUT = 0
EXP_ERR = 1

def waitOutput(out, err):
    r"""Wait for any output."""
    return out

def waitError(out, err):
    r"""Wait for any error."""
    return err


class LineWaiter(object):
    r"""Wait for *count* lines of output."""
    def __init__(self, count):
        self.count = count
        self.n = 0
        
    def __call__(self, out, err):
        self.n += out.count('\n')
        return self.n >= self.count


class StringWaiter(object):
    r"""Wait for a specific *string* in the *where* stream."""
    def __init__(self, string, where):
        self.string = string
        self.where = where
    
    def __call__(self, out, err):
        if self.where == EXP_OUT:
            o = out
        else:
            o = err
        return o.find(self.string) != -1


class RegexpWaiter(object):
    r"""Wait for a match to a given *regexp*, passed either compiled or as a string."""
    def __init__(self, regexp, where):
        if isinstance(regexp, six.string_types):
            self.regexp = re.compile(regexp, re.MULTILINE)
        else:
            self.regexp = regexp
        self.where = where
    
    def __call__(self, out, err):
        if self.where == EXP_OUT:
            o = out
        else:
            o = err
        return self.regexp.search(o)


class Timer(object):
    r"""
    A collaborative timer class.
    Support a polling mechanism by keeping track of the amount of time to wait before the next
    attempt, according to different policies.
    
    """    
    def __init__(self, timeout=0, retries=0, interval=0.1, quantum=0.01):
        """
        Specify an overall *timeout*, a number of *retries* and/or an *interval* between them.
        The next attempt will not take place before a *quantum* has passed. Timings are expressed
        in seconds. If a timeout is specified it will take precedence over the other arguments; in
        that case the number of retries will take precedence over the interval. If neither a timeout
        nor a number of retries are specified the overall timer will never expire.
        
        """
        if retries < 0:
            raise nxpy.command.error.TimerError("retries must be equal or greater than 0")
        elif retries == 0:
            self.retries = -1
        else:
            self.retries = retries
        self.count = 0
        self.interval = interval
        if timeout > 0:
            self.timeout = timeout
            self.end = time.time() + timeout
            if retries > 1:
                self.interval = timeout / retries
        else:
            self.timeout = 0
            self.end = 0
        if quantum < 0:
            raise nxpy.command.error.TimerError("quantum must be equal or greater than 0")
        self.quantum = quantum

    def getInterval(self):
        r"""
        Return the next wait interval.
        Call after each attempt in order to know how long to wait for.
        
        """
        if self.end and self.retries > 1:
            self.interval = max((self.end-time.time())/self.retries, self.quantum)
        return self.interval

    def expired(self):
        r"""
        Indicate whether the current timer expired.
        Use as polling loop control condition.
        
        """
        self.count += 1
        return self.timeout and self.end < time.time() or ( self.retries - self.count == 0 )

    def reset(self):
        r"""Reset the timer."""
        self.count = 0
        if self.timeout:
            self.end = time.time() + self.timeout


class BaseInterpreter(object):
    r"""
    Controls the execution of an interactive program in a sub-process.
    Provides means to send input to the controlled process and to check different conditions on its
    output and error streams.
    
    """
    def __init__(self, popen):
        r"""
        Creates an interpreter instance. *popen* is a :py:class:`.Popen`-like object which must
        support non-blocking I/O.
        
        """
        self.log = False
        self.popen = popen

    def setLog(self, log):
        r"""
        If *log* is *True*, enable logging of command output and error, otherwise disable it.
        
        """
        self.log = log
        
    def _log(self, log):
        r"""
        Check whether logging should be enabled. Usually *log* is passed from the calling method.
        
        """
        if log != None:
            return log
        else:
            return self.log

    def send_cmd(self, cmd, log=None):
        r"""
        Write *cmd* to the interpreter's input, optianally logging it. If *log* is not *None*,
        override the global setting.
        
        """
        try:
            if self._log(log):
                _format(cmd, sys.stderr, COMMAND)
            self.popen.send(cmd + os.linesep)
        except Exception:
            e = sys.exc_info()[1]
            raise BadCommand(cmd, str(e.args))
            
    def expect_any(self, **kwargs):
        r"""Expect any output."""
        return self.expect(waitOutput, **kwargs)

    def expect_lines(self, count=1, **kwargs):
        r"""Expect *count* lines of output."""
        return self.expect(LineWaiter(count), **kwargs)
    
    def expect_string(self, string, where=EXP_OUT, **kwargs):
        r"""Expect a *string* in the *where* stream."""
        return self.expect(StringWaiter(string, where), **kwargs)  

    def expect_regexp(self, regexp, where=EXP_OUT, **kwargs):
        r"""
        Expect to find a match for the *regexp* regular expression within the *where* stream.
        
        """
        return self.expect(RegexpWaiter(regexp, where), **kwargs)  

    def expect(self, cond=None, timeout=0, retries=0, interval=0.01, 
            quantum=0.01, raise_on_error=True, log=None):
        r"""
        Express expectations on the outcome of a command.
        
        *cond* is a two argument callable which will be passed the command's standard output and
        standard error, and which should return *True* if the expectation is satisfied. For the
        other arguments see the documentation for the :py:class:`.Timer` class.
        
        """
        try:
            out_list = []
            err_list = []
            timer = Timer(timeout, retries, interval, quantum)
            while not timer.expired():
                out = self.popen.recv()
                if out:
                    out_list.append(out)
                err = self.popen.recv_err()
                if err:
                    err_list.append(err)
                if cond and cond(out, err):
                    break
                if out or err:
                    timer.reset()
                    t = timer.quantum
                else:
                    t = timer.getInterval()
                if self._log(log):
                    sys.stderr.write("END: %s  SLEEP: %f  SIZE: %d\n" % 
                            (time.ctime(timer.end), t, len(out) + len(err)))
                if t > 0:
                    time.sleep(t)
            else:
                if cond:
                    raise nxpy.command.error.TimeoutError(err)
        finally:
            out = ''.join(out_list)
            err = ''.join(err_list)
            if self._log(log):
                _format(out, sys.stderr)
                _format(err, sys.stderr, ERROR)
        if raise_on_error and err:
            raise nxpy.command.error.ExpectError(err)
        return out, err

    def run(self, cmd, log=None, **kwargs):
        r"""Executes the command and waits for the expected outcome or an error."""
        self.send_cmd(cmd, log=log)
        kwargs['log'] = log
        try:
            return self.expect(**kwargs)
        except nxpy.command.error.ExpectError:
            e = sys.exc_info()[1]
            raise BadCommand(cmd, e.args[0])


class Interpreter(BaseInterpreter):
    r"""
    The actual Interpreter class.
    
    This implementation uses a :py:class:`.core.async_subprocess.AsyncPopen` instance.
    
    """
    def __init__(self, cmd):
        super(Interpreter, self).__init__(nxpy.core.async_subprocess.AsyncPopen(cmd.split(), 
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE))
