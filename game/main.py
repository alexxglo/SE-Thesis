import arcade
from views.intro import IntroView
import settings

# --- Constants ---
SCREEN_WIDTH = settings.SCREEN_WIDTH
SCREEN_HEIGHT = settings.SCREEN_HEIGHT
SCREEN_TITLE = settings.SCREEN_TITLE


def main():
    """ Main function """
    settings.init_websocket()
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = IntroView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
