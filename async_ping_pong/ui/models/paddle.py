import pygame

from ping_pong.ui.consts import (
    BLACK,
    HEIGHT,
    PADDLE_HEIGHT,
    PADDLE_SPEED,
    PADDLE_WIDTH,
    WHITE,
    WIDTH,
)
from .direction import Direction


class Paddle(pygame.sprite.Sprite):
    def __init__(
            self,
            move_up_key=pygame.K_UNKNOWN,
            move_down_key=pygame.K_UNKNOWN,
            speed=PADDLE_SPEED,
            color=WHITE,
            width=PADDLE_WIDTH,
            height=PADDLE_HEIGHT
    ):
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

    async def on_key(self, keys):
        if keys[self.move_up_key]:
            self.move(Direction.UP)

        if keys[self.move_down_key]:
            self.move(Direction.DOWN)

    def set(self, direction: Direction):
        if direction in (Direction.UP, Direction.DOWN):
            raise ValueError("Can set only left or right position")

        if direction == Direction.LEFT:
            self.rect.x = self.width
            self.rect.y = HEIGHT // 2 - self.height // 2

        elif direction == Direction.RIGHT:
            self.rect.x = WIDTH - self.width * 2
            self.rect.y = HEIGHT // 2 - self.height // 2

    def move(self, direction: Direction):
        if direction in (Direction.LEFT, Direction.RIGHT):
            raise ValueError("Can move only up or down")

        if direction == Direction.UP:
            self.rect.y -= self.speed
        elif direction == Direction.DOWN:
            self.rect.y += self.speed

        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > HEIGHT - PADDLE_HEIGHT:
            self.rect.y = HEIGHT - PADDLE_HEIGHT


__all__ = ["Paddle"]
