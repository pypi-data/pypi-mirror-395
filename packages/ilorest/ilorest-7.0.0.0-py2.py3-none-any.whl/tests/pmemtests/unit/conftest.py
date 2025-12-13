"""
conftest.py is used to set up shared fixtures, plugins, hooks, other config etc.
This is the unit test conftest.py
http://docs.pytest.org/en/latest/writing_plugins.html#conftest-py-local-per-directory-plugins
"""
from __future__ import absolute_import

import pytest

from ..conftest import (
    ClearPendingConfigCommand,
    DisplayHelpers,
    MapperRenderers,
    RestHelpers,
    ShowPmemCommand,
)
