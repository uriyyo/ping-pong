from typing import Optional

import click

from ping_pong.game_loop import game_loop
from ping_pong.ui.models import Game


@click.command()
@click.option("-v", "--verbosity", type=str, default=None)
def main(verbosity: "Optional[str]") -> None:
    game_loop(Game(), verbosity)


if __name__ == "__main__":
    main()
