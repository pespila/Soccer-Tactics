"""Main Streamlit app for the Soccer Tactics Board."""

from __future__ import annotations

import streamlit as st

from soccer_tactics.component import tactics_board
from soccer_tactics.formations import FORMATION_NAMES
from soccer_tactics.io_utils import export_png_button, load_tactic, save_tactic
from soccer_tactics.models import BoardState
from soccer_tactics.state import (
    init_state,
    redo,
    reset_to_formation,
    undo,
    update_from_component,
)

st.set_page_config(
    page_title="Soccer Tactics Board",
    page_icon="\u26bd",
    layout="wide",
)

init_state()

# ----- Sidebar -----
with st.sidebar:
    st.title("Soccer Tactics Board")

    home_formation = st.selectbox(
        "Home Formation",
        FORMATION_NAMES,
        key="home_formation_select",
    )
    away_formation = st.selectbox(
        "Away Formation",
        FORMATION_NAMES,
        key="away_formation_select",
    )

    if st.button("Apply Formations", use_container_width=True):
        reset_to_formation(home_formation, away_formation)
        st.rerun()

    st.divider()

    home_color = st.color_picker("Home Color", "#1e56a0", key="home_color")
    away_color = st.color_picker("Away Color", "#d32f2f", key="away_color")

    st.divider()

    mode = st.radio(
        "Mode",
        ["move", "arrow"],
        format_func=lambda x: "Move Players" if x == "move" else "Draw Arrows",
        horizontal=True,
        key="mode_radio",
    )
    st.session_state.mode = mode

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Undo", use_container_width=True):
            undo()
            st.rerun()
    with col2:
        if st.button("Redo", use_container_width=True):
            redo()
            st.rerun()

    if st.button("Clear Arrows", use_container_width=True):
        state: BoardState = st.session_state.board_state
        if state.arrows:
            from soccer_tactics.state import push_undo

            push_undo()
            state.arrows = []
            st.rerun()

    st.divider()

    save_tactic(st.session_state.board_state)

    loaded = load_tactic()
    if loaded is not None:
        st.session_state.board_state = loaded
        st.session_state.undo_stack = []
        st.session_state.redo_stack = []
        st.rerun()

    st.divider()

    # Player name editing
    with st.expander("Edit Home Players"):
        state = st.session_state.board_state
        for p in state.home_players:
            p.name = st.text_input(
                f"#{p.number}",
                value=p.name,
                key=f"home_name_{p.id}",
            )

    with st.expander("Edit Away Players"):
        state = st.session_state.board_state
        for p in state.away_players:
            p.name = st.text_input(
                f"#{p.number}",
                value=p.name,
                key=f"away_name_{p.id}",
            )

# ----- Main Area -----
state: BoardState = st.session_state.board_state

all_players = [p.model_dump() for p in state.home_players] + [
    p.model_dump() for p in state.away_players
]

result = tactics_board(
    players=all_players,
    ball=state.ball.model_dump(),
    arrows=[a.model_dump() for a in state.arrows],
    mode=st.session_state.mode,
    home_color=home_color,
    away_color=away_color,
    key="tactics_board",
)

if result is not None:
    # Check for PNG export
    if "png" in result:
        export_png_button(result["png"])

    update_from_component(result)

st.caption(
    "Drag players and the ball to reposition. "
    "Switch to arrow mode to draw tactical arrows. "
    "Use Undo/Redo to navigate changes."
)
