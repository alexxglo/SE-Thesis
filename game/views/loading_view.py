import threading
import time

import arcade
from auto1111sdk import StableDiffusionPipeline

import settings
from views.battle_view import BattleView


class LoadingView(arcade.View):
    """ Class to manage the game overview """

    def __init__(self, player_data, boss_data):
        super().__init__()
        self.background = arcade.load_texture('resources/loading_screen.jpg')
        self.boss = None
        self.boss_prompt = boss_data
        self.player_data = player_data
        self.thread_done = 0

    def on_update(self, delta_time: float):
        self.on_draw()
        if settings.IMAGE_GENERATED:
            next_view = BattleView(self.boss_prompt, self.player_data)
            next_view.setup()
            self.window.show_view(next_view)

    def on_show_view(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        pass

    def on_draw(self):
        """ Draw the game overview """
        self.clear()
        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            1920, 1080,
                                            self.background)
