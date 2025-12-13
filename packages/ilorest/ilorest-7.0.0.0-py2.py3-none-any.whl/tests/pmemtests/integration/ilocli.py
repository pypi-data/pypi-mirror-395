from __future__ import absolute_import

import sys
import time
from contextlib import contextmanager

import paramiko


class IloCli(object):
    """Wrapper for the iLO CLI (SMASH CLP)."""

    def __init__(self, hostname, username=None, password=None, port=22, timeout=10, window_size=None):
        """Initialize an iLO CLI instance.

        :param hostname: iLO hostname
        :param username: iLO username
        :param password: iLO password
        :param port: SSH port
        :param window_size: window size for the SSH session (max is used if not specified)
        :param timeout: connection timeout, in seconds
        """
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.timeout = timeout
        self.window_size = window_size if window_size else paramiko.common.MAX_WINDOW_SIZE
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.channel = None

    def open(self):
        """Start an interactive iLO CLI session."""
        self.ssh.connect(self.hostname, username=self.username, password=self.password,
                         port=self.port, timeout=self.timeout, look_for_keys=False)
        transport = self.ssh.get_transport()
        self.channel = transport.open_session(window_size=self.window_size)
        self.channel.get_pty()
        self.channel.invoke_shell()

    def close(self):
        """End the iLO CLI session."""
        if self.channel:
            self.channel.close()
        self.ssh.close()

    def __enter__(self):
        for _ in range(5):
            try:
                self.open()
                return self
            except paramiko.SSHException:
                sys.stdout.write("SSHException: retrying connection")
                time.sleep(30)

        sys.stdout.write("SSH: Max retries attempted. No vsp will be captured.")
        return None

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def read(self):
        """Read all available output without blocking I/O."""
        buf = []
        while self.channel.recv_ready():
            data = self.channel.recv(1024)
            buf.append(data)
        return "".join(buf)

    def send(self, data):
        self.channel.send(data)

    def sendline(self, data):
        self.send(data + '\n')

    @contextmanager
    def vsp_session(self):
        """Start a Virtual Serial Port session, returning to the CLI afterward."""
        self.sendline("vsp")
        yield self
        self.send("\x1B(")  # press 'ESC ('
