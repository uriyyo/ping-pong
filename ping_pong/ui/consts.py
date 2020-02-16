from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .types import Size, Color

WIDTH: int = 1000
HEIGHT: int = 650

SIZE: Size = (WIDTH, HEIGHT)

BLACK: Color = (0, 0, 0)
WHITE: Color = (255, 255, 255)

PADDLE_SPEED: int = 20

PADDLE_WIDTH: int = 20
PADDLE_HEIGHT: int = 300

BALL_SIZE: int = 20

__all__ = [
    "WIDTH",
    "HEIGHT",
    "SIZE",
    "BLACK",
    "WHITE",
    "PADDLE_WIDTH",
    "PADDLE_SPEED",
    "PADDLE_HEIGHT",
    "BALL_SIZE",
]
