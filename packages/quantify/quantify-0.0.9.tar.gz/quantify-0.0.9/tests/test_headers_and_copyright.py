# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import datetime
import importlib.util
import os
from pathlib import Path
import pprint

import pytest


def test_header() -> None:
    skipfiles = {
        "__init__.py",
        "conftest.py",
        "setup.py",
        "_version.py",
        "_static_version.py",
        # The "SI_utilities.py" throw a ruff error because its name starts with capital
        # letters. A noqa needs to be added for ruff to not ignore it but that
        # breaks the test. It was decided to skip this file.
        "SI_utilities.py",
    }
    skipdirs = {"docs", ".", "tests", "__pycache__", "venv", "build"}
    failures = []
    quantify_path = Path(__file__).resolve().parent.parent.resolve()
    header_lines = [
        "# Repository: https://gitlab.com/quantify-os/quantify",
        "# Licensed according to the LICENSE file on the main branch",
    ]
    for root, _, files in os.walk(quantify_path):
        # skip hidden folders, etc
        if any(part.startswith(name) for part in Path(root).parts for name in skipdirs):
            continue
        for file_name in files:
            if file_name[-3:] == ".py" and file_name not in skipfiles:
                file_path = Path(root) / file_name
                try:
                    with open(file_path) as file:
                        lines_iter = (line.strip() for line in file)
                        line_matches = [
                            expected_line == line
                            for expected_line, line in zip(header_lines, lines_iter)
                        ]
                        if not all(line_matches):
                            failures.append(str(file_path))
                except OSError:
                    pytest.fail(
                        f"There was a problem while opening the following file: "
                        f"{file_path}"
                    )

    if failures:
        pytest.fail(f"Bad headers:\n{pprint.pformat(failures)}")


def test_docs_copyright() -> None:
    # Path to conf.py
    conf_file = Path(__file__).resolve().parent.parent / "docs" / "source" / "conf.py"

    # Dynamically import conf.py
    spec = importlib.util.spec_from_file_location("conf", conf_file)
    if spec is None:
        return
    conf = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(conf)  # type: ignore

    # Get evaluated copyright
    current_year = str(datetime.datetime.now().year)
    value = getattr(conf, "copyright", "")

    assert current_year in value, f"Expected year {current_year} in copyright: {value}"
    assert "Orange Quantum Systems" in value, "Missing organization name in copyright"
