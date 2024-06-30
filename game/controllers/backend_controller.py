import requests

url = "http://192.168.1.155:8082/"
headers = {"Content-Type": "*/*"}


def post_room_info(data):
    return requests.post(url + "players?roomCode=" + data, headers=headers)

def get_room_info(data):
    return requests.get(url + "players?roomCode=" + data, headers=headers)