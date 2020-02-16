from typing import TYPE_CHECKING, Optional

import pygame

from ..consts import BALL_SIZE, BLACK, HEIGHT, WHITE, WIDTH
from .direction import Direction
from .velocity import Velocity

if TYPE_CHECKING:
    from ..types import Color


class Ball(pygame.sprite.Sprite):
    def __init__(self, color: "Color" = WHITE, size: "int" = BALL_SIZE) -> None:
        super().__init__()

        self.size = size
        self.velocity = Velocity()

        self.image = pygame.Surface([size, size])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        pygame.draw.circle(self.image, color, [size // 2] * 2, size // 2)

    def update(self) -> None:
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

    def move_to_center(self) -> None:
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT // 2

    def reset_velocity(self) -> None:
        self.velocity.reset()

    def bounce(self) -> None:
        self.velocity.speedup()
        self.velocity.horizontal_inverse()

    def collision_with_borders(self) -> "Optional[Direction]":
        direction = Direction.collision(self.rect, self.size)

        if direction:
            self.velocity.move_opposite_direction(direction)

        return direction

    def collision_with_sprite(self, *sprites: "pygame.sprite.Sprite") -> "bool":
        return any(pygame.sprite.collide_mask(self, s) for s in sprites)


__all__ = ["Ball"]
