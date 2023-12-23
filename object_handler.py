import pygame as pg
from util.pseudo3d import SpriteObject3d, AnimatedSprite3d
from random import randint, choice
from copy import deepcopy
from npc import *


class ObjectHandler:
    def __init__(self, game, num_npc=0):
        self.game = game
        self.level = game.level
        self.player = game.player
        self.c_map = deepcopy(self.game.map.game_map)
        self.settings = game.settings  # game.settings
        self.sprite_list = []
        self.npc_soldier_list = []
        self.npc_minotaur_list = []
        self.npc_demon_list = []
        self.sprite_on_map(num_npc)
        self.npc_on_map(num_npc)
        self.npc_positions = {}

    def check_win(self):
        # if self.level == 0: there and back again
        if not len(self.npc_positions) and (
                (self.level == 0 and (int(self.player.y), int(self.player.x)) == self.game.map.start) or
                (self.level > 0 and (int(self.player.y), int(self.player.x)) == self.game.map.finish)):
            self.game.object_renderer.win()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()
        elif self.level == 0 and not len(self.npc_positions) and (int(self.player.y), int(self.player.x)) == self.game.map.finish:
            self.add_new_npc()

    def find_point_on_map(self):
        """help to find empty space on map"""
        while True:
            x = randint(0, len(self.c_map) - 1)
            y = randint(0, len(self.c_map[0]) - 1)
            if self.c_map[x][y] != 1 and self.c_map[x][y] != 2 and self.c_map[x][y] != 3:
                self.c_map[x][y] = 2
                return x, y

    def sprite_on_map(self, num):
        """sprites position on map"""
        if self.level == 0:
            self.add_sprite(
                SpriteObject3d(self.game, path=self.settings.static_sprite_path + self.settings.vase, pos=(14.5, 11.5)))
            self.add_sprite(AnimatedSprite3d(self.game, path=self.settings.anim_sprite_path + self.settings.green_light,
                                             pos=(1.5, 1.5)))
        else:
            start_x, start_y = self.game.map.start
            finish_x, finish_y = self.game.map.finish

            if num > 0:
                self.c_map[start_x][start_y] = 2
                self.c_map[finish_x][finish_y] = 2

            self.add_sprite(AnimatedSprite3d(self.game, path=self.settings.anim_sprite_path + self.settings.green_light,
                                             pos=(start_y + 0.5, start_x + 0.5)))
            self.add_sprite(
                SpriteObject3d(self.game, path=self.settings.static_sprite_path + self.settings.vase,
                               pos=(finish_y + 0.5, finish_x + 0.5)))

        # animated fires
        path = self.settings.anim_sprite_path
        color = self.settings.red_light

        if num == 0:
            for pos_sprite in self.game.loaded_sprites:
                y, x = pos_sprite
                if (x, y) != self.game.map.start and (x, y) != self.game.map.finish:
                    self.add_sprite(AnimatedSprite3d(self.game, path + color, pos=(y + 0.5, x + 0.5), color='red'))
        else:
            num_sprites = randint(1, num)
            i = 0
            while i < num_sprites:
                x, y = self.find_point_on_map()
                if ((self.c_map[x][y + 1] == 1 or self.c_map[x][y - 1] == 1)
                        and (self.c_map[x + 1][y] == 1 or self.c_map[x - 1][y] == 1)):
                    self.add_sprite(AnimatedSprite3d(self.game, path + color, pos=(y + 0.5, x + 0.5), color='red'))
                    i += 1

    def npc_on_map(self, num):
        """npc position on map"""
        finish_x, finish_y = self.game.map.finish

        if num == 0:  # num = 0 for loaded game
            if self.game.parameters['minotaur']:
                self.add_npc(CyberMinotaur(self.game, pos=(finish_y + 0.5, finish_x + 0.5)), 'minotaur')
            for pos_npc in self.game.loaded_npc_soldier:
                y, x = pos_npc
                self.add_npc(Soldier(self.game, pos=(y + 0.5, x + 0.5)), 'soldier')
            for pos_npc in self.game.loaded_npc_demon:
                y, x = pos_npc
                self.add_npc(Demon(self.game, pos=(y + 0.5, x + 0.5)), 'demon')
        else:
            i = 0
            while i < num:
                x, y = self.find_point_on_map()
                self.add_npc(Soldier(self.game, pos=(y + 0.5, x + 0.5)), 'soldier')
                i += 1
            if self.game.level > 1:
                j = 0
                while j < self.game.level - 1:
                    x, y = self.find_point_on_map()
                    self.add_npc(Demon(self.game, pos=(y + 0.5, x + 0.5)), 'demon')
                    j += 1

            self.add_npc(CyberMinotaur(self.game, pos=(finish_y + 0.5, finish_x + 0.5)), 'minotaur')

    def add_new_npc(self):
        i = 0
        while i < self.settings.num_npc:
            x, y = self.find_point_on_map()
            self.add_npc(Soldier(self.game, pos=(y + 0.5, x + 0.5)), 'soldier')
            i += 1

    @property
    def get_npc_positions(self):
        npc_positions = {npc.map_pos for npc in self.npc_soldier_list if npc.alive}
        minotaur_position = {npc.map_pos for npc in self.npc_minotaur_list if npc.alive}
        npc_positions.update(minotaur_position)
        demon_position = {npc.map_pos for npc in self.npc_demon_list if npc.alive}
        npc_positions.update(demon_position)
        return npc_positions

    def update(self):
        self.npc_positions = self.get_npc_positions
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_soldier_list]
        [npc.update() for npc in self.npc_minotaur_list]
        [npc.update() for npc in self.npc_demon_list]
        self.check_win()

    def draw2d(self, size):
        self.npc_positions = self.get_npc_positions
        [sprite.draw2d(size) for sprite in self.sprite_list]
        [npc.draw2d(size) for npc in self.npc_soldier_list if npc.alive]
        [npc.draw2d(size) for npc in self.npc_minotaur_list if npc.alive]
        [npc.draw2d(size) for npc in self.npc_demon_list if npc.alive]

    def add_npc(self, npc, monster):
        if monster == 'soldier':
            self.npc_soldier_list.append(npc)
        if monster == 'minotaur':
            self.npc_minotaur_list.append(npc)
        if monster == 'demon':
            self.npc_demon_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    def secret_walls(self):
        y, x = int(self.game.player.x), int(self.game.player.y)
        if self.check_wall(y, x):
            self.game.sound.bonus.play()
            if not self.game.is_weapon:
                self.game.is_weapon = True
                self.game.text.show_secret_screen('weapon'.upper())
            else:
                secrets = ['health', 'teleport', 'powerful weapon', 'return']
                secret = choice(secrets)
                self.game.text.show_secret_screen(secret.upper())
                self.secrets(secret)

    def check_wall(self, y, x):
        if self.game.map.game_map[x][y + 1] == 3:
            self.game.map.game_map[x][y + 1] = 1
            return True
        elif self.game.map.game_map[x][y - 1] == 3:
            self.game.map.game_map[x][y - 1] = 1
            return True
        elif self.game.map.game_map[x + 1][y] == 3:
            self.game.map.game_map[x + 1][y] = 1
            return True
        elif self.game.map.game_map[x - 1][y] == 3:
            self.game.map.game_map[x - 1][y] = 1
            return True
        else:
            return False

    def secrets(self, secret):
        if secret == 'health':
            self.health()
        elif secret == 'teleport':
            self.teleport()
        elif secret == 'powerful weapon':
            self.powerful_weapon()
        elif secret == 'return':
            self.return_to_start()

    def health(self):
        self.player.health_recovery_delay = 200

    def teleport(self):
        while True:
            x = randint(0, len(self.c_map) - 1)
            y = randint(0, len(self.c_map[0]) - 1)
            if self.c_map[x][y] != 1 and self.c_map[x][y] != 2 and self.c_map[x][y] != 3:
                self.player.y = x + 0.5
                self.player.x = y + 0.5
                break

    def powerful_weapon(self):
        self.game.weapon.damage = 100

    def return_to_start(self):
        self.player.y, self.player.x = self.game.map.start
        self.player.y += 0.5
        self.player.x += 0.5
