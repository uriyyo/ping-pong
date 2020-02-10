from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    NONE = "none"
    UP = "up"
    DOWN = "down"
    RIGHT = "right"
    LEFT = "left"


@dataclass
class Window:
    width: int = 480
    height: int = 640


@dataclass
class Point:
    window: Window
    x: int
    y: int


@dataclass
class Ball(Point):
    speed: int = 1
    size: int = 10
    direction: Direction = Direction.NONE


@dataclass
class Board(Point):
    speed: int = 1
    width: int = 100
    height: int = 10
    direction: Direction = Direction.NONE


@dataclass
class Player:
    board: Board
    window: Window


@dataclass
class Game:
    p1: Player
    p2: Player
    window: Window
    ball: Ball
