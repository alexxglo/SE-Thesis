import arcade
import math

from auto1111sdk import StableDiffusionPipeline

import settings
from views import start
from pynput.mouse import Controller
import threading
import story_mechanics

# Set up the constants

# These constants control the particulars about the radar
CENTER_X = settings.SCREEN_WIDTH // 2
CENTER_Y = settings.SCREEN_HEIGHT // 3
RADIANS_PER_FRAME = 0.02
SWEEP_LENGTH = settings.SCREEN_HEIGHT / 30 + settings.SCREEN_WIDTH / 30
mouse = Controller()


class Radar:
    def __init__(self):
        self.angle = 0

    def update(self):
        # Move the angle of the sweep.
        self.angle += RADIANS_PER_FRAME

    def draw(self):
        """ Use this function to draw everything to the screen. """

        # Calculate the end point of our radar sweep. Using math.
        x = SWEEP_LENGTH * math.sin(self.angle) + CENTER_X
        y = SWEEP_LENGTH * math.cos(self.angle) + CENTER_Y

        # Start the render. This must happen before any drawing
        # commands. We do NOT need an stop render command.
        arcade.start_render()

        arcade.draw_text("Waiting for your input", settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 1.7,
                         arcade.color.WHITE, 44, anchor_x="center")
        arcade.draw_text("Please check  your phone", settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 1.9,
                         arcade.color.WHITE, 25, anchor_x="center")
        # Draw the radar line
        arcade.draw_line(CENTER_X, CENTER_Y, x, y, arcade.color.WHITE, 3)

        # Draw the outline of the radar
        arcade.draw_circle_outline(CENTER_X,
                                   CENTER_Y,
                                   SWEEP_LENGTH,
                                   arcade.color.DARK_GREEN,
                                   border_width=10,
                                   num_segments=60)


class LoadingView(arcade.View):
    """ Main application class. """

    def generate_image(self, prompt):
        pipe = StableDiffusionPipeline("resources/arthemy-diffuser.safetensors")

        output = pipe.generate_txt2img(prompt=prompt, height=256, width=256, steps=10)

        output[0].save("resources/boss.png")
        settings.IMAGE_GENERATED = True

    def await_server_response(self):
        flag = 0
        while flag == 0:
            event = settings.sio.receive()
            print(f'received event: "{event[0]}" with arguments {event[1:]}')
            if event[0] == "get_initial_game_data":
                flag = 1
                game_data = event[1:]
                game_view = start.StartView()
                start.set_player_data(event[1]['players'])
                start.set_story_data(story_mechanics.generate_story(game_data))  # send story data to next view
                start.set_boss_data(game_data[0]['finalBoss'])
                boss_name = game_data[0]['finalBoss']
                t1 = threading.Thread(target=self.generate_image, args=(boss_name,))
                t1.start()
                self.window.show_view(game_view)

    def on_show_view(self):
        """ This is run once when we switch to this view """
        self.radar = Radar()
        arcade.set_background_color(arcade.color.BLACK)
        t1 = threading.Thread(
            target=self.await_server_response)  # start thread to check on server response with player list and game details
        t1.start()

    def on_update(self, delta_time):
        # Move the rectangle
        self.radar.update()

    def on_draw(self):
        # Clear screen
        self.clear()
        # Draw the rectangle
        self.radar.draw()
