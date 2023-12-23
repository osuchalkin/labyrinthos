from util.text_image import TextImage, Button
import pygame as pg
import sys
import os


class Text(TextImage):
    def __init__(self, game):
        super().__init__(game)
        self.game = game

        self.big_font = pg.font.SysFont(None, (self.settings.HEIGHT // 5))
        self.medium_font = pg.font.SysFont(None, (self.settings.HEIGHT // 10))
        self.small_font = pg.font.SysFont(None, (self.settings.HEIGHT // 20))
        self.name_color = (16, 15, 12)

        x_button_new = (self.settings.WIDTH / 2) - 100
        y_button_new = (self.settings.HEIGHT / 2) + 200
        self.button_new_game = Button(game, x_button_new, y_button_new, 200, 50, (200, 200, 200), 'NEW GAME')

        x_button_load = (self.settings.WIDTH / 2) - 125
        y_button_load = (self.settings.HEIGHT / 2) + 300

        self.button_load_game = Button(game, x_button_load, y_button_load, 250, 50, (200, 200, 200), 'LOAD GAME')
        self.file_name = ''

        self.buttons_saving_games = []
        self.start_text_color = (16, 15, 12)
        self.info_text = ['3D Labyrinths is a fork StanislavPetrovVs DOOM-style-Game 3D:',
                          'https://github.com/StanislavPetrovV/DOOM-style-Game',
                          '',
                          'Generating labyrinths is based on Yan-Minotskiy code:',
                          'https://github.com/Yan-Minotskiy/labyrinth_generating',
                          '',
                          'Texture:',
                          'https://opengameart.org/content/cobblestone-wall-texture',
                          'Edward Burne-Jones - Tile Design - Theseus and the Minotaur in the Labyrinth',
                          'https://opengameart.org/content/wall-of-large-bricks',
                          'https://opengameart.org/content/black-brick-wall-512px',
                          'https://opengameart.org/content/dark-brick-wall-seamless-texture-with-normalmap-darkwallsjpg',
                          '',
                          '',
                          '© Oleh Suchalkin 2023']
        self.control_keys = ['F1 or H - this help',
                             'F2 - save the game',
                             'F3 - load the game',
                             'ESC - save and exit',
                             '',
                             'I - info',
                             'L - choose level',
                             'M - map',
                             '',
                             'WASD - movement',
                             'Mouse Left Click - fire']

    def show_title_screen(self, title):
        self._load_background()

        self.button_new_game.draw_button()
        if self._check_files():
            self.button_load_game.draw_button()

        super().show_title_screen(title)

    def show_text_screen(self, files):
        """show saving files"""
        self._load_background()

        x_button = (self.settings.WIDTH / 2) - 100
        y_button = (self.settings.HEIGHT / 2) - 300
        for index, file in enumerate(files):
            button_game = Button(self.game, x_button, y_button + (50 + 25) * index, 200, 50, (200, 200, 200), file)
            self.buttons_saving_games.append(button_game)

        for button in self.buttons_saving_games:
            button.draw_button()

        while self._check_mouse_choice() is None:
            pg.display.flip()

        return self.file_name

    def show_info_screen(self, title, text):
        title_screen, title_rect = self._make_text_obj(title, self.medium_font, self.text_color)
        title_rect.center = (int(self.settings.WIDTH / 2), 100)
        self.screen.blit(title_screen, title_rect)

        for index, info in enumerate(text):
            title_screen, title_rect = self._make_text_obj(info, self.info_font, self.text_color)
            title_rect.center = (int(self.settings.WIDTH / 2), 300 + 30 * (index + 1))
            self.screen.blit(title_screen, title_rect)

        while super()._check_for_keypress() is None:
            pg.display.flip()

    def show_secret_screen(self, text):
        text_color = (255, 0, 0)
        text_screen, text_rect = self._make_text_obj(text, self.medium_font, text_color)
        text_rect.center = (int(self.settings.WIDTH / 2), int(self.settings.HEIGHT / 2))
        self.screen.blit(text_screen, text_rect)

        pg.display.flip()
        pg.time.delay(1000)

    def choose_level_screen(self):
        title = 'Enter level'
        text_color = (255, 0, 0)
        title_screen, title_rect = self._make_text_obj(title, self.medium_font, text_color)
        title_rect.center = (int(self.settings.WIDTH / 2), 100)
        self.screen.blit(title_screen, title_rect)
        while True:
            level = self.get_name()
            if level.isdecimal() and level != '0':
                return int(level)

    @staticmethod
    def _check_files():
        files = []
        for file in os.listdir():
            if file.endswith('.sav'):
                files.append(file)
        if len(files) == 0:
            return False
        else:
            return True

    def _load_background(self):
        """background image"""
        image = pg.image.load(self.settings.wall_2)
        title_image = pg.transform.scale(image, (self.settings.WIDTH, self.settings.HEIGHT))
        title_rect = title_image.get_rect()
        self.screen.blit(title_image, title_rect)

    def _check_for_keypress(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                self.game.data.end_work()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONUP:
                if self.button_new_game.check_mouse():
                    self.game.enter_name()
                    self.game.new_game()
                    return True
                if self.button_load_game.check_mouse():
                    self.game.load_game()
                    return True
        return None

    def _check_mouse_choice(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                self.game.data.end_work()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONUP:
                for button in self.buttons_saving_games:
                    if button.check_mouse():
                        self.file_name = button.msg
                        return True

        return None
