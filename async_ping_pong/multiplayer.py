from asyncio import run

import click

from async_ping_pong.game_loop import game_loop
from async_ping_pong.network import ConnectionType, RemoteGame, connect


async def remote_game_loop(host, port, connection_type: ConnectionType):
    game = RemoteGame(connection_type=connection_type)
    game.events_queue = await connect(game, connection_type, host, port)

    await game_loop(game)


@click.command()
@click.option("--host", type=str, default="127.0.0.1")
@click.option("--port", type=int, default=8000)
@click.option("--server", is_flag=True)
def main(host, port, server):
    run(
        remote_game_loop(
            host, port, ConnectionType.SERVER if server else ConnectionType.CLIENT
        )
    )


if __name__ == "__main__":
    main()
