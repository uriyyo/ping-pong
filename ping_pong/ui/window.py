from dataclasses import dataclass, field
from types import TracebackType
from typing import TYPE_CHECKING, Any, Iterator, Optional, Type

import pygame

from .consts import SIZE
from .keyboard import Keyboard

if TYPE_CHECKING:
    from .types import Size


@dataclass
class Window:
    fps: "int" = 30
    title: "str" = "Ping Pong"
    size: "Size" = SIZE

    screen: "Optional[Any]" = field(default=None, init=False)
    keyboard: "Keyboard" = field(default_factory=Keyboard, init=False)

    def start(self) -> None:
        pygame.init()
        pygame.mixer.quit()

        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("Ping Pong")

    def __enter__(self) -> "Window":
        self.start()

        return self

    def __exit__(
        self, exc_type: "Type[Exception]", exc_val: "Exception", exc_tb: "TracebackType"
    ) -> None:
        pygame.quit()

    def __iter__(self) -> "Iterator[Any]":
        clock = pygame.time.Clock()

        while True:
            event = pygame.event.poll()

            if event.type == pygame.QUIT:
                break

            self.keyboard.loop()

            yield event

            clock.tick(self.fps)


__all__ = ["Window"]
