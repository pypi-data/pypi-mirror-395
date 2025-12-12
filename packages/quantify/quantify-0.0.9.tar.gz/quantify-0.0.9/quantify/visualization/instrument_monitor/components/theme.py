# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""Shared UI theme elements for the instrument monitor."""

from __future__ import annotations

from bokeh.models import Div

STYLES: dict[str, dict[str, str | None]] = {
    "card": {
        "background-color": "#ffffff",
        "border": "1px solid #e1e5e9",
        "border-radius": "12px",
        "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.05)",
        "padding": "16px",
        "margin": "8px",
    },
    "table": {
        "font-family": "'Segoe UI', -apple-system BlinkMacSystemFont, sans-serif",
        "border-radius": "6px",
        "border": "1px solid #e1e5e9",
    },
    "header": {
        "margin": "0",
        "font-family": "Segoe UI, sans-serif",
        "font-size": "16px",
        "font-weight": "500",
        "color": "#1f2937",
    },
    "empty_state": {
        "color": "#6b7280",
        "font-family": "Segoe UI, sans-serif",
        "font-size": "13px",
        "text-align": "center",
        "padding": "8px 4px",
        "margin": "4px 0 0 0",
        "white-space": "pre-line",
    },
}


def create_header(title: str, icon: str) -> Div:
    """Create a styled header with icon."""
    style_str = "; ".join(f"{k}: {v}" for k, v in STYLES["header"].items())
    return Div(
        text=f"<h3 style='{style_str}'>{icon} {title}</h3>",
        styles={"margin-bottom": "16px"},
    )
