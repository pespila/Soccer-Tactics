"""Tests for formation presets."""

from soccer_tactics.constants import FIELD_LENGTH, FIELD_WIDTH
from soccer_tactics.formations import (
    FORMATION_NAMES,
    FORMATIONS,
    get_formation,
    mirror_positions,
)


def test_all_formations_have_11_positions():
    for name, positions in FORMATIONS.items():
        assert len(positions) == 11, f"{name} has {len(positions)} positions"


def test_formation_names_match_keys():
    assert FORMATION_NAMES == list(FORMATIONS.keys())


def test_get_formation():
    positions = get_formation("4-4-2")
    assert len(positions) == 11


def test_all_positions_within_field():
    for name, positions in FORMATIONS.items():
        for x, y in positions:
            assert 0 <= x <= FIELD_LENGTH, f"{name}: x={x} out of bounds"
            assert 0 <= y <= FIELD_WIDTH, f"{name}: y={y} out of bounds"


def test_mirror_positions():
    original = [(10.0, 20.0), (30.0, 40.0)]
    mirrored = mirror_positions(original)
    assert mirrored[0] == (FIELD_LENGTH - 10.0, FIELD_WIDTH - 20.0)
    assert mirrored[1] == (FIELD_LENGTH - 30.0, FIELD_WIDTH - 40.0)


def test_nine_formations_exist():
    expected = ["4-4-2", "4-3-3", "3-5-2", "4-2-3-1", "4-1-4-1", "3-4-3", "5-3-2", "5-4-1", "4-5-1"]
    for name in expected:
        assert name in FORMATIONS, f"Missing formation: {name}"
