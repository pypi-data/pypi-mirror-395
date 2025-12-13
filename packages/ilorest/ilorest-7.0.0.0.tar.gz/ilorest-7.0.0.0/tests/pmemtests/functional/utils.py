"""Utilities for functional tests"""
from __future__ import absolute_import

import os
import subprocess
import tempfile
import time
from collections import namedtuple

# For cross-compatibility between Python 2 and Python 3
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

CommandResult = namedtuple('CommandResult', ('stdout', 'stderr', 'retcode'))


def run_cmd(args):
    """Runs a shell command.

    :param args: list of command arguments
    :return: results of the command as a named tuple: (stdout, stderr, retcode)
    """
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    retcode = proc.returncode
    return CommandResult(stdout=stdout, stderr=stderr, retcode=retcode)


def urlparse_auth(url):
    """Extracts the auth section from a URL (e.g. https://user:password@host)."""
    parts = urlparse(url)
    username = parts.username
    password = parts.password
    netloc = parts.netloc.split('@')[-1]
    url = parts._replace(netloc=netloc).geturl()
    return url, username, password


class InteractivePopen(object):
    """Interactive subprocess Popen."""

    def __init__(self, args):
        """Launches an interactive shell as a subprocess.

        :param args: sequence of command arguments or a single string
        """
        fout = tempfile.NamedTemporaryFile('wb', delete=False)
        ferr = tempfile.NamedTemporaryFile('wb', delete=False)
        self.fout = open(fout.name, 'r')
        self.ferr = open(ferr.name, 'r')
        self.proc = subprocess.Popen(args, stdout=fout, stderr=ferr, stdin=subprocess.PIPE)

    def communicate(self, input=None):
        """Interacts with the process and waits for it to terminate.

        :param input: data to send to stdin
        :return: named tuple of (stdout, stderr, retcode)
        """
        self.proc.communicate(input)
        stdout, stderr = self.read()
        retcode = self.proc.returncode

        # clean up
        self.fout.close()
        self.ferr.close()
        os.remove(self.fout.name)
        os.remove(self.ferr.name)

        return CommandResult(stdout=stdout, stderr=stderr, retcode=retcode)

    def send(self, str):
        """Sends data to stdin."""
        self.proc.stdin.write(str)

    def sendline(self, line=""):
        """Sends a newline-terminated string to stdin."""
        self.send(line + '\n')

    def read(self, expect=None, timeout=60, poll_interval=0.1):
        """Reads from stdout and stderr.

        The read is non-blocking unless 'expect' is specified.

        :param expect: string to match in stdout before finishing the read
        :param timeout: time to wait for the expected string, in seconds
        :param poll_interval: poll interval, in seconds
        :return: tuple of (stdout, stderr)
        """
        stdout = ""
        stderr = ""
        time_timeout = time.time() + timeout
        while True:
            out = self.fout.read()
            err = self.ferr.read()
            if out:
                stdout += out
            if err:
                stderr += err

            if expect is None or expect in stdout:
                break

            if time.time() > time_timeout:
                break

            time.sleep(poll_interval)

        return stdout, stderr
