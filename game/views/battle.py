import arcade

from views.start import StartView
import settings
import start


class BattleView(arcade.View):
    """ Class to manage the game overview """

    def on_update(self, dt):
        self.update_fade(next_view=StartView)

    def on_show_view(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """ Draw the game overview """
        self.clear()
        arcade.draw_text("Players", settings.SCREEN_WIDTH / 2,
                         settings.SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, 50, anchor_x="center")
        arcade.draw_text("Check your device", settings.SCREEN_WIDTH / 2,
                         settings.SCREEN_HEIGHT / 2.5,
                         arcade.color.WHITE, 30, anchor_x="center")

    def setup(self):
        """ This should set up your game and get it ready to play """
        # Replace 'pass' with the code to set up your game
        pass
