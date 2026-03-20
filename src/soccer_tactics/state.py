"""Session state management."""

from __future__ import annotations

import streamlit as st

from soccer_tactics.constants import DEFAULT_FORMATION
from soccer_tactics.formations import get_formation, mirror_positions
from soccer_tactics.models import BoardState, Player


def _make_players(
    positions: list[tuple[float, float]],
    team: str,
) -> list[Player]:
    """Create a list of Player objects from position tuples."""
    return [
        Player(id=i, number=i + 1, x=x, y=y, team=team)
        for i, (x, y) in enumerate(positions)
    ]


def _make_ball() -> Player:
    """Create the ball at the center of the field."""
    return Player(id=0, number=0, x=52.5, y=34.0, team="ball")


def init_state() -> None:
    """Initialize session state if not already set."""
    if "board_state" not in st.session_state:
        reset_to_formation(DEFAULT_FORMATION, DEFAULT_FORMATION)
    if "state_version" not in st.session_state:
        st.session_state.state_version = 0
    if "mode" not in st.session_state:
        st.session_state.mode = "move"


def reset_to_formation(
    home_formation: str,
    away_formation: str,
) -> None:
    """Reset the board to the given formations."""
    home_pos = get_formation(home_formation)
    away_pos = mirror_positions(get_formation(away_formation))
    state = BoardState(
        home_players=_make_players(home_pos, "home"),
        away_players=_make_players(away_pos, "away"),
        ball=_make_ball(),
        arrows=[],
    )
    st.session_state.board_state = state
