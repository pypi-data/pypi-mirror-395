"""ilomock module"""
from __future__ import absolute_import

import os
import subprocess
import sys

import requests

JAVA_BIN = os.getenv('JAVA_BIN', 'java')
ILOMOCK_JAR = os.getenv('ILOMOCK_JAR')

os.environ['NO_PROXY'] = 'localhost'

# ignore SSL warnings
# requests.packages.urllib3.disable_warnings()


class MockServerError(Exception):
    """An error occurred starting the mock server."""


class MockServer(object):
    """Wrapper for ilomock."""

    def __init__(self, profile_dir=None, port=0):
        """Initializes a mock server.

        :param profile_dir: path to the server profile to use
        :param port: port to listen on
        """
        self.profile_dir = profile_dir
        self.port = port
        self.url = None
        self.proc = None

    def start(self):
        """Starts the mock server.

        :raises MockServerError: if the server failed to start
        """
        if not ILOMOCK_JAR:
            raise MockServerError("ILOMOCK_JAR must be set")

        sys.stdout.write("Starting mock server on port {} with profile {}".format(self.port, self.profile_dir))

        args = [JAVA_BIN, '-jar', ILOMOCK_JAR, '-p', str(self.port)]
        if self.profile_dir:
            args.extend(['-s', self.profile_dir])
        if not os.path.exists(JAVA_BIN):
            raise IOError("JAVA_BIN location does not exist: {}".format(JAVA_BIN))
        proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        # Block until the server starts or fails
        output = []
        for line in iter(proc.stdout.readline, ''):
            output.append(line)
            prefix = "Listening on port "
            if line.startswith(prefix):
                self.proc = proc
                self.port = int(line[len(prefix):])
                self.url = "https://localhost:{}".format(self.port)
                return

        proc.communicate()
        output = ''.join(output)
        raise MockServerError("Failed to start ilomock: {}\n{}".format(proc.returncode, output))

    def stop(self):
        """Stops the running mock server."""
        if self.proc:
            self.proc.kill()
            self.proc = None
            self.url = None

    def __enter__(self):
        """Starts the mock server and returns it."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Ensures the running mock server stops."""
        self.stop()

    def patch(self, path, data):
        """Patches a resource in the mock server."""
        payload = {'path': path, 'data': data}
        resp = requests.post(self.url + '/admin/patch', json=payload, verify=False)
        assert resp.status_code == 200, "Failed to patch mock server: {}\n{}"\
                                        .format(resp.status_code, resp.text)

    def load(self, profile_dir):
        """Loads a new server profile while the mock server is running."""
        config = {'serverProfile': profile_dir}
        resp = requests.post(self.url + '/admin/load', json=config, verify=False)
        assert resp.status_code == 200, "Failed to load mock server: {}\n{}"\
                                        .format(resp.status_code, resp.text)
