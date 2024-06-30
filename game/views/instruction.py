import arcade

from views import lobby


class InstructionView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = None

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.BLACK)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            1920, 1080,
                                            self.background)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = lobby.LobbyView()
        self.window.show_view(game_view)

    def setup(self):
        """ This should set up your game and get it ready to play """
        # Replace 'pass' with the code to set up your game
        self.background = arcade.load_texture('resources/intro.png')
