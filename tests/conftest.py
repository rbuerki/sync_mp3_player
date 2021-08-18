import sys
from pathlib import Path

import pytest

# Append source code path to sys.path()
sys.path.append(str(Path.cwd().parent / "sync"))


@pytest.fixture
def source_dict():
    """This is the first base df for testing."""
    return {
        "unchanged_1": 5,
        "unchanged_2": 7,
        "new": 3,
        "updated": 4,
    }


@pytest.fixture
def target_dict():
    """This is the first base df for testing."""
    return {
        "unchanged_1": 5,
        "unchanged_2": 7,
        "updated": 3,
        "deleted": 9,
    }
