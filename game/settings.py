import random
import string

import socketio

sio = socketio.SimpleClient()

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = .25
COIN_COUNT = 50

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Project Dreambuilder"
NAME_LIST = []
PLAYER_LIST_Y = [1.8, 2, 2.2, 2.4]

OPENAI_API_KEY = ""
ENDPOINT_RESPONSE = ""
ROOM_CODE = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
IMAGE_GENERATED = False


# --- init socket connection ---
def init_websocket():
    sio.connect(url='ws://{IP4-Address}:8085')  # connect to server
    sio.emit(event="init_game", data={
        "roomCode": ROOM_CODE
    })  # send server the roomCode
    print(ROOM_CODE)


def emit_player_info(player_data):
    sio.emit(event="emit_ch_info", data=player_data)


def empty_room():
    sio.emit(event="empty_room", data=ROOM_CODE)


def emit_next_attack(player):
    sio.emit(event="emit_next_action", data=player)
