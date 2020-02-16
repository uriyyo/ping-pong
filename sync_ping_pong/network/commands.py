from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from sync_ping_pong.ui.models import Game


class Command(ABC):
    @abstractmethod
    def __call__(self, game: "Game"):
        ...


@dataclass
class CompoundCommand(Command):
    commands: List["Command"]

    def __call__(self, game: "Game"):
        for c in self.commands:
            c(game)


@dataclass
class SetScoresCommand(Command):
    scores: Dict[str, Any]

    def __call__(self, game: "Game"):
        game.scores = self.scores


@dataclass
class SetRectCommand(Command):
    entity: str
    rect: Any

    def __call__(self, game: "Game"):
        getattr(game, self.entity).rect = self.rect


@dataclass
class SetBallVelocity(Command):
    velocity: Any

    def __call__(self, game: "Game"):
        game.ball.velocity = self.velocity
