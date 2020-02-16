from ping_pong.game_loop import game_loop
from ping_pong.ui.models import Game


def main():
    game_loop(Game())


if __name__ == "__main__":
    main()
