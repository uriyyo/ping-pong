from asyncio import run

from async_ping_pong.game_loop import game_loop
from async_ping_pong.ui.models import Game


def main():
    run(game_loop(Game()))


if __name__ == "__main__":
    main()
