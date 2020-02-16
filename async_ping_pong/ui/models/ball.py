from typing import Optional, Tuple

import pygame

from async_ping_pong.ui.consts import BALL_SIZE, BLACK, HEIGHT, WHITE, WIDTH
from .direction import Direction
from .velocity import Velocity

Range = Tuple[int, int]


class Ball(pygame.sprite.Sprite):
    def __init__(self, color=WHITE, size=BALL_SIZE):
        super().__init__()

        self.size = size
        self.velocity = Velocity()

        self.image = pygame.Surface([size, size])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        pygame.draw.circle(self.image, color, [BALL_SIZE // 2] * 2, BALL_SIZE // 2)

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

    def move_to_center(self):
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT // 2

    def reset_velocity(self):
        self.velocity.reset()

    def bounce(self):
        self.velocity.speedup()
        self.velocity.horizontal_inverse()

    def collision_with_borders(self) -> Optional[Direction]:
        direction = Direction.collision(self.rect, self.size)

        if direction:
            self.velocity.move_opposite_direction(direction)

        return direction

    def collision_with_sprite(self, *sprites: pygame.sprite.Sprite):
        return any(pygame.sprite.collide_mask(self, s) for s in sprites)


__all__ = ["Ball"]
