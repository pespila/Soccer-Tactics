"""Formation presets for the tactics board.

Each formation is a list of 11 (x, y) tuples in field coordinates (105 x 68).
Positions are defined for the home team occupying the BOTTOM half (x < 52.5).
Order: GK, defenders L→R, midfielders L→R, forwards L→R.

Away positions are mirrored by reflecting through the field center.
"""

from __future__ import annotations

from soccer_tactics.constants import FIELD_LENGTH, FIELD_WIDTH

# Home team formations (bottom half: GK near x=0)
FORMATIONS: dict[str, list[tuple[float, float]]] = {
    "4-4-2": [
        (4.0, 34.0),     # GK
        (20.0, 8.0),     # LB
        (20.0, 24.0),    # CB
        (20.0, 44.0),    # CB
        (20.0, 60.0),    # RB
        (38.0, 8.0),     # LM
        (38.0, 24.0),    # CM
        (38.0, 44.0),    # CM
        (38.0, 60.0),    # RM
        (48.0, 22.0),    # ST
        (48.0, 46.0),    # ST
    ],
    "4-3-3": [
        (4.0, 34.0),
        (20.0, 8.0),
        (20.0, 24.0),
        (20.0, 44.0),
        (20.0, 60.0),
        (36.0, 14.0),
        (36.0, 34.0),
        (36.0, 54.0),
        (48.0, 10.0),
        (48.0, 34.0),
        (48.0, 58.0),
    ],
    "3-5-2": [
        (4.0, 34.0),
        (20.0, 14.0),
        (20.0, 34.0),
        (20.0, 54.0),
        (36.0, 4.0),
        (36.0, 20.0),
        (36.0, 34.0),
        (36.0, 48.0),
        (36.0, 64.0),
        (48.0, 22.0),
        (48.0, 46.0),
    ],
    "4-2-3-1": [
        (4.0, 34.0),
        (20.0, 8.0),
        (20.0, 24.0),
        (20.0, 44.0),
        (20.0, 60.0),
        (32.0, 22.0),
        (32.0, 46.0),
        (42.0, 10.0),
        (42.0, 34.0),
        (42.0, 58.0),
        (50.0, 34.0),
    ],
    "4-1-4-1": [
        (4.0, 34.0),
        (20.0, 8.0),
        (20.0, 24.0),
        (20.0, 44.0),
        (20.0, 60.0),
        (30.0, 34.0),
        (40.0, 8.0),
        (40.0, 24.0),
        (40.0, 44.0),
        (40.0, 60.0),
        (50.0, 34.0),
    ],
    "3-4-3": [
        (4.0, 34.0),
        (20.0, 14.0),
        (20.0, 34.0),
        (20.0, 54.0),
        (36.0, 6.0),
        (36.0, 26.0),
        (36.0, 42.0),
        (36.0, 62.0),
        (48.0, 10.0),
        (48.0, 34.0),
        (48.0, 58.0),
    ],
    "5-3-2": [
        (4.0, 34.0),
        (20.0, 4.0),
        (20.0, 18.0),
        (20.0, 34.0),
        (20.0, 50.0),
        (20.0, 64.0),
        (36.0, 14.0),
        (36.0, 34.0),
        (36.0, 54.0),
        (48.0, 22.0),
        (48.0, 46.0),
    ],
    "5-4-1": [
        (4.0, 34.0),
        (20.0, 4.0),
        (20.0, 18.0),
        (20.0, 34.0),
        (20.0, 50.0),
        (20.0, 64.0),
        (38.0, 8.0),
        (38.0, 24.0),
        (38.0, 44.0),
        (38.0, 60.0),
        (50.0, 34.0),
    ],
    "4-5-1": [
        (4.0, 34.0),
        (20.0, 8.0),
        (20.0, 24.0),
        (20.0, 44.0),
        (20.0, 60.0),
        (36.0, 4.0),
        (36.0, 20.0),
        (36.0, 34.0),
        (36.0, 48.0),
        (36.0, 64.0),
        (50.0, 34.0),
    ],
}

FORMATION_NAMES = list(FORMATIONS.keys())


def get_formation(name: str) -> list[tuple[float, float]]:
    """Return the list of (x, y) positions for a formation."""
    return FORMATIONS[name]


def mirror_positions(
    positions: list[tuple[float, float]],
) -> list[tuple[float, float]]:
    """Mirror positions through the field center for the away team."""
    return [
        (FIELD_LENGTH - x, FIELD_WIDTH - y) for x, y in positions
    ]
