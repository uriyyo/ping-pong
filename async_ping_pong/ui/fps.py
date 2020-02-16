import time
from asyncio import sleep
from dataclasses import dataclass, field


@dataclass
class FPS:
    fps: float = 1 / 30
    current_time: float = field(init=False, default=0)

    async def loop(self):
        last_time, self.current_time = self.current_time, time.time()
        await sleep(self.fps - (self.current_time - last_time))


__all__ = ["FPS"]
