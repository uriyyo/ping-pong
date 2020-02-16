import logging
from typing import Optional

from .ui.models import Game
from .ui.window import Window


def game_loop(game: Game, verbosity: Optional[str] = None) -> None:
    if verbosity is not None:
        logging.basicConfig(
            level=getattr(logging, verbosity.upper()),
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.FileHandler("ping_pong.log"), logging.StreamHandler()],
        )

    with Window() as w:
        game.init_keyboard(w.keyboard)

        for _ in w:
            game.update()
            game.render(w.screen)


__all__ = ["game_loop"]
