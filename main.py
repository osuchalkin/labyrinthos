import json
import sys

from map import Map, MapSaved
from object_handler import ObjectHandler
from settings import Settings
from sound import Sound
from text import Text
from textures import ObjectRenderer
from util.pseudo3d import *
from util.data import Data


class Game(Game3d):
    def __init__(self):
        super().__init__()
        self.data = Data('data.dat', 'data.zip', 'data')
        self.data.start_work()
        pg.mouse.set_visible(True)
        self.settings = Settings()
        self.screen = pg.display.set_mode(self.settings.RES)
        pg.display.set_caption(self.settings.caption)
        pg.display.set_icon(pg.image.load(self.settings.ico))
        self.level = 0
        self.num_npc = self.settings.num_npc
        self.parameters = {}
        self.text = Text(self)
        self.player_name = ''
        self.is_weapon = False
        self.start_game()

    def start_game(self):
        self.text.show_title_screen('Λ Α Β Υ Ρ Ι Ν Θ ΟΙ')

    def new_game(self):
        pg.mouse.set_visible(False)
        self.num_npc = self.settings.num_npc
        self.map = Map(self)
        self.player = Player3d(self)
        if self.level >= 1:
            self.player.y, self.player.x = self.map.start
            self.player.y += 0.5
            self.player.x += 0.5
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting3d(self)
        self.num_npc += self.level
        self.object_handler = ObjectHandler(self, num_npc=self.num_npc)

        self.weapon = Weapon3d(self, path=self.settings.weapon)
        self.sound = Sound(self)
        self.pathfinding = PathFinding3d(self)

        self.level += 1
        self.minotaurus = True

    def restart_game(self):
        """after 'game over'"""
        self.player.health = self.settings.PLAYER_MAX_HEALTH
        self.player.y, self.player.x = self.map.start
        self.player.y += 0.5
        self.player.x += 0.5

    def save_game(self):
        self.parameters = {
            'level': self.level,
            'map': self.map.game_map,
            'start': self.map.start,
            'finish': self.map.finish,
            'x': int(self.player.x),
            'y': int(self.player.y),
            'health': self.player.health,
            'weapon': self.is_weapon,
            'sprites': [sprite.map_pos for sprite in self.object_handler.sprite_list if sprite.color == 'red'],
            'npc_soldier': [npc.map_pos for npc in self.object_handler.npc_soldier_list if npc.alive],
            'npc_demon': [npc.map_pos for npc in self.object_handler.npc_demon_list if npc.alive],
            'minotaur': self.minotaurus,
            'wall': self.object_renderer.wall
        }
        name = self.player_name + '.sav'
        with open(name, "w") as f:
            json.dump(self.parameters, f)

    def load_game(self):
        name = self._find_files()

        with open(name, "r") as f:
            self.parameters = json.load(f)

        self.player_name = name[:-4]
        self.level = self.parameters['level']
        maze = self.parameters['map']
        start = tuple(self.parameters['start'])
        finish = tuple(self.parameters['finish'])
        x = self.parameters['x']
        y = self.parameters['y']
        health = self.parameters['health']
        self.is_weapon = self.parameters['weapon']
        self.loaded_npc_soldier = self.parameters['npc_soldier']
        self.loaded_npc_demon = self.parameters['npc_demon']
        self.loaded_sprites = self.parameters['sprites']
        self.minotaurus = self.parameters['minotaur']
        wall = self.parameters['wall']

        pg.mouse.set_visible(False)
        self.map = MapSaved(self, self.level, maze, start, finish)
        self.player = Player3d(self)
        self.player.y, self.player.x = y + 0.5, x + 0.5
        self.player.health = health

        self.object_renderer = ObjectRenderer(self, wall_text=wall)
        self.raycasting = RayCasting3d(self)

        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon3d(self, path=self.settings.weapon)
        self.sound = Sound(self)
        self.pathfinding = PathFinding3d(self)

    def enter_name(self):
        self.text.show_text_enter_name()
        self.player_name = self.text.get_name(width=200, height=50)

    def _find_files(self):
        files = []
        for file in os.listdir():
            if file.endswith('.sav'):
                files.append(file)
        files.sort(key=os.path.getmtime)

        if len(files) > 10:
            del files[0]
        files.reverse()
        name = self.text.show_text_screen(files)
        return name

    def choose_level(self):
        self.level = self.text.choose_level_screen() - 1
        self.new_game()

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(self.settings.FPS)

    def draw(self):
        self.object_renderer.draw()
        if self.is_weapon:
            self.weapon.draw()

    def draw2d(self):
        self.screen.fill('black')
        size = self.map.draw2d()
        self.player.draw2d(size)
        self.object_handler.draw2d(size)

    def check_events(self):
        for event in pg.event.get():
            self.global_trigger = False
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.save_game()
                pg.quit()
                self.data.end_work()
                sys.exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_F2:  # save game
                self.save_game()
            elif event.type == pg.KEYDOWN and event.key == pg.K_F3:  # load game
                pg.mouse.set_visible(True)
                self.load_game()
            elif event.type == pg.KEYDOWN and event.key == pg.K_m:  # show map
                self.draw2d()
                pg.display.flip()
                pg.time.delay(3000)
            elif event.type == pg.KEYDOWN and event.key == pg.K_l:  # show map
                self.choose_level()
            elif event.type == pg.KEYUP and (event.key == pg.K_F1 or event.key == pg.K_h):
                # help
                self.screen.fill((0, 0, 0))
                self.text.show_info_screen('Controls Keys', self.text.control_keys)
            elif event.type == pg.KEYUP and event.key == pg.K_i:
                # info
                self.screen.fill((0, 0, 0))
                self.text.show_info_screen('Labyrinths', self.text.info_text)
            elif event.type == pg.KEYUP and event.key == pg.K_SPACE:
                self.object_handler.secret_walls()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()

