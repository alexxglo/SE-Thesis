class Attack:
    def __init__(self, name, damage, desc):
        self.name = name
        self.damage = damage
        self.desc = desc

    def __str__(self):
        return f"Name: {self.name}\nDamage: {self.damage}\nDescription: {self.desc}"