import time

import arcade
import threading

import jsonpickle

import settings
from BattleMessage import BattleMessage
from Boss import Boss
from Character import Character
import story_mechanics
from classes.CharacterPayloadResponse import CharacterPayloadResponse
from classes.PlayerNextAttack import PlayerNextAttack
from views import end_view


def increment_message_pos(pos):
    if pos == 9:
        return 0
    return pos + 1


def commence_battle(input_player_list, boss, battle_message, window):
    player_list_attacks = []

    for player in input_player_list:
        player_attacks = story_mechanics.create_player_options(player.character)
        player_list_attacks.append(player_attacks)

    while boss.cur_health > 0 and story_mechanics.check_if_players_all_dead(input_player_list) == 0:
        for player_pos, player_ in enumerate(input_player_list):
            if player_.cur_health > 0:
                player_ = PlayerNextAttack(player_.character.name, settings.ROOM_CODE)
                settings.emit_next_attack(jsonpickle.dumps(player_, unpicklable=False))
                flag = 0
                while flag == 0:
                    event = settings.sio.receive()
                    if event[0] == "get_attack":
                        flag = 1
                        attack_data = event[1:]
                        action = attack_data[0]['ability']
                        attack = story_mechanics.roll_player_dice(attack_data[0]['damage'], len(input_player_list))
                        battle_message.message = attack_data[0]['name'] + " has selected: " + action
                        time.sleep(1)
                        battle_message.message = attack_data[0]['name'] + " rolls " + str(attack)
                        boss.cur_health = boss.cur_health - attack
                        if boss.cur_health <= 0:
                            boss.cur_health = 0
                            time.sleep(4)
                            end = end_view.EndView(False)
                            window.show_view(end)
                            break
                        time.sleep(1)

        if boss.cur_health > 0:
            boss_attack = story_mechanics.roll_dice(boss.attack.damage)
            battle_message.message = boss.name + " has selected: " + boss.attack.name
            time.sleep(1)
            battle_message.message = boss.name + " rolls " + str(boss_attack)
            time.sleep(1)

            target = story_mechanics.choose_boss_target(input_player_list)
            if target == -1:  # all players dead
                time.sleep(4)
                end = end_view.EndView(True)
                window.show_view(end)
                break
            input_player_list[target].cur_health = input_player_list[target].cur_health - boss_attack
            if input_player_list[target].cur_health <= 0:
                battle_message.message = input_player_list[target].character.name + " has died!"
            else:
                battle_message.message = input_player_list[target].character.name + " now has " + str(
                    input_player_list[target].cur_health) + " hp"
        else:
            battle_message.message = boss.name + " has died!"
            break
    if story_mechanics.choose_boss_target(input_player_list) == -1:
        time.sleep(4)
        end = end_view.EndView(True)
        window.show_view(end)


class BattleView(arcade.View):
    """ Class to manage the game overview """

    def __init__(self, boss_prompt, player_data):
        super().__init__()
        self.player_list = None
        self.player_name_list = None
        self.sprite_list = None
        self.battle_log = None
        self.background = None
        self.boss = None
        self.boss_prompt = boss_prompt
        self.player_data = player_data
        self.relative_height = []

    def set_relative_h(self):
        if len(self.player_data) == 1:
            self.relative_height = [580]
        elif len(self.player_data) == 2:
            self.relative_height = [440, 640]
        elif len(self.player_data) == 3:
            self.relative_height = [270, 540, 810]
        else:
            self.relative_height = [216, 450, 670, 900]

    def on_update(self, delta_time: float):
        self.on_draw()

    def on_show_view(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        """ This should set up your game and get it ready to play """
        self.background = arcade.load_texture('resources/background.jpg')
        self.player_list = arcade.SpriteList()
        self.sprite_list = arcade.SpriteList()

        self.battle_log = arcade.Sprite('resources/log.png', scale=0.2)
        self.battle_log.center_x = 1920 / 2.2
        self.battle_log.center_y = 1080 / 1.9

        self.sprite_list.append(self.battle_log)

        self.set_relative_h()

        for player_pos, p in enumerate(self.player_data):
            player = Character(p['name'], p['characterClass'],
                               'resources/pfp/' + p['characterClass'].lower() + '_pfp.png', 1)
            player.center_x = 1920 / 15
            player.center_y = self.relative_height[player_pos]
            player.cur_health = 100
            self.player_list.append(player)

        boss = Boss(self.boss_prompt)
        self.boss = boss
        self.sprite_list.append(boss)

        c = CharacterPayloadResponse(self.player_list)
        settings.emit_player_info(jsonpickle.dumps(c, unpicklable=False))

        self.sprite_list.append(BattleMessage(message="", pos_x=1080 / 2, pos_y=500))
        t1 = threading.Thread(target=commence_battle,
                              args=(self.player_list, self.boss, self.sprite_list[2], self.window))
        t1.start()

    def on_draw(self):
        """ Draw the game overview """
        self.clear()
        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            1920, 1080,
                                            self.background)
        self.player_list.draw(pixelated=True)
        for player_pos, player in enumerate(self.player_list):
            player.draw_health_number()
            player.draw_health_bar()
            arcade.draw_text(self.player_data[player_pos]['name'], 1920 / 7,
                             self.relative_height[player_pos] + 20,
                             arcade.color.WHITE, 20, anchor_x="center")
        self.sprite_list.draw(pixelated=True)
        self.sprite_list[1].draw_health_number()
        self.sprite_list[1].draw_health_bar()
        self.sprite_list[2].draw_message()
