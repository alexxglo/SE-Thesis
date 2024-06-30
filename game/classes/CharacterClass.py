import settings


class CharacterClass:
    def __init__(self, name, class_name, spells, proficiencies, inventory, main_weapon):
        self.name = name
        self.characterClass = class_name
        self.spells = spells
        self.proficiencies = ', '.join(value['name'] for value in proficiencies.values())
        self.level = 1
        self.xp = 0
        self.xpToNextLevel = 3000
        self.inventory = ', '.join([item.name for item in inventory])
        self.mainWeapon = main_weapon
        self.roomCode = settings.ROOM_CODE

    def __str__(self):
        return f"Name: {self.name}\nClass: {self.characterClass}\nSpells: {self.spells}\nProficiencies: {self.proficiencies}\nLevel: {self.level}\nXP: {self.xp}/{self.xpToNextLevel}\nInventory: {self.inventory}\nMain weapon: {self.mainWeapon}"
