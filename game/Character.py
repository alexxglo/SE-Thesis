import arcade

import character_creation

HEALTHBAR_WIDTH = 100
HEALTHBAR_HEIGHT = 3
HEALTHBAR_OFFSET_X = 150
HEALTHBAR_OFFSET_Y = 0
HEALTH_NUMBER_OFFSET_X = 100
HEALTH_NUMBER_OFFSET_Y = -30


class Character(arcade.Sprite):
    def __init__(self, name, class_name, image, scale):
        super().__init__(image, scale)
        # Add extra attributes for health
        self.max_health = 100
        self.cur_health = 100
        self.character = character_creation.create(class_name, name)

    def draw_health_number(self):
        """ Draw how many hit points we have """

        health_string = f"{self.cur_health}/{self.max_health}"
        arcade.draw_text(health_string,
                         start_x=self.center_x + HEALTH_NUMBER_OFFSET_X,
                         start_y=self.center_y + HEALTH_NUMBER_OFFSET_Y,
                         font_size=12,
                         color=arcade.color.WHITE)

    def draw_health_bar(self):
        """ Draw the health bar """
        # Draw the 'unhealthy' background
        if self.cur_health < self.max_health:
            arcade.draw_rectangle_filled(center_x=self.center_x + HEALTHBAR_OFFSET_X,
                                         center_y=self.center_y + HEALTHBAR_OFFSET_Y,
                                         width=HEALTHBAR_WIDTH,
                                         height=3,
                                         color=arcade.color.RED)
            # Calculate width based on health
        health_width = HEALTHBAR_WIDTH * (self.cur_health / self.max_health)
        arcade.draw_rectangle_filled(center_x=(self.center_x + HEALTHBAR_OFFSET_X) - 0.5 * (HEALTHBAR_WIDTH - health_width),
                                     center_y=(self.center_y + HEALTHBAR_OFFSET_Y),
                                     width=health_width,
                                     height=HEALTHBAR_HEIGHT,
                                     color=arcade.color.GREEN)
