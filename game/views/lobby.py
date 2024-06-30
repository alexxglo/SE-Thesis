from time import sleep

import arcade
import settings
import controllers.backend_controller
import json

from views import loading_screen
import threading
from pynput.mouse import Controller

mouse = Controller()


def add_players():
    sleep(1)
    return "USER_"


class LobbyView(arcade.View):
    ACTIVE_PLAYERS = 0
    NAME_LIST = []
    CREATE_ROOM = False
    PLAYER_LIST_Y = [540, 620, 700, 780]
    index = 0

    def __init__(self):
        super().__init__()
        self.background = None
        self.word_list = None

    def setup(self):
        pass

    def await_server_response(self):
        flag = 0
        while flag == 0:
            event = settings.sio.receive()
            print(f'received event: "{event[0]}" with arguments {event[1:]}')
            if event[0] == "lock_room":
                flag = 1
                game_view = loading_screen.LoadingView()
                self.window.show_view(game_view)

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.BLACK)
        self.ACTIVE_PLAYERS = 0
        self.NAME_LIST = []
        self.CREATE_ROOM = False
        self.index = 0

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
        t1 = threading.Thread(
            target=self.await_server_response)  # start thread to check on server response with player list and game details
        t1.start()

    def on_draw(self):
        """ Draw this view """
        self.clear()
        arcade.draw_text("Please connect to room code ", self.window.width / 2, self.window.height / 1.2,
                         arcade.color.WHITE, font_size=40, anchor_x="center")
        arcade.draw_text(settings.ROOM_CODE, self.window.width / 2, self.window.height / 1.35,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Lobby list", self.window.width / 2, self.window.height / 1.7,
                         arcade.color.WHITE, font_size=35, anchor_x="center")
        if len(self.NAME_LIST) != 0:
            for index, name in enumerate(self.NAME_LIST):
                arcade.draw_text(name, self.window.width / 2, self.window.height - self.PLAYER_LIST_Y[index],
                                 arcade.color.WHITE, font_size=25, anchor_x="center")
                self.ACTIVE_PLAYERS = self.ACTIVE_PLAYERS + 1

    def on_update(self, delta_time: float):
        if len(self.NAME_LIST) < 4:
            if self.CREATE_ROOM is False:
                response = json.loads(controllers.backend_controller.post_room_info(settings.ROOM_CODE).text)
                self.CREATE_ROOM = True
            else:
                response = json.loads(controllers.backend_controller.get_room_info(settings.ROOM_CODE).text)
            if response['players'] is not None:
                for i in response['players']:
                    if i['name'] not in self.NAME_LIST:
                        self.NAME_LIST.append(i['name'])
