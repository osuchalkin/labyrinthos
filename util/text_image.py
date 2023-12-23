# TextImage && Button classes

import pygame.font
import pygame as pg
import sys


class TextImage:
    """
    to display text information
    You need game.settings.WIDTH, game.settings.HEIGHT - game screen width and height
    """

    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.text_color = (235, 226, 220)
        self.text_shadow_color = (46, 44, 43)
        self.name_color = (255, 85, 0)
        self.small_font = pygame.font.SysFont(None, (self.settings.HEIGHT // 16))
        self.big_font = pygame.font.SysFont(None, (self.settings.HEIGHT // 10))
        self.next_font = pygame.font.SysFont(None, (self.settings.HEIGHT // 20))
        self.info_font = pygame.font.SysFont(None, (self.settings.HEIGHT // 33))

        self.info_text = ['', '', ]
        self.control_keys = ['', '', ]

    @staticmethod
    def _make_text_obj(text, font, color):
        """Вспомогательная для отображения текста """
        image = font.render(text, True, color)
        image_rect = image.get_rect()
        return image, image_rect

    def _check_for_keypress(self):
        for event in pg.event.get(pg.QUIT):  # get all the QUIT event
            pg.quit()
            sys.exit()
        for event in pg.event.get([pg.KEYDOWN, pg.KEYUP]):
            if event == pg.KEYDOWN:
                continue
            return event.key
        return None

    def show_title_screen(self, title):
        """shows large text in the center of the screen - title, ending, etc."""
        # drawing shadow
        title_screen, title_rect = self._make_text_obj(title, self.big_font, self.text_shadow_color)
        title_rect.center = (int(self.settings.WIDTH / 2),
                             int(self.settings.HEIGHT / 2))
        self.screen.blit(title_screen, title_rect)

        # drawing text
        title_screen, title_rect = self._make_text_obj(title, self.big_font, self.text_color)
        title_rect.center = (int(self.settings.WIDTH / 2) - 3,
                             int(self.settings.HEIGHT / 2) - 3)
        self.screen.blit(title_screen, title_rect)

        while self._check_for_keypress() is None:
            pg.display.flip()

    def show_text_screen(self, text):
        """show text on the screen - ['', '', ...]"""
        for index, info in enumerate(text):
            title_screen, title_rect = self._make_text_obj(info, self.info_font, self.text_color)
            title_rect.center = (int(self.settings.WIDTH / 2), 300 + 30 * (index + 1))
            self.screen.blit(title_screen, title_rect)

        while self._check_for_keypress() is None:
            pg.display.flip()

    def show_text_enter_name(self):
        title_screen = self.small_font.render('Enter your name:', True, self.name_color)
        title_rect = title_screen.get_rect()
        title_rect.center = (int(self.settings.WIDTH / 2),
                             int(self.settings.HEIGHT / 2) - (self.settings.HEIGHT // 8))
        self.screen.blit(title_screen, title_rect)

        pg.display.flip()

    def get_name(self, width=400, height=100, num_symbols=8):
        """Getter player's name"""
        # input window parameters
        screen_width, screen_height = width, height
        screen_color = (255, 255, 255)
        screen_rect = pg.Rect(0, 0, screen_width, screen_height)
        screen_rect.midbottom = self.screen_rect.center
        # get input
        name = ""
        input_active = True
        while input_active:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    input_active = True
                    name = ""
                elif event.type == pg.KEYDOWN and input_active:
                    if event.key == pg.K_RETURN:
                        input_active = False
                    elif event.key == pg.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode
                        if len(name) > num_symbols:
                            name = name[:-1]
                # display the input window
                self.screen.fill(screen_color, screen_rect)
                name_image = self.small_font.render(name, True, self.name_color)
                name_image_rect = name_image.get_rect()
                name_image_rect.center = screen_rect.center
                self.screen.blit(name_image, name_image_rect)

                pg.display.flip()

        return name


class Button:

    def __init__(self, game, x, y, width, height, color, msg):
        """Initialize button attributes."""
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = width, height
        self.x, self.y = x, y
        self.button_color = color
        self.text_color = (15, 15, 15)
        self.msg = msg
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it.
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        # self.rect.center = self.screen_rect.center <- if you need to center

        # The button message needs to be prepped only once.
        self._prep_msg(self.msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def check_mouse(self):
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            return True
