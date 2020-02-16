import logging

from ping_pong.ui.window import Window

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)


async def game_loop(game):
    with Window() as w:
        game.init_keyboard(w.keyboard)

        async for _ in w:
            await game.update()
            game.render(w.screen)


__all__ = ["game_loop"]
