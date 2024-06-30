class WeaponClass:
    def __init__(self, name, damage, weapon_range):
        self.name = name
        self.damage = damage
        self.weaponRange = weapon_range

    def __str__(self):
        return f"{self.name}\nDamage: {self.damage}\nWeapon range: {self.weaponRange}"
