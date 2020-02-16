import asyncio
from dataclasses import (
    field,
)
from enum import Enum
from random import randint
from typing import (
    Optional,
)

import pygame

from ping_pong.commands import *
from ping_pong.consts import *


class ClientType(Enum):
    SERVER = 'server'
    CLIENT = 'client'

    @classmethod
    def from_str(cls, s: str) -> "ClientType":
        for t in ClientType:
            if t.value.lower() == s.lower():
                return t

        raise ValueError(s)


class Ball(pygame.sprite.Sprite):

    def __init__(self, color=WHITE, size=BALL_SIZE):
        super().__init__()

        width = height = size

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.circle(self.image, color, [BALL_SIZE // 2] * 2, BALL_SIZE // 2)

        self.velocity = [randint(4, 8), randint(-8, 8)]
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.velocity = [-self.velocity[0], randint(-8, 8)]


class Paddle(pygame.sprite.Sprite):
    def __init__(self, color=WHITE, width=PADDLE_WIDTH, height=PADDLE_HEIGHT):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()

    def move_up(self, pixels):
        self.rect.y -= pixels

        if self.rect.y < 0:
            self.rect.y = 0

    def move_down(self, pixels):
        self.rect.y += pixels

        if self.rect.y > HEIGHT - PADDLE_HEIGHT:
            self.rect.y = HEIGHT - PADDLE_HEIGHT


@dataclass
class Game:
    type: ClientType
    ball: Ball = field(default_factory=Ball)
    paddle_a: Paddle = field(default_factory=Paddle)
    paddle_b: Paddle = field(default_factory=Paddle)
    scores: Dict[str, str] = field(default_factory=lambda: {"a": 0, "b": 0})
    sprites: Optional[pygame.sprite.Group] = None

    def __post_init__(self):
        self.paddle_a.rect.x = BALL_SIZE * 2
        self.paddle_a.rect.y = HEIGHT // 2 - PADDLE_HEIGHT // 2

        self.paddle_b.rect.x = WIDTH - BALL_SIZE * 2
        self.paddle_b.rect.y = HEIGHT // 2 - PADDLE_HEIGHT // 2

        self.ball.rect.x = WIDTH // 2
        self.ball.rect.y = HEIGHT // 2

        self.sprites = pygame.sprite.Group(self.paddle_a, self.paddle_b, self.ball)

    async def update(self, queue: asyncio.Queue):
        self.sprites.update()

        if self.type == ClientType.CLIENT:
            return

        velocity = [*self.ball.velocity]
        scores = {**self.scores}

        if self.ball.rect.x >= WIDTH - BALL_SIZE:
            self.scores["a"] += 1
            self.ball.velocity[0] = -self.ball.velocity[0]
        if self.ball.rect.x <= 0:
            self.scores["b"] += 1
            self.ball.velocity[0] = -self.ball.velocity[0]
        if self.ball.rect.y > HEIGHT - BALL_SIZE:
            self.ball.velocity[1] = -self.ball.velocity[1]
        if self.ball.rect.y < 0:
            self.ball.velocity[1] = -self.ball.velocity[1]

        if (
                pygame.sprite.collide_mask(self.ball, self.paddle_a)
                or pygame.sprite.collide_mask(self.ball, self.paddle_b)
        ):
            self.ball.bounce()

        if scores != self.scores:
            await queue.put(SetScoresCommand(self.scores))

        if velocity != self.ball.velocity:
            await queue.put(CompoundCommand([
                SetRectCommand("ball", self.ball.rect),
                SetBallVelocity(self.ball.velocity),
            ]))

    async def on_key(self, queue: asyncio.Queue):
        keys = pygame.key.get_pressed()

        if self.type == ClientType.CLIENT:
            if keys[pygame.K_w]:
                self.paddle_a.move_up(PADDLE_SPEED)
                await queue.put(SetRectCommand("paddle_a", self.paddle_a.rect))

            if keys[pygame.K_s]:
                self.paddle_a.move_down(PADDLE_SPEED)
                await queue.put(SetRectCommand("paddle_a", self.paddle_a.rect))

        else:
            if keys[pygame.K_UP]:
                self.paddle_b.move_up(PADDLE_SPEED)
                await queue.put(SetRectCommand("paddle_b", self.paddle_b.rect))

            if keys[pygame.K_DOWN]:
                self.paddle_b.move_down(PADDLE_SPEED)
                await queue.put(SetRectCommand("paddle_b", self.paddle_b.rect))

    def render(self, screen):
        screen.fill(BLACK)
        pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5)

        self.sprites.draw(screen)

        font = pygame.font.Font(None, 74)

        text = font.render(str(self.scores["a"]), 1, WHITE)
        screen.blit(text, (250, 10))

        text = font.render(str(self.scores["b"]), 1, WHITE)
        screen.blit(text, (420, 10))

        pygame.display.flip()
