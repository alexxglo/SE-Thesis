import json


class CharacterPayloadResponse:
    def __init__(self, data):
        self.character_sheets = []
        for player in data:
            self.character_sheets.append(player.character)

    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)
