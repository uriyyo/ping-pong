import logging

from sync_ping_pong.ui.window import Window

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)


def game_loop(game):
    with Window() as w:
        game.init_keyboard(w.keyboard)

        for _ in w:
            game.update()
            game.render(w.screen)


__all__ = ["game_loop"]
