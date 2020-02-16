from dataclasses import dataclass, field
from typing import Callable, List, Sequence

import pygame

Keys = Sequence[int]
KeyboardCallback = Callable[[Keys], None]


@dataclass
class Keyboard:
    subscribers: List[KeyboardCallback] = field(default_factory=list)

    def subscribe(self, subscriber: KeyboardCallback) -> None:
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber: KeyboardCallback) -> None:
        self.subscribers.remove(subscriber)

    def loop(self) -> None:
        keys: Keys = pygame.key.get_pressed()

        for h in self.subscribers:
            h(keys)


__all__ = ["Keys", "Keyboard", "KeyboardCallback"]
