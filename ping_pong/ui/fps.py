from dataclasses import dataclass

import pygame


@dataclass
class FPS:
    fps: float = 30
    clock: pygame.time.Clock = pygame.time.Clock()

    def loop(self):
        self.clock.tick(self.fps)


__all__ = ["FPS"]
