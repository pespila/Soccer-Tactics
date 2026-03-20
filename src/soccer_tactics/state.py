"""Session state management with undo/redo support."""

from __future__ import annotations

import streamlit as st

from soccer_tactics.constants import DEFAULT_FORMATION, UNDO_STACK_LIMIT
from soccer_tactics.formations import get_formation, mirror_positions
from soccer_tactics.models import Arrow, BoardState, Player


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
    if "undo_stack" not in st.session_state:
        st.session_state.undo_stack = []
    if "redo_stack" not in st.session_state:
        st.session_state.redo_stack = []
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
    st.session_state.undo_stack = []
    st.session_state.redo_stack = []


def push_undo() -> None:
    """Save current state to undo stack."""
    state: BoardState = st.session_state.board_state
    stack: list[str] = st.session_state.undo_stack
    stack.append(state.model_dump_json())
    if len(stack) > UNDO_STACK_LIMIT:
        stack.pop(0)
    st.session_state.redo_stack = []


def undo() -> bool:
    """Undo last action. Returns True if undo was performed."""
    stack: list[str] = st.session_state.undo_stack
    if not stack:
        return False
    current: BoardState = st.session_state.board_state
    st.session_state.redo_stack.append(current.model_dump_json())
    st.session_state.board_state = BoardState.model_validate_json(stack.pop())
    return True


def redo() -> bool:
    """Redo last undone action. Returns True if redo was performed."""
    stack: list[str] = st.session_state.redo_stack
    if not stack:
        return False
    current: BoardState = st.session_state.board_state
    st.session_state.undo_stack.append(current.model_dump_json())
    st.session_state.board_state = BoardState.model_validate_json(stack.pop())
    return True


def update_from_component(data: dict) -> None:
    """Update board state from component return value."""
    if data is None:
        return

    push_undo()
    state: BoardState = st.session_state.board_state

    if "players" in data:
        for p_data in data["players"]:
            team = p_data.get("team")
            pid = p_data.get("id")
            if team == "home":
                for p in state.home_players:
                    if p.id == pid:
                        p.x = p_data["x"]
                        p.y = p_data["y"]
                        break
            elif team == "away":
                for p in state.away_players:
                    if p.id == pid:
                        p.x = p_data["x"]
                        p.y = p_data["y"]
                        break

    if "ball" in data:
        state.ball.x = data["ball"]["x"]
        state.ball.y = data["ball"]["y"]

    if "arrows" in data:
        state.arrows = [Arrow(**a) for a in data["arrows"]]

    st.session_state.board_state = state
