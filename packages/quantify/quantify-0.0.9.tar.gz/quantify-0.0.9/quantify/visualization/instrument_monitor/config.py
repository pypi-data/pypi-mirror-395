# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""Configuration for instrument monitor ingestion with performance-tuned defaults."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class IngestionConfig(BaseModel):
    """Configuration for minimal memory ingestion behavior.

    Shared across discovery/poller to parameterize warmup and event batching.
    """

    warmup_total_passes: int = Field(2, description="Number of warmup snapshot passes")
    warmup_interval_s: float = Field(2.0, description="Seconds between warmup passes")
    event_batch_limit: int = Field(500, description="Max events drained per tick")

    model_config = ConfigDict(frozen=True)


DEFAULT_INGESTION_CONFIG: IngestionConfig = IngestionConfig(
    warmup_total_passes=5,
    warmup_interval_s=1.0,
    event_batch_limit=10000,
)
