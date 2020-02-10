import asyncio
import random

from common.models import Ball
from common.network import Connection


async def main(host, port):
    ball = Ball(
        random.randint(0, 100),
        random.randint(0, 100),
    )

    with await Connection.create(host, port) as connection:
        for _ in range(100):
            await connection.send_obj(ball)
            print(await connection.recv_obj())


if __name__ == '__main__':
    asyncio.run(main('127.0.0.1', 5000))
