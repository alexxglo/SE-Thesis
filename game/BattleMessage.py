import arcade


class BattleMessage(arcade.Sprite):
    def __init__(self, message, pos_x, pos_y):
        super().__init__()
        self.message = message
        self.pos_x = pos_x
        self.pos_y = pos_y

    def draw_message(self):
        """ Draw how many hit points we have """

        message_string = f"{self.message}"
        arcade.draw_text(message_string,
                         start_x=self.center_x + self.pos_x,
                         start_y=self.center_y + self.pos_y,
                         font_size=20,
                         color=arcade.color.WHITE)
