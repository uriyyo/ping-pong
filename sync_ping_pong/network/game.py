from dataclasses import dataclass
from queue import Queue

from sync_ping_pong.ui.keyboard import Keyboard
from sync_ping_pong.ui.models import Game, Paddle
from .commands import SetRectCommand, SetScoresCommand
from .connection import ConnectionType


def on_key_callback(paddle: Paddle, paddle_name: str, queue: Queue):
    def _callback(keys):
        paddle.on_key(keys)
        queue.put(SetRectCommand(paddle_name, paddle.rect))

    return _callback


@dataclass
class RemoteGame(Game):
    connection_type: ConnectionType = ConnectionType.CLIENT
    events_queue: Queue = None

    def init_keyboard(self, keyboard: Keyboard):
        super().init_keyboard(keyboard)

        keyboard.unsubscribe(self.paddle_a.on_key)
        keyboard.unsubscribe(self.paddle_b.on_key)

        if self.connection_type == ConnectionType.SERVER:
            keyboard.subscribe(on_key_callback(self.paddle_a, "paddle_a", self.events_queue))

        elif self.connection_type == ConnectionType.CLIENT:
            keyboard.subscribe(on_key_callback(self.paddle_b, "paddle_b", self.events_queue))

    def on_score_changed(self):
        self.events_queue.put(SetScoresCommand(self.scores))

    def update(self):
        if self.connection_type == ConnectionType.SERVER:
            super().update()
            self.events_queue.put(SetRectCommand("ball", self.ball.rect))


__all__ = ["RemoteGame"]
