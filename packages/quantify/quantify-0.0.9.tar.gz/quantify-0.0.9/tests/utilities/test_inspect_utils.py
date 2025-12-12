"""Unit tests for inspect_utils module."""

from quantify.data import types
from quantify.utilities import inspect_utils


def test_get_classes() -> None:
    classes = inspect_utils.get_classes(types)
    assert "TUID" in classes
    assert isinstance(classes["TUID"], type)


def test_get_functions() -> None:
    # Arrange
    expected = {
        "get_members_of_module": inspect_utils.get_members_of_module,
        "get_classes": inspect_utils.get_classes,
        "get_functions": inspect_utils.get_functions,
        "display_source_code": inspect_utils.display_source_code,
    }

    # Act
    functions = inspect_utils.get_functions(inspect_utils)

    # Assert
    assert functions == expected
