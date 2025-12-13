"""
conftest.py is used to set up shared fixtures, plugins, hooks, other config etc.
This is the conftest.py for integration tests
http://docs.pytest.org/en/latest/writing_plugins.html#conftest-py-local-per-directory-plugins
"""
from __future__ import absolute_import

import logging
import re
import sys

import pytest

from ..functional.conftest import RestClient, ilorest, test_server
from .ilocli import IloCli
from .ilodebug import IloDebugger

ilo_debug_logger = logging.getLogger('ilodebug')
vsp_logger = logging.getLogger('vsp')


def pytest_configure(config):
    # configure logging
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

    ilo_debug_file = config.getoption('--ilodebug')
    if ilo_debug_file:
        sys.stdout.write("logging iLO debugger output to: {}".format(ilo_debug_file))
        ilo_debug_logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(ilo_debug_file, mode='wb+')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        ilo_debug_logger.addHandler(fh)

    vsp_file = config.getoption('--vsp')
    if vsp_file:
        sys.stdout.write("logging iLO Virtual Serial Port output to: {}".format(vsp_file))
        vsp_logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(vsp_file, mode='wb+')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        vsp_logger.addHandler(fh)


def pytest_runtest_makereport(item, call):
    # incremental testing marker
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item


def pytest_runtest_setup(item):
    # incremental testing marker
    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail("previous test failed (%s)" % previousfailed.name)


@pytest.fixture(scope='session', autouse=True)
def clear_nand_counters(test_server, request):
    """Clear all iLO NAND write counters using the iLO debugger."""
    if request.config.getoption('--clear-nand-counters'):
        with IloDebugger(test_server.hostname) as ilo_debugger:
            sys.stdout.write("Clearing all iLO NAND write counters (setting timers to max)")
            output = ilo_debugger.run("otmax all")
            assert "Set daily timer to MAX value" in output, \
                "Failed to clear NAND write counters:\n {}".format(output)


@pytest.fixture
def ilodebug(test_server, request):
    """Start an iLO debugger session and log all output."""
    if request.config.getoption('--ilodebug'):
        test_path = request.node.nodeid.replace('::()::', '::')
        ilo_debug_logger.info(test_path)

        with IloDebugger(test_server.hostname) as ilo_debugger:
            # get current system time
            output = ilo_debugger.run('id')
            ilo_debug_logger.debug(output)
            yield ilo_debugger
            output = ilo_debugger.read()
            if output:
                ilo_debug_logger.debug('\n' + output)
    else:
        yield


@pytest.fixture
def vsp(test_server, request, set_uefi_debug):
    """Start an iLO Virtual Serial Port session and log all output."""
    if request.config.getoption('--vsp'):
        test_path = request.node.nodeid.replace('::()::', '::')
        vsp_logger.info(test_path)

        hostname = test_server.hostname
        username, password = test_server.username, test_server.password

        with IloCli(hostname, username, password) as cli:
            if cli is None:
                yield
            else:
                # get current system time
                cli.sendline("time")
                with cli.vsp_session():
                    yield cli
                output = cli.read()
                if output:
                    vsp_logger.debug('\n' + output)
    else:
        yield


@pytest.fixture
def set_uefi_debug(test_server, request):
    """Temporarily set the UEFI serial debug level using the iLO debugger.

    The debug levels are: 0 (Disabled), 1 (ErrorsOnly), 2 (Medium), 3 (Verbose).
    """
    new_dbg = request.config.getoption('--uefi-debug-level')
    if new_dbg is not None:
        with IloDebugger(test_server.hostname) as debugger:
            # save the current debug level
            output = debugger.run("evs name cqhdbg")
            match = re.search('EVS NAME "CQHDBG".+\n.+([0-9]{2})', output)
            current_dbg = "0x{}".format(match.group(1)) if match else None

            sys.stdout.write("setting UEFI serial debug level to {} (current {})".format(new_dbg, current_dbg))
            debugger.run("evs xset cqhdbg {}".format(new_dbg))

        yield
        # restore previous debug level
        if current_dbg:
            with IloDebugger(test_server.hostname) as debugger:
                debugger.run("evs xset cqhdbg {}".format(current_dbg))
    else:
        yield
