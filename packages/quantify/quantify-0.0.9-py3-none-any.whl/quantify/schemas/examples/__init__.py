# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""Module containing example JSON schemas."""

from quantify.schemas.examples.device_example_cfgs import example_transmon_cfg
from quantify.schemas.examples.utils import load_json_example_scheme

__all__ = ["example_transmon_cfg", "load_json_example_scheme"]
