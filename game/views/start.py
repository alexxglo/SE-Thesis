import arcade
import settings
import re

from views import loading_view
from .helpers import fading

story_data = None
player_data = None


def set_player_data(data):
    global player_data
    player_data = data


def set_story_data(data):
    global story_data
    story_data = data


def set_boss_data(data):
    global boss_data
    boss_data = data


class StartView(fading.FadingView):

    def on_update(self, dt):
        self.update_fade(next_view=GameView)

    def on_show_view(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """ Draw the menu """
        self.clear()
        input_string = story_data.content
        split_string = re.split(" ", input_string)
        adjusted_height_rate = 100
        word_line = 0
        show_string = []
        for string_pos, string in enumerate(split_string):
            word_line += 1
            show_string.append(string)
            if word_line == 10 or string_pos == len(split_string) - 1:
                adjusted_height_rate = adjusted_height_rate + 100
                arcade.draw_text(" ".join(show_string), settings.SCREEN_WIDTH / 2,
                                 settings.SCREEN_HEIGHT - adjusted_height_rate,
                                 arcade.color.WHITE, font_size=30, anchor_x="center")
                word_line = 0
                show_string = []

        self.draw_fading()

    def on_show(self):
        if self.fade_out is None:
            self.fade_out = 0

    def setup(self):
        """ This should set up your game and get it ready to play """
        # Replace 'pass' with the code to set up your game
        pass


class GameView(fading.FadingView):
    # player characters view

    def __init__(self):
        super().__init__()
        self.player_pic_list = None
        self.relative_width = []
        self.relative_height = []
        self.relative_align = []
        self.relative_direction = []

    def setup(self):  # setup
        self.player_pic_list = arcade.SpriteList()
        if len(player_data) == 1:
            self.relative_width = [960]
            self.relative_height = [540]
            self.relative_align = [-200]
            self.relative_direction = ['right']
        elif len(player_data) == 2:
            self.relative_width = [640, 1280]
            self.relative_height = [540, 540]
            self.relative_align = [-200, 200]
            self.relative_direction = ['right', 'left']
        elif len(player_data) == 3:
            self.relative_width = [640, 1280, 960]
            self.relative_height = [750, 750, 300]
            self.relative_align = [-200, 200, -200]
            self.relative_direction = ['right', 'left', 'right']
        else:
            self.relative_width = [640, 1280, 640, 1280]
            self.relative_height = [750, 750, 300, 300]
            self.relative_align = [-200, 200, -200, 200]
            self.relative_direction = ['right', 'left', 'right', 'left']

        for player_pos, player in enumerate(player_data):
            p = arcade.Sprite("misc/" + player['characterClass'].lower() + ".png", 0.5)
            p.center_x = self.relative_width[player_pos]
            p.center_y = self.relative_height[player_pos]

            self.player_pic_list.append(p)

    def on_show(self):
        if self.fade_out is None:
            self.fade_out = 0

    def on_update(self, dt):
        self.update_fade(next_view=GameOverView)

    def on_show_view(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """ Draw everything for the game. """
        self.clear()
        for player_pos, player in enumerate(player_data):
            arcade.draw_text(player["name"], self.relative_width[player_pos] + self.relative_align[player_pos],
                             self.relative_height[player_pos] + 50,
                             arcade.color.WHITE, font_size=30, anchor_x=self.relative_direction[player_pos])
            arcade.draw_text(player["race"],self.relative_width[player_pos] + self.relative_align[player_pos],
                             self.relative_height[player_pos],
                             arcade.color.WHITE, font_size=30, anchor_x=self.relative_direction[player_pos])
            arcade.draw_text(player["characterClass"], self.relative_width[player_pos] + self.relative_align[player_pos],
                             self.relative_height[player_pos] - 50,
                             arcade.color.WHITE, font_size=30, anchor_x=self.relative_direction[player_pos])

        self.player_pic_list.draw()
        self.draw_fading()


class GameOverView(fading.FadingView):
    """ Class to manage the game overview """

    def on_update(self, dt):
        self.update_fade(next_view=StartView)

    def on_show_view(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """ Draw the game overview """
        self.clear()
        game_view = loading_view.LoadingView(
            player_data, boss_data)
        game_view.setup()
        self.window.show_view(game_view)

    def setup(self):
        """ This should set up your game and get it ready to play """
        # Replace 'pass' with the code to set up your game
        pass


def main():
    """ Startup """
    window = arcade.Window(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, "Different Views Minimal Example")
    menu_view = StartView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
