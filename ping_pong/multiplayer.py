from typing import Optional

import click

from ping_pong.game_loop import game_loop
from ping_pong.network import ConnectionType, RemoteGame, connect


def remote_game_loop(
    host: "str",
    port: "int",
    connection_type: "ConnectionType",
    verbosity: "Optional[str]",
) -> None:
    game = RemoteGame(connection_type=connection_type)
    connect(game, connection_type, host, port, game.events_queue)

    game_loop(game, verbosity)


@click.command()
@click.option("--host", type=str, default="127.0.0.1")
@click.option("--port", type=int, default=8000)
@click.option("--server", is_flag=True)
@click.option("-v", "--verbosity", type=str, default=None)
def main(host: "str", port: "int", server: "bool", verbosity: "Optional[str]") -> None:
    remote_game_loop(
        host,
        port,
        ConnectionType.SERVER if server else ConnectionType.CLIENT,
        verbosity,
    )


if __name__ == "__main__":
    main()
