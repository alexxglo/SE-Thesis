import arcade
from arcade.experimental import Shadertoy
from pynput.mouse import Button, Controller
from views import instruction
from .helpers import fading

mouse = Controller()


class IntroView(fading.FadingView):
    """ View to show instructions """

    def __init__(self):
        # Call the parent constructor
        super().__init__()

        # Keep track of total run-time
        self.time = 0.0
        file_name = "misc/earth_planet_sky.glsl"

        # Create a shader from it
        self.shadertoy = Shadertoy(size=(1920, 1080),
                                   main_source=open(file_name).read())

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
        arcade.draw_text(""
                         "Project Dreambuilder Intro", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        mouse.press(Button.left)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        arcade.draw_text("Project Dreambuilder Intro", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        self.shadertoy.render(time=self.time)
        self.draw_fading()

    def on_update(self, dt):
        # Keep track of elapsed time
        self.time += dt
        self.update_fade(next_view=instruction.InstructionView)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        if self.fade_out is None and _button == arcade.MOUSE_BUTTON_LEFT:
            self.fade_out = 0
        # game_view = instruction.InstructionView()
        # self.window.show_view(game_view)
