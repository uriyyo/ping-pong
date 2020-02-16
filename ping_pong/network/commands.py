from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, List

import pygame

if TYPE_CHECKING:
    from ping_pong.ui.models import Game


class Command(ABC):
    @abstractmethod
    def __call__(self, game: "Game") -> None:
        ...


@dataclass
class CompoundCommand(Command):
    commands: List["Command"]

    def __call__(self, game: "Game") -> None:
        for c in self.commands:
            c(game)


@dataclass
class SetScoresCommand(Command):
    scores: Dict[str, int]

    def __call__(self, game: "Game") -> None:
        game.scores = self.scores


@dataclass
class SetRectCommand(Command):
    entity: str
    rect: pygame.Rect

    def __call__(self, game: "Game") -> None:
        getattr(game, self.entity).rect = self.rect
