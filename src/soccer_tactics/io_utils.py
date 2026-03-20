"""I/O utilities for tactic file validation."""

from __future__ import annotations

from soccer_tactics.models import BoardState


def parse_tactic(data: bytes) -> BoardState:
    """Parse and validate a tactic JSON file."""
    return BoardState.model_validate_json(data)
