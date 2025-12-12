"""Pytest configuration for Quantify tests.

Ensures test helpers are discovered and test data is copied into a temp directory.
"""

import os
from pathlib import Path

import pytest
from pytest import FixtureRequest, TempPathFactory

from quantify.data.handling import set_datadir
from quantify.utilities._tests_helpers import (
    get_test_data_dir,
    remove_target_then_copy_from,
    rmdir_recursive,
)

# Prevent QT windows from popping up during test runs
os.environ["QT_QPA_PLATFORM"] = "offscreen"


@pytest.fixture(scope="session", autouse=True)
def tmp_test_data_dir(
    request: FixtureRequest, tmp_path_factory: TempPathFactory
) -> Path:
    """
    Fixture which uses the pytest tmp_path_factory fixture
    and extends it by copying the entire contents of the test_data
    directory. After the test session is finished, then it calls
    the `cleanup_tmp` method which tears down the fixture and cleans up itself.

    Returns
    -------
    Path
        Temporary test data directory path.

    """
    temp_data_dir = tmp_path_factory.mktemp("temp_data")
    remove_target_then_copy_from(source=get_test_data_dir(), target=temp_data_dir)
    set_datadir(str(temp_data_dir))

    def cleanup_tmp() -> None:
        rmdir_recursive(root_path=temp_data_dir)

    request.addfinalizer(cleanup_tmp)

    return temp_data_dir
