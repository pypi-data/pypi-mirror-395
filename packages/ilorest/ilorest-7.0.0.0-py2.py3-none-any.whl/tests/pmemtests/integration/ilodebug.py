from __future__ import absolute_import

from telnetlib import Telnet


class IloDebugger(object):
    DEBUG_PORT = 8

    def __init__(self, hostname, timeout=10):
        """Initialize an iLO debugger instance.

        :param hostname: hostname of the iLO server
        :param timeout: connection timeout, in seconds
        """
        self.hostname = hostname
        self.timeout = timeout
        self.tn = None
        self.prompt = '\r\n>'

    def open(self):
        """Connect to the iLO debugger."""
        self.tn = Telnet(self.hostname, self.DEBUG_PORT, self.timeout)
        # wait until the debugger is ready and clear initial output
        self.read_until(self.prompt)

    def close(self):
        """Close the connection."""
        if self.tn:
            self.tn.close()
            self.tn = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def read(self):
        """Read all available output without blocking I/O."""
        output = self.tn.read_very_eager()
        # debugger occasionally outputs CRLFs with double CRs - just convert all to LFs
        output = output.replace('\r', '')
        return output

    def read_until(self, expected, timeout=10):
        """Read until an expected string is encountered or the timeout, in seconds, has been reached."""
        output = self.tn.read_until(expected, timeout)
        output = output.replace('\r', '')
        return output

    def writeline(self, line):
        """Write a line to the iLO debugger."""
        self.tn.write(line + '\n')

    def run(self, cmd_line):
        """Run an iLO debugger command and capture output."""
        self.read()  # clear any previous output
        self.writeline(cmd_line)
        output = self.read_until(self.prompt)
        return output
