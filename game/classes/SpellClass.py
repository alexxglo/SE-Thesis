class SpellClass:

    def __init__(self, name, description, damage):
        self.name = name
        self.description = description
        if damage is not None:
            if damage.get('damage_at_slot_level') is not None:
                self.damage = damage.get('damage_at_slot_level').get('1')
            elif damage.get('damage_at_character_level') is not None:
                self.damage = damage.get('damage_at_character_level').get('1')
        else:
            self.damage = 0

    def __str__(self):
        return f"Name: {self.name}\nDescription: {self.description}\nDamage: {self.damage}"