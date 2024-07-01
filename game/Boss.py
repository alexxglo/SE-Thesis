import arcade
import spacy
from arcade import Texture
from dnd_character.monsters import Monster
from openai import OpenAI
import PIL.Image
import settings

from Attack import Attack

HEALTHBAR_WIDTH = 256
HEALTHBAR_HEIGHT = 3
HEALTHBAR_OFFSET_Y = -220
HEALTH_NUMBER_OFFSET_X = -130
HEALTH_NUMBER_OFFSET_Y = -250
mob_list = ['adult-blue-dragon', 'air-elemental', 'androsphinx', 'animated-armor', 'archmage', 'ape', 'assassin',
            'baboon',
            'badger', 'bandit', 'barbed-devil', 'basilisk', 'bat', 'berserker', 'black-bear', 'camel', 'cat', 'centaur',
            'cloud-giant', 'cultist', 'cult-fanatic', 'death-dog', 'darkmantle', 'deer', 'dire-wolf', 'djinni',
            'doppelganger',
            'draft-horse', 'dretch', 'druid', 'eagle', 'elephant', 'elk', 'ettin', 'fire-elemental', 'flying-snake',
            'frog',
            'gargoyle', 'ghost', 'gladiator', 'gnoll', 'goat', 'gray-ooze', 'harpy', 'hawk', 'hyena', 'hydra', 'imp',
            'jackal', 'killer-whale',
            'knight', 'kobold', 'kraken', 'lemure', 'lich', 'lion', 'lizard', 'mage', 'mastiff', 'medusa', 'minotaur',
            'mule',
            'mummy', 'octopus', 'orc', 'noble', 'nightmare', 'panther', 'pegasus', 'pony', 'priest', 'rat', 'raven',
            'rhinoceros',
            'salamander', 'scorpion', 'scout', 'sea-horse', 'solar', 'spider', 'sprite', 'specter', 'spider', 'spy',
            'thug', 'tiger',
            'vampire', 'unicorn', 'vulture', 'wolf', 'wraith', 'wyvern']


def predictMob(mob_input):
    nlp = spacy.load("en_core_web_sm")
    # Process the input text with spaCy
    input_doc = nlp(mob_input)
    # Calculate similarity scores between the input text and each option
    option_similarities = {option: input_doc.similarity(nlp(option)) for option in mob_list}
    # Choose the option with the highest similarity score
    chosen_option = max(option_similarities, key=option_similarities.get)
    return chosen_option


def generate_boss_name(input):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user",
             "content": "In one word, summarize the next sentence into a person name or a word that can describe the thing:" + input
             }
        ]
    )
    return completion.choices[0].message.content.rsplit('.', 1)[0]


def generate_main_attack_name(input):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user",
             "content": "In maximum three words, create an attack name that a villain with the name: " + input + " might have, but don't use the villain name in it"
             }
        ]
    )
    return completion.choices[0].message.content.rsplit('.', 1)[0]
    return "Generic default ability"


class Boss(arcade.Sprite):
    def __init__(self, mob_input):
        super().__init__('resources/boss.png', 1)
        # Predict monster name and class
        self.mob = Monster(predictMob(mob_input))
        self.name = generate_boss_name(mob_input)
        # self.name = "Bald Eagle"
        # Add extra attributes for health
        self.max_health = 100
        self.cur_health = 100
        self.center_x = 1920 / 1.2
        self.center_y = 1080 / 1.75
        self.attack = Attack(generate_main_attack_name(self.name), "2d20", "")
        self.append_texture(Texture(name="dead_state", image=PIL.Image.open("resources/dead_pic.png")))

    def draw_health_number(self):
        """ Draw how many hit points we have """

        health_string = f"{self.cur_health}/{self.max_health}"
        arcade.draw_text(health_string,
                         start_x=self.center_x + HEALTH_NUMBER_OFFSET_X,
                         start_y=self.center_y + HEALTH_NUMBER_OFFSET_Y,
                         font_size=12,
                         color=arcade.color.WHITE)
        arcade.draw_text(self.name, 1600, 430, arcade.color.WHITE, 30, anchor_x="center")

    def draw_health_bar(self):
        """ Draw the health bar """
        # Draw the 'unhealthy' background
        if self.cur_health < self.max_health:
            arcade.draw_rectangle_filled(center_x=self.center_x,
                                         center_y=self.center_y + HEALTHBAR_OFFSET_Y,
                                         width=HEALTHBAR_WIDTH,
                                         height=3,
                                         color=arcade.color.RED)
            # Calculate width based on health
        health_width = HEALTHBAR_WIDTH * (self.cur_health / self.max_health)
        arcade.draw_rectangle_filled(center_x=self.center_x - 0.5 * (HEALTHBAR_WIDTH - health_width),
                                     center_y=(self.center_y + HEALTHBAR_OFFSET_Y),
                                     width=health_width,
                                     height=HEALTHBAR_HEIGHT,
                                     color=arcade.color.GREEN)
