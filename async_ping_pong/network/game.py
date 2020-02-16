from asyncio import Queue
from dataclasses import dataclass

from async_ping_pong.ui.keyboard import Keyboard
from async_ping_pong.ui.models import Game
from .commands import SetRectCommand, SetScoresCommand
from .connection import ConnectionType


@dataclass
class RemoteGame(Game):
    connection_type: ConnectionType = ConnectionType.CLIENT
    events_queue: Queue = None

    def init_keyboard(self, keyboard: Keyboard):
        super().init_keyboard(keyboard)

        if self.connection_type == ConnectionType.CLIENT:
            keyboard.unsubscribe(self.paddle_a.on_key)
        elif self.connection_type == ConnectionType.SERVER:
            keyboard.unsubscribe(self.paddle_b.on_key)

    async def on_score_changed(self):
        await self.events_queue.put(SetScoresCommand(self.scores))

    async def update(self):
        if self.connection_type == ConnectionType.SERVER:
            await super().update()
            await self.events_queue.put(SetRectCommand("ball", self.ball.rect))


__all__ = ["RemoteGame"]
