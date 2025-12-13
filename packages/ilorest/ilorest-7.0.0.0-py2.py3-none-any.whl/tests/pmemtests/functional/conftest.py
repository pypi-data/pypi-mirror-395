"""
conftest.py is used to set up shared fixtures, plugins, hooks, other config etc.
This is the functional test conftest.py
http://docs.pytest.org/en/latest/writing_plugins.html#conftest-py-local-per-directory-plugins
"""
from __future__ import absolute_import

import os
import re
import sys
from contextlib import contextmanager

import pytest

import redfish

# For cross-compatibility between Python 2 and Python 3
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from ..conftest import RDMC_FILE
from . import utils
from .ilomock import MockServer


@pytest.fixture(scope='session')
def mock_server():
    with MockServer() as server:
        yield server


@pytest.fixture
def dl360_large(mock_server):
    """Returns a mock server config:

      - DL360 Gen10
      - 1x AEP DIMM
      - 1x DRAM DIMM
    """
    data_dir = os.path.join(os.path.dirname(__file__), 'mockdata/dl360-large')
    mock_server.load(data_dir)
    return MockServerConfig(mock_server, username='rev', password='hpe123')


@pytest.fixture
def dl360_memfast_disabled(dl360_large):
    """Returns a dl360_configured config with MemFastTraining disabled
    """
    dl360_large.patch('/redfish/v1/systems/1/bios/settings/', {'Attributes': {'MemFastTraining': 'Disabled'}})

    return dl360_large


@pytest.fixture(scope='session')
def test_server():
    """Returns a server config specified by the TEST_SERVER environment variable.

    TEST_SERVER should be a URL with optional auth, e.g. https://user:password@host:port
    """
    if 'TEST_SERVER' not in os.environ:
        pytest.skip("TEST_SERVER not set")

    url, username, password = utils.urlparse_auth(os.getenv('TEST_SERVER'))
    # If no credentials, then populate with hard-coded values. Credentials required by ilorest.
    username = "orange" if username is None else username
    password = "password" if password is None else password
    return ServerConfig(url=url, username=username, password=password)


@pytest.fixture
def ilorest(tmpdir):
    """Returns an ilorest session (in scripting mode by default).

    Each ilorest session receives its own unique temporary cache directory.
    """
    yield Ilorest(cache_dir=tmpdir.dirname)
    tmpdir.remove(ignore_errors=True)


class ServerConfig(object):

    def __init__(self, url=None, username=None, password=None):
        self.url = url
        self.username = username
        self.password = password

    @property
    def config(self):
        return self.url, self.username, self.password

    @property
    def hostname(self):
        parts = urlparse(self.url)
        hostname = parts.hostname if parts.scheme else self.url
        return hostname


class MockServerConfig(ServerConfig):

    def __init__(self, server, username=None, password=None):
        super(MockServerConfig, self).__init__(url=server.url, username=username, password=password)
        self.server = server

    def patch(self, path, data):
        """Patches a resource in the mock server."""
        self.server.patch(path, data)


class Ilorest(object):
    """Wrapper for the iLO RESTful Interface Tool."""

    def __init__(self, cache_dir=None):
        """Starts ilorest in scripting mode.

        :param cache_dir: directory to use for caching instead of the default global location
        """
        self.cache_dir = cache_dir
        self.args = [sys.executable, RDMC_FILE]

        if cache_dir:
            self.args.append('--cache-dir={}'.format(cache_dir))

        self.interactive = False
        self.proc = None
        self.prompt = "iLOrest > "

    def run(self, args, sendline=None):
        """Runs an ilorest command.

        :param args: list of command arguments
        :param sendline: string to send after running (only used in interactive mode)
        :return: results of the command as a named tuple: (stdout, stderr, retcode)
        """
        if not self.interactive:
            return utils.run_cmd(self.args + args)

        # interactive mode
        cmd_line = ' '.join(args)
        self.proc.sendline(cmd_line)
        if sendline:
            self.proc.sendline(sendline)

        stdout, stderr = self.proc.read(expect=self.prompt)

        match = re.search("iLOrest return code: ([0-9]+)\n", stdout)
        retcode = int(match.group(1)) if match else None

        return utils.CommandResult(stdout=stdout, stderr=stderr, retcode=retcode)

    def login(self, url=None, username=None, password=None):
        """Logs in to the server and establishes a secure session.

        :param url: iLO server url if connecting remotely
        :param username: iLO username. If no username specified, use "orange"
        :param password: iLO password. If no password specified, use "password"
        """
        args = ['login']
        if url:
            args.append(url)
        if username:
            args.extend(['-u', username])
        if password:
            args.extend(['-p', password])

        results = self.run(args)
        assert results.retcode == 0, "Failed to connect or log in"

    def logout(self):
        """Ends the current session and disconnects from the server."""
        self.run(['logout'])

    @contextmanager
    def session(self, url=None, username=None, password=None):
        """Establishes a session with an iLO server and logs out afterwards."""
        self.login(url=url, username=username, password=password)
        yield self
        self.logout()

    @contextmanager
    def interactive_session(self, url=None, username=None, password=None):
        """Establishes an interactive session with an iLO server, and logs out and exits afterwards."""
        with self.interactive_mode(), self.session(url=url, username=username, password=password):
            yield self

    @contextmanager
    def interactive_mode(self):
        """Enters interactive mode and exits afterwards."""
        # use --verbose to extract the return code
        self.proc = utils.InteractivePopen(self.args + ['--verbose'])
        self.proc.read(expect=self.prompt)
        self.interactive = True
        yield self
        self.proc.communicate('exit')
        self.interactive = False


class RestClient(object):
    """REST client for an iLO server."""

    def __init__(self, url=None, username=None, password=None):
        """Initializes an iLO REST client.

        :param url: iLO server url if connecting remotely
        :param username: iLO username
        :param password: iLO password
        """
        # if no scheme/protocol defined, try https
        if "://" not in url:
            url = "https://" + url
        self._client = redfish.redfish_client(base_url=url, username=username, password=password)
        self._client.login(auth=redfish.AuthMethod.BASIC)

    def get(self, path):
        """Sends a GET request."""
        resp = self._client.get(path)
        return resp.dict

    def patch(self, path, body):
        """
        Sends a PATCH request to the path with the given body
        :param path: URI path
        :param body: the body of the patch. For example dict:{ "Attributes": { "Prop1": true } }
        :return: RestResponse status, RestResponse dictionary
        """
        rest_response = self._client.patch(path=path, body=body)
        return rest_response.status, rest_response.dict
