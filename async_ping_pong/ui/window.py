from dataclasses import dataclass, field
from typing import Any, Optional, Tuple

import pygame

from .consts import SIZE
from .fps import FPS
from .keyboard import Keyboard


@dataclass
class Window:
    fps: FPS = FPS()
    title: str = "Ping Pong"
    size: Tuple[int, int] = SIZE
    screen: Optional[Any] = field(default=None, init=False)
    keyboard: Keyboard = field(default_factory=Keyboard, init=False)

    def __post_init__(self):
        self.keyboard.delay = self.fps.fps / 2

    def start(self):
        pygame.init()

        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("Ping Pong")

    def __enter__(self):
        self.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pygame.quit()

    async def __aiter__(self):
        while True:
            event = pygame.event.poll()

            if event.type == pygame.QUIT:
                break

            await self.keyboard.loop()

            yield event

            await self.fps.loop()


__all__ = ["Window"]
