"""Main Streamlit app for the Soccer Tactics Board."""

from __future__ import annotations

import json

import streamlit as st

from soccer_tactics.component import tactics_board
from soccer_tactics.formations import FORMATION_NAMES
from soccer_tactics.models import BoardState
from soccer_tactics.state import init_state, reset_to_formation

st.set_page_config(
    page_title="Soccer Tactics Board",
    page_icon="\u26bd",
    layout="wide",
)

init_state()


def _post_message(msg_type: str) -> None:
    """Send a postMessage command to the canvas iframe."""
    st.markdown(
        f"""<script>
        (function() {{
            var iframes = parent.document.querySelectorAll('iframe');
            for (var i = 0; i < iframes.length; i++) {{
                iframes[i].contentWindow.postMessage({{type: "{msg_type}"}}, "*");
            }}
        }})();
        </script>""",
        unsafe_allow_html=True,
    )


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
        st.session_state.state_version = st.session_state.get("state_version", 0) + 1
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
            _post_message("undo")
    with col2:
        if st.button("Redo", use_container_width=True):
            _post_message("redo")

    if st.button("Clear Arrows", use_container_width=True):
        _post_message("clearArrows")

    st.divider()

    if st.button("Save Tactic", use_container_width=True):
        _post_message("save")

    uploaded = st.file_uploader("Load Tactic", type=["json"], key="tactic_uploader")
    if uploaded is not None:
        try:
            loaded = BoardState.model_validate_json(uploaded.read())
            st.session_state.board_state = loaded
            st.session_state.state_version = st.session_state.get("state_version", 0) + 1
            st.rerun()
        except Exception as e:
            st.error(f"Invalid tactic file: {e}")

    if st.button("Export PNG", use_container_width=True):
        _post_message("exportPng")

    st.divider()

    # Player name editing
    with st.expander("Edit Home Players"):
        state = st.session_state.board_state
        for p in state.home_players:
            new_name = st.text_input(
                f"#{p.number}",
                value=p.name,
                key=f"home_name_{p.id}",
            )
            if new_name != p.name:
                p.name = new_name

    with st.expander("Edit Away Players"):
        state = st.session_state.board_state
        for p in state.away_players:
            new_name = st.text_input(
                f"#{p.number}",
                value=p.name,
                key=f"away_name_{p.id}",
            )
            if new_name != p.name:
                p.name = new_name


# ----- Main Area -----
state: BoardState = st.session_state.board_state

all_players = [p.model_dump() for p in state.home_players] + [
    p.model_dump() for p in state.away_players
]

tactics_board(
    players=all_players,
    ball=state.ball.model_dump(),
    arrows=[a.model_dump() for a in state.arrows],
    mode=st.session_state.mode,
    home_color=home_color,
    away_color=away_color,
    state_version=st.session_state.get("state_version", 0),
)

st.caption(
    "Drag players and the ball to reposition. "
    "Switch to arrow mode to draw tactical arrows. "
    "Ctrl+Z / Ctrl+Shift+Z for undo/redo."
)
