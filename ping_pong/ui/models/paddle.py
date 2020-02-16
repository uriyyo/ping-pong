import pygame

from ..consts import (
    BLACK,
    HEIGHT,
    PADDLE_HEIGHT,
    PADDLE_SPEED,
    PADDLE_WIDTH,
    WHITE,
    WIDTH,
)
from ..keyboard import Keys
from ..types import Color
from .direction import Direction


class Paddle(pygame.sprite.Sprite):
    def __init__(
        self,
        move_up_key: int = pygame.K_UNKNOWN,
        move_down_key: int = pygame.K_UNKNOWN,
        speed: int = PADDLE_SPEED,
        color: Color = WHITE,
        width: int = PADDLE_WIDTH,
        height: int = PADDLE_HEIGHT,
    ) -> None:
        super().__init__()

        self.move_up_key = move_up_key
        self.move_down_key = move_down_key
        self.height = height
        self.width = width
        self.speed = speed

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        pygame.draw.rect(self.image, color, [0, 0, width, height])

    def on_key(self, keys: Keys) -> None:
        if keys[self.move_up_key]:
            self.move(Direction.UP)

        if keys[self.move_down_key]:
            self.move(Direction.DOWN)

    def set(self, direction: Direction) -> None:
        if direction in (Direction.UP, Direction.DOWN):
            raise ValueError("Can set only left or right position")

        if direction == Direction.LEFT:
            self.rect.x = self.width
            self.rect.y = HEIGHT // 2 - self.height // 2

        elif direction == Direction.RIGHT:
            self.rect.x = WIDTH - self.width * 2
            self.rect.y = HEIGHT // 2 - self.height // 2

    def move(self, direction: Direction) -> None:
        if direction in (Direction.LEFT, Direction.RIGHT):
            raise ValueError("Can move only up or down")

        if direction == Direction.UP:
            self.rect.y = max(self.rect.y - self.speed, 0)
        elif direction == Direction.DOWN:
            self.rect.y = min(self.rect.y + self.speed, HEIGHT - self.height)


__all__ = ["Paddle"]
