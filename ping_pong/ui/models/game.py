from dataclasses import dataclass, field
from typing import Dict, Optional

import pygame

from .ball import Ball
from .direction import Direction
from .paddle import Paddle
from ..consts import BALL_SIZE, BLACK, HEIGHT, WHITE, WIDTH
from ..keyboard import Keyboard


@dataclass
class Game:
    ball: Ball = field(default_factory=Ball)
    paddle_a: Paddle = field(default_factory=Paddle)
    paddle_b: Paddle = field(default_factory=Paddle)

    scores: Dict[str, str] = field(default_factory=lambda: {"a": 0, "b": 0})

    sprites: Optional[pygame.sprite.Group] = field(default=None, init=False)

    def __post_init__(self):
        self.paddle_a.set(Direction.LEFT)
        self.paddle_b.set(Direction.RIGHT)

        self.paddle_a.move_up_key = self.paddle_a.move_up_key or pygame.K_w
        self.paddle_a.move_down_key = self.paddle_a.move_down_key or pygame.K_s

        self.paddle_b.move_up_key = self.paddle_b.move_up_key or pygame.K_UP
        self.paddle_b.move_down_key = self.paddle_b.move_down_key or pygame.K_DOWN

        self.ball.move_to_center()
        self.sprites = pygame.sprite.Group(self.paddle_a, self.paddle_b, self.ball)

    def init_keyboard(self, keyboard: Keyboard):
        keyboard.subscribe(self.paddle_a.on_key)
        keyboard.subscribe(self.paddle_b.on_key)

    def update(self):
        self.sprites.update()
        scores = {**self.scores}

        direction = self.ball.collision_with_borders()

        if direction == Direction.LEFT:
            self.scores["a"] += 1

        if direction == Direction.RIGHT:
            self.scores["b"] += 1

        if self.ball.collision_with_sprite(self.paddle_a, self.paddle_b):
            self.ball.bounce()

        if scores != self.scores:
            self.ball.reset_velocity()
            self.ball.move_to_center()

            self.on_score_changed()

    def render(self, screen):
        screen.fill(BLACK)
        pygame.draw.line(screen, WHITE, [WIDTH // 2, 0], [WIDTH // 2, HEIGHT], 5)

        self.sprites.draw(screen)

        font = pygame.font.Font(None, 74)

        text = font.render(str(self.scores["a"]), 1, WHITE)
        screen.blit(text, (WIDTH // 2 - BALL_SIZE * 2, 10))

        text = font.render(str(self.scores["b"]), 1, WHITE)
        screen.blit(text, (WIDTH // 2 + BALL_SIZE, 10))

        pygame.display.flip()

    def on_score_changed(self):
        pass


__all__ = ["Game"]
