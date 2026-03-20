"""Tests for state management (unit tests without Streamlit runtime)."""

from soccer_tactics.models import Arrow, BoardState, Player


def _make_state() -> BoardState:
    return BoardState(
        home_players=[
            Player(id=i, number=i + 1, x=float(i * 5), y=float(i * 5), team="home")
            for i in range(11)
        ],
        away_players=[
            Player(id=i, number=i + 1, x=float(100 - i * 5), y=float(60 - i * 5), team="away")
            for i in range(11)
        ],
        ball=Player(id=0, number=0, x=52.5, y=34.0, team="ball"),
        arrows=[],
    )


def test_board_state_round_trip():
    state = _make_state()
    json_str = state.model_dump_json()
    restored = BoardState.model_validate_json(json_str)
    assert restored.home_players[0].x == state.home_players[0].x
    assert restored.ball.x == 52.5


def test_board_state_with_arrows():
    state = _make_state()
    state.arrows = [
        Arrow(start_x=10, start_y=20, end_x=50, end_y=40),
        Arrow(start_x=30, start_y=30, end_x=80, end_y=50, color="#ff0000"),
    ]
    json_str = state.model_dump_json()
    restored = BoardState.model_validate_json(json_str)
    assert len(restored.arrows) == 2
    assert restored.arrows[1].color == "#ff0000"


def test_undo_stack_serialization():
    """Test that state can be serialized/deserialized for undo stack."""
    state = _make_state()
    stack = []
    stack.append(state.model_dump_json())
    state.home_players[0].x = 99.0
    stack.append(state.model_dump_json())
    previous = BoardState.model_validate_json(stack[0])
    assert previous.home_players[0].x == 0.0
