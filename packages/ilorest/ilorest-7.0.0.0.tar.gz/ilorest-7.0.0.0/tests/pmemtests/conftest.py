"""
conftest.py is used to set up shared fixtures, plugins, hooks, other config etc.
This is the global, root-level conftest.py loaded for all tests.
Sub-directories can have their own conftest.py that gets loaded locally for that sub-directory only.
http://docs.pytest.org/en/latest/writing_plugins.html#conftest-py-local-per-directory-plugins
"""
from __future__ import absolute_import

import os
import sys
from importlib import import_module

import pytest

# Add the 'src' directory to the module search path so our tests can import from it
SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ilorest'))
RDMC_FILE = os.path.join(SRC_DIR, 'rdmc.py')

sys.path.insert(0, SRC_DIR)

DisplayHelpers = import_module('extensions.PERSISTENT_MEMORY_COMMANDS.lib.DisplayHelpers')
ShowPmemCommand = import_module('extensions.PERSISTENT_MEMORY_COMMANDS.ShowPmemCommand')
RestHelpers = import_module('extensions.PERSISTENT_MEMORY_COMMANDS.lib.RestHelpers')
Mapper = import_module('extensions.PERSISTENT_MEMORY_COMMANDS.lib.Mapper')
MapperRenderers = import_module('extensions.PERSISTENT_MEMORY_COMMANDS.lib.MapperRenderers')
PmemHelpers = import_module('extensions.PERSISTENT_MEMORY_COMMANDS.lib.PmemHelpers')
ClearPendingConfigCommand = import_module('extensions.PERSISTENT_MEMORY_COMMANDS.ClearPendingConfigCommand')
ApplyPmemConfigCommand = import_module('extensions.PERSISTENT_MEMORY_COMMANDS.ApplyPmemConfigCommand')

def pytest_addoption(parser):
    parser.addoption("--runquix", action="store_true", default=False,
                     help="Run tests associated with an open QuIX (which are skipped by default).")
    parser.addoption("--skipincremental", action="store_true", default=False,
                     help="Skip incremental configuration tests (run by default).")
    parser.addoption("--clear-nand-counters", action="store_true", default=False,
                     help="Clear all iLO NAND write counters using the iLO debugger.")

    logging_group = parser.getgroup('logging', description='logging configuration')
    logging_group.addoption("--ilodebug", metavar='path', help="log iLO debugger output to the specified file.")
    logging_group.addoption("--vsp", metavar='path', help="log Virtual Serial Port output to the specified file.")
    logging_group.addoption("--uefi-debug-level", choices=[0, 1, 2, 3], type=int,
                            help="set UEFI serial debug level when capturing Virtual Serial Port output: "
                                 "0 (Disabled), 1 (ErrorsOnly), 2 (Medium), 3 (Verbose)")


def pytest_runtest_setup(item):
    openquix_marker = item.get_marker("openquix")
    if openquix_marker is not None:
        if item.config.getoption("--runquix") is False:
            pytest.skip("skipping test associated with an open QuIX")


def pytest_collection(session):
    """
    Hook to use testpaths for a test root directory passed in as a pytest argument.
    This allows using testpaths without having to execute pytest from the test root directory.
    """
    args = session.config.args
    testpaths = session.config.getini('testpaths')
    currdir = session.startdir
    rootdir = session.config.rootdir

    if len(args) == 1 and testpaths:
        testdir = args[0]
        if currdir.join(testdir) == rootdir:
            session.config.args = [os.path.join(testdir, testpath) for testpath in testpaths]
