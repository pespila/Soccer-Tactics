"""Soccer tactics board canvas component using st.components.v1.html().

Uses direct HTML embedding instead of declare_component to avoid
component registration/discovery issues. State flows:
  - Python → JS: embedded as JSON in the HTML string
  - JS → localStorage: drag-drop positions persisted across reruns
  - Save/Export: handled entirely in JS via browser download APIs
  - Load: Python file_uploader → session_state → re-rendered HTML
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import streamlit.components.v1 as components

_TEMPLATE_PATH = Path(__file__).parent / "frontend" / "index.html"
_template_cache: str | None = None


def _load_template() -> str:
    global _template_cache
    if _template_cache is None:
        _template_cache = _TEMPLATE_PATH.read_text(encoding="utf-8")
    return _template_cache


def tactics_board(
    players: list[dict[str, Any]],
    ball: dict[str, Any],
    arrows: list[dict[str, Any]],
    mode: str,
    home_color: str,
    away_color: str,
    state_version: int = 0,
    height: int = 600,
) -> None:
    """Render the tactics board canvas."""
    template = _load_template()

    init_data = json.dumps({
        "players": players,
        "ball": ball,
        "arrows": arrows,
        "mode": mode,
        "homeColor": home_color,
        "awayColor": away_color,
        "stateVersion": state_version,
    })

    html = template.replace("/*__INIT_DATA__*/", f"var INIT_DATA = {init_data};")

    components.html(html, height=height, scrolling=False)
