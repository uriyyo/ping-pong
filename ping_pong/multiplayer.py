import click

from ping_pong.game_loop import game_loop
from ping_pong.network import ConnectionType, RemoteGame, connect


def remote_game_loop(host, port, connection_type: ConnectionType):
    game = RemoteGame(connection_type=connection_type)
    game.events_queue = connect(game, connection_type, host, port)

    game_loop(game)


@click.command()
@click.option("--host", type=str, default="127.0.0.1")
@click.option("--port", type=int, default=8000)
@click.option("--server", is_flag=True)
def main(host, port, server):
    remote_game_loop(
        host, port, ConnectionType.SERVER if server else ConnectionType.CLIENT
    )


if __name__ == "__main__":
    main()
