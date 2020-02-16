from dataclasses import dataclass, field
from typing import Callable, List

import pygame


@dataclass
class Keyboard:
    delay: float = 0
    subscribers: List[Callable] = field(default_factory=list)

    def subscribe(self, subscriber: Callable):
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber: Callable):
        self.subscribers.remove(subscriber)

    async def loop(self):
        keys = pygame.key.get_pressed()

        if any(keys):
            for h in self.subscribers:
                await h(keys)


__all__ = ["Keyboard"]
