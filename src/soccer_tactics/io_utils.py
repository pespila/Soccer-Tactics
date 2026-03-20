"""Save/load JSON and PNG export utilities."""

from __future__ import annotations

import base64

import streamlit as st

from soccer_tactics.models import BoardState


def save_tactic(state: BoardState) -> None:
    """Offer a download button for the current tactic as JSON."""
    json_data = state.model_dump_json(indent=2)
    st.download_button(
        label="Save Tactic",
        data=json_data,
        file_name="tactic.json",
        mime="application/json",
        use_container_width=True,
    )


def load_tactic() -> BoardState | None:
    """Show a file uploader and return loaded BoardState or None."""
    uploaded = st.file_uploader(
        "Load Tactic",
        type=["json"],
        key="tactic_uploader",
    )
    if uploaded is not None:
        try:
            return BoardState.model_validate_json(uploaded.read())
        except Exception as e:
            st.error(f"Invalid tactic file: {e}")
    return None


def export_png_button(png_base64: str | None) -> None:
    """Offer a download button for the PNG export."""
    if png_base64:
        # Strip data URL prefix if present
        if "," in png_base64:
            png_base64 = png_base64.split(",", 1)[1]
        png_bytes = base64.b64decode(png_base64)
        st.download_button(
            label="Export PNG",
            data=png_bytes,
            file_name="tactic.png",
            mime="image/png",
            use_container_width=True,
        )
