from openai import OpenAI
import settings
from random import randint

from Attack import Attack

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def generate_story(player_data):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are a Dungeons and Dragons game organizer that can create narrative stories."},
            {"role": "user",
             "content": "In about 70 words, create a story introduction based on the following elements:" +
                        "Final boss is: " + player_data[0]['finalBoss'] +
                        "Location of adventure is: " + player_data[0]['location'] +
                        "The element conjuring the grounds is: " + player_data[0]['element'] +
                        "The theme of the adventure is: " + player_data[0]['theme']}
        ]
    )
    return completion.choices[0].message


def d(sides):
    return randint(1, sides)


def roll(n, sides):
    return tuple(d(sides) for _ in range(n))


def adjust_attack(no_of_players):
    if no_of_players == 2:
        return "1d20"
    elif no_of_players == 3:
        return "1d15"
    elif no_of_players == 4:
        return "1d10"
    return "2d20"


def roll_dice(dice_value):
    split_dice = dice_value.split("d")
    nof_dice = int(split_dice[0])
    value = int(split_dice[1])
    return sum(roll(nof_dice, value))


def roll_player_dice(dice_value, no_of_players):
    dice_value = adjust_attack(no_of_players)
    split_dice = dice_value.split("d")
    nof_dice = int(split_dice[0])
    value = int(split_dice[1])
    return sum(roll(nof_dice, value))


def create_player_options(player):
    options_list = [Attack("Normal Attack", "1d6", "Execute a normal attack")]
    for spell in player.spells:
        options_list.append(Attack(spell.name, spell.damage, spell.description))
    return options_list


def check_if_players_all_dead(player_list):
    total_hp = 0
    for player in player_list:
        total_hp = total_hp + player.cur_health
    if total_hp > 0:
        return 0
    return 1


def choose_boss_target(player_list):
    if check_if_players_all_dead(player_list) == 1:  # check if all players dead
        return -1
    while 1 > 0:
        randomize_attack = randint(0, len(player_list) - 1)  # randomize attack
        if player_list[randomize_attack].cur_health > 0:  # check if player not already dead
            return randomize_attack
