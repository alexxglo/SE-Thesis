import arcade

import settings
from views import lobby


class EndView(arcade.View):
    def __init__(self, did_cpu_win):
        super().__init__()
        if did_cpu_win:
            self.background = arcade.load_texture('resources/game_over.jpg')
        else:
            self.background = arcade.load_texture('resources/win_view.png')

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            1920, 1080,
                                            self.background)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        # TODO emit socket event to empty old room
        settings.empty_room()
        settings.NAME_LIST = []  # reset player names list
        game_view = lobby.LobbyView()
        self.window.show_view(game_view)
