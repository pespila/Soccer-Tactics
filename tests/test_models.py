"""Tests for data models."""

from soccer_tactics.models import Arrow, BoardState, Player


def test_player_creation():
    p = Player(id=0, number=1, x=10.0, y=20.0, team="home")
    assert p.id == 0
    assert p.number == 1
    assert p.x == 10.0
    assert p.y == 20.0
    assert p.team == "home"
    assert p.name == ""


def test_player_with_name():
    p = Player(id=1, number=9, name="Striker", x=50.0, y=34.0, team="away")
    assert p.name == "Striker"


def test_arrow_defaults():
    a = Arrow(start_x=0, start_y=0, end_x=10, end_y=10)
    assert a.color == "#ffeb3b"


def test_board_state_serialization():
    state = BoardState(
        home_players=[
            Player(id=i, number=i + 1, x=float(i), y=float(i), team="home")
            for i in range(11)
        ],
        away_players=[
            Player(id=i, number=i + 1, x=float(i), y=float(i), team="away")
            for i in range(11)
        ],
        ball=Player(id=0, number=0, x=52.5, y=34.0, team="ball"),
        arrows=[Arrow(start_x=0, start_y=0, end_x=10, end_y=10)],
    )
    json_str = state.model_dump_json()
    restored = BoardState.model_validate_json(json_str)
    assert len(restored.home_players) == 11
    assert len(restored.away_players) == 11
    assert restored.ball.x == 52.5
    assert len(restored.arrows) == 1
