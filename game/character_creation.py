import random

from dnd_character import classes
from dnd_character.equipment import Item
from dnd_character.spellcasting import SPELLS
from classes.CharacterClass import CharacterClass
from classes.SpellClass import SpellClass
from classes.WeaponClass import WeaponClass


def __class_creation__(class_name, name, weapon_name):
    match class_name:
        case "Bard":
            bard = classes.Bard(name=name,
                                level=1,
                                age=random.randint(18, 70)
                                )
            bard.spells_prepared.append(SPELLS["detect-magic"])
            bard.spells_prepared.append(SPELLS["minor-illusion"])
            bard.spells_prepared.append(SPELLS["unseen-servant"])
            bard.spells_prepared.append(SPELLS["vicious-mockery"])
            bard.spells_prepared.append(SPELLS["healing-word"])

            bard.skills_strength['acrobatics'] = True
            bard.skills_dexterity['persuasion'] = True
            bard.skills_dexterity['deception'] = True

            bard.give_item(Item(weapon_name))

            return bard
        case "Paladin":
            paladin = classes.Paladin(name=name,
                                      level=1,
                                      age=random.randint(18, 70))
            paladin.spells_prepared.append(SPELLS["bless"])
            paladin.spells_prepared.append(SPELLS["command"])
            paladin.spells_prepared.append(SPELLS["shield-of-faith"])
            paladin.spells_prepared.append(SPELLS["hunters-mark"])

            paladin.skills_strength['athletics'] = True
            paladin.skills_dexterity['persuasion'] = True

            paladin.give_item(Item(weapon_name))

            return paladin
        case "Cleric":
            cleric = classes.Cleric(name=name,
                                    level=1,
                                    age=random.randint(18, 70))
            cleric.spells_prepared.append(SPELLS["guidance"])
            cleric.spells_prepared.append(SPELLS["light"])
            cleric.spells_prepared.append(SPELLS["inflict-wounds"])
            cleric.spells_prepared.append(SPELLS["burning-hands"])
            cleric.spells_prepared.append(SPELLS["faerie-fire"])

            cleric.give_item(Item(weapon_name))

            return cleric
        case "Fighter":
            fighter = classes.Fighter(name=name,
                                      level=1,
                                      age=random.randint(18, 70))
            fighter.skills_strength['athletics'] = True
            fighter.skills_dexterity['stealth'] = True

            fighter.give_item(Item(weapon_name))

            return fighter
        case "Barbarian":
            barbarian = classes.Barbarian(name=name,
                                          level=1,
                                          age=random.randint(18, 70))
            barbarian.skills_strength['athletics'] = True
            barbarian.skills_wisdom['perception'] = True

            barbarian.give_item(Item(weapon_name))

            return barbarian
        case "Monk":
            monk = classes.Monk(name=name,
                                level=1,
                                age=random.randint(18, 70))
            monk.skills_dexterity['acrobatics'] = True
            monk.skills_dexterity['stealth'] = True

            monk.give_item(Item(weapon_name))

            return monk
        case "Ranger":
            ranger = classes.Ranger(name=name,
                                    level=1,
                                    age=random.randint(18, 70))
            ranger.spells_prepared.append(SPELLS["goodberry"])
            ranger.spells_prepared.append(SPELLS["jump"])

            ranger.skills_dexterity['stealth'] = True
            ranger.skills_wisdom['survival'] = True
            ranger.skills_intelligence['nature'] = True

            ranger.give_item(Item(weapon_name))

            return ranger
        case "Druid":
            druid = classes.Druid(name=name,
                                  level=1,
                                  age=random.randint(18, 70))
            druid.spells_prepared.append(SPELLS["guidance"])
            druid.spells_prepared.append(SPELLS["entangle"])
            druid.spells_prepared.append(SPELLS["fog-cloud"])
            druid.spells_prepared.append(SPELLS["goodberry"])
            druid.spells_prepared.append(SPELLS["healing-word"])

            druid.skills_wisdom['survival'] = True
            druid.skills_wisdom['perception'] = True

            druid.give_item(Item(weapon_name))

            return druid
        case "Rogue":
            rogue = classes.Rogue(name=name,
                                  level=1,
                                  age=random.randint(18, 70))
            rogue.skills_dexterity['acrobatics'] = True
            rogue.skills_dexterity['sleight-of-hand'] = True
            rogue.skills_dexterity['stealth'] = True
            rogue.skills_wisdom['insight'] = True

            rogue.give_item(Item(weapon_name))

            return rogue


def create(class_name, name):
    weapon_name = 'quarterstaff' # all characters start with a quarterstaff
    c = __class_creation__(class_name, name, weapon_name)
    spell_list = []
    for sp in c.spells_prepared:
        spell = SpellClass(sp.name, "".join(str(sp.desc)),
                           sp.damage)
        spell_list.append(spell)

    for item in c.inventory:
        if item.weapon_range is not None:
            weapon = WeaponClass(item.name, item.damage.get('damage_dice'), item.weapon_range)
            break
    ch = CharacterClass(c.name, c.class_name, spell_list, c.proficiencies, c.inventory, weapon)
    return ch
