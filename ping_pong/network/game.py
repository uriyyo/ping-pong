from dataclasses import dataclass
from queue import Queue

from ping_pong.ui.keyboard import Keyboard
from ping_pong.ui.models import Game
from .commands import SetRectCommand, SetScoresCommand
from .connection import ConnectionType


@dataclass
class RemoteGame(Game):
    connection_type: ConnectionType = ConnectionType.CLIENT
    events_queue: Queue = None

    def _on_key_callback(self, paddle_name: str):
        paddle = getattr(self, paddle_name)

        def _callback(keys):
            paddle.on_key(keys)
            self.events_queue.put(SetRectCommand(paddle_name, paddle.rect))

        return _callback

    def init_keyboard(self, keyboard: Keyboard):
        super().init_keyboard(keyboard)

        keyboard.unsubscribe(self.paddle_a.on_key)
        keyboard.unsubscribe(self.paddle_b.on_key)

        if self.connection_type == ConnectionType.SERVER:
            keyboard.subscribe(self._on_key_callback("paddle_a"))
        elif self.connection_type == ConnectionType.CLIENT:
            keyboard.subscribe(self._on_key_callback("paddle_b"))

    def on_score_changed(self):
        self.events_queue.put(SetScoresCommand(self.scores))

    def update(self):
        if self.connection_type == ConnectionType.SERVER:
            super().update()
            self.events_queue.put(SetRectCommand("ball", self.ball.rect))


__all__ = ["RemoteGame"]
