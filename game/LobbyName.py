import arcade


class LobbyName(arcade.Sprite):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def draw_name(self):
        arcade.draw_text(self.name,
                         start_x=self.center_x,
                         start_y=self.center_y,
                         font_size=12,
                         color=arcade.color.WHITE)
