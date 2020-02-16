from dataclasses import dataclass, field
from queue import Queue
from typing import TYPE_CHECKING

from ping_pong.ui.keyboard import Keyboard, KeyboardCallback, Keys
from ping_pong.ui.models import Game

from .commands import SetRectCommand, SetScoresCommand
from .connection import ConnectionType

if TYPE_CHECKING:
    from .commands import CommandQueue


@dataclass
class RemoteGame(Game):
    connection_type: "ConnectionType" = ConnectionType.CLIENT
    events_queue: "CommandQueue" = field(default_factory=Queue)

    def _on_key_callback(self, paddle_name: "str") -> "KeyboardCallback":
        paddle = getattr(self, paddle_name)

        def _callback(keys: "Keys") -> None:
            paddle.on_key(keys)
            self.events_queue.put(SetRectCommand(paddle_name, paddle.rect))

        return _callback

    def init_keyboard(self, keyboard: "Keyboard") -> None:
        super().init_keyboard(keyboard)

        keyboard.unsubscribe(self.paddle_a.on_key)
        keyboard.unsubscribe(self.paddle_b.on_key)

        if self.connection_type == ConnectionType.SERVER:
            keyboard.subscribe(self._on_key_callback("paddle_b"))
        elif self.connection_type == ConnectionType.CLIENT:
            keyboard.subscribe(self._on_key_callback("paddle_a"))

    def on_score_changed(self) -> None:
        self.events_queue.put(SetScoresCommand(self.scores))

    def update(self) -> None:
        if self.connection_type == ConnectionType.SERVER:
            super().update()
            self.events_queue.put(SetRectCommand("ball", self.ball.rect))


__all__ = ["RemoteGame"]
