from dataclasses import dataclass
from random import randint
from typing import TYPE_CHECKING

from .direction import Direction

if TYPE_CHECKING:
    from ..types import Range


@dataclass
class Velocity:
    x: "int" = 0
    y: "int" = 0

    x_start_range: "Range" = (10, 15)
    y_start_range: "Range" = (-20, 20)

    speed: "int" = 4
    max_speed: "int" = 45

    def __post_init__(self) -> None:
        self.reset()

    def _check_bounds(self) -> None:
        if abs(self.x) > self.max_speed:
            self.x = self.max_speed if self.x > 0 else -self.max_speed

        if abs(self.y) > self.max_speed:
            self.y = self.max_speed if self.y > 0 else -self.max_speed

    def reset(self) -> None:
        self.x = randint(*self.x_start_range)
        self.y = randint(*self.y_start_range)

    def speedup(self) -> None:
        self.x += self.speed if self.x >= 0 else -self.speed
        self.y += self.speed if self.y >= 0 else -self.speed

        self._check_bounds()

    def horizontal_inverse(self) -> None:
        self.x = -self.x
        self.y = randint(*self.y_start_range)

    def vertical_inverse(self) -> None:
        self.x = randint(*self.x_start_range)
        self.y = -self.y

    def move_opposite_direction(self, direction: "Direction") -> None:
        if direction.UP and self.y > 0:
            self.y = -self.y
        elif direction.DOWN and self.y < 0:
            self.y = -self.y
        elif direction.RIGHT and self.x > 0:
            self.x = -self.x
        elif direction.LEFT and self.x < 0:
            self.x = -self.x


__all__ = ["Velocity"]
