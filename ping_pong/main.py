import asyncio
import time

import click
import pygame

from ping_pong.consts import *
from ping_pong.models import (
    ClientType,
    Game,
)
from ping_pong.network import create_connection


async def game(host, port, client_type: ClientType):
    pygame.init()

    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Ping Pong")

    game = Game(client_type)

    updates_queue = await create_connection(game, client_type, host, port)

    try:
        current_time = 0

        while True:
            event = pygame.event.poll()
            if event != pygame.NOEVENT:
                if event == pygame.QUIT:
                    break

                await game.on_key(updates_queue)

            await game.update(updates_queue)
            game.render(screen)

            last_time, current_time = current_time, time.time()
            await asyncio.sleep(1 / FPS - (current_time - last_time))

    finally:
        pygame.quit()


@click.command()
@click.option('--host', type=str, default="127.0.0.1")
@click.option('--port', type=int, default=8000)
@click.option('--server', is_flag=True)
def main(host, port, server):
    asyncio.run(game(
        host,
        port,
        ClientType.SERVER if server else ClientType.CLIENT,
    ))


if __name__ == '__main__':
    main()
