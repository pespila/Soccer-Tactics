"""Custom Streamlit component for the soccer tactics board canvas."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import streamlit.components.v1 as components

FRONTEND_DIR = Path(__file__).parent / "frontend"

_component = components.declare_component(
    "soccer_tactics_board",
    path=str(FRONTEND_DIR),
)


def tactics_board(
    players: list[dict[str, Any]],
    ball: dict[str, Any],
    arrows: list[dict[str, Any]],
    mode: str,
    home_color: str,
    away_color: str,
    key: str | None = None,
) -> dict[str, Any] | None:
    """Render the tactics board canvas and return updated state on interaction."""
    return _component(
        players=players,
        ball=ball,
        arrows=arrows,
        mode=mode,
        homeColor=home_color,
        awayColor=away_color,
        key=key,
        default=None,
    )
