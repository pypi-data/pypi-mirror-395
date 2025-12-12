# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""Data models for data handling with thread safety."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Reading(BaseModel):
    """Immutable parameter reading with thread safety."""

    full_name: str = Field(
        ...,
        description="Full parameter name (instrument.parameter)",
    )
    instrument: str = Field(..., description="Instrument name")
    parameter: str = Field(..., description="Parameter name")
    value: Any = Field(..., description="Parameter value (any type supported)")
    unit: str | None = Field(None, description="Unit of measurement")
    ts: datetime | None = Field(None, description="Timestamp (timezone-aware UTC)")

    model_config = ConfigDict(frozen=True)  # Immutable for thread safety


class ChangeEvent(BaseModel):
    """Immutable change event for high-throughput processing."""

    reading: Reading = Field(..., description="The new reading after change")
    changed_fields: set[str] = Field(
        ..., description="Fields that changed (value, unit, ts)"
    )
    ts: datetime | None = Field(None, description="Timestamp when change was detected")

    model_config = ConfigDict(frozen=True)  # Immutable for thread safety


class TreeNode(BaseModel):
    """Represents a node in the instrument hierarchy tree (UI view model)."""

    node_id: str
    label: str
    level: int
    is_group: bool
    expanded: bool

    # Immutable: tree view rows should be constructed, not mutated
    model_config = ConfigDict(frozen=True)


class _TreeEntry(BaseModel):
    """Internal recursive tree entry used to build the hierarchy.

    Mutable because children and reading are filled during tree construction.
    """

    name: str
    instrument: str
    path: tuple[str, ...]
    reading: Reading | None = None
    children: dict[str, _TreeEntry] = Field(default_factory=dict)

    # Mutable to allow population during tree building
    model_config = ConfigDict(frozen=False)


# # Resolve forward references for recursive types
# _TreeEntry.model_rebuild()
