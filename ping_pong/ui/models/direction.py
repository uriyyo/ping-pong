from enum import Enum
from typing import Optional

import pygame

from ..consts import HEIGHT, WIDTH


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    RIGHT = "right"
    LEFT = "left"

    @classmethod
    def collision(
        cls, rect: pygame.Rect, size: int, width: int = WIDTH, height: int = HEIGHT
    ) -> Optional["Direction"]:
        if rect.x >= width - size:
            return Direction.RIGHT
        elif rect.x <= 0:
            return Direction.LEFT
        elif rect.y > height - size:
            return Direction.DOWN
        elif rect.y < 0:
            return Direction.UP

        return None


__all__ = ["Direction"]
