"""Pydantic data models for the tactics board."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class Player(BaseModel):
    """A player or ball on the field."""

    id: int
    number: int
    name: str = ""
    x: float  # 0-105 field coords (length)
    y: float  # 0-68 field coords (width)
    team: Literal["home", "away", "ball"]


class Arrow(BaseModel):
    """A tactical arrow drawn on the field."""

    start_x: float
    start_y: float
    end_x: float
    end_y: float
    color: str = "#ffeb3b"


class BoardState(BaseModel):
    """Complete state of the tactics board."""

    home_players: list[Player]
    away_players: list[Player]
    ball: Player
    arrows: list[Arrow] = []
