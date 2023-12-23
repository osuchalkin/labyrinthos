from util.pseudo3d import ObjectRenderer3d
from random import randint


class ObjectRenderer(ObjectRenderer3d):
    def __init__(self, game, wall_text=-1):
        super().__init__(game)
        self.settings = game.settings

        self.path_textures = self.settings.path_textures
        self.path_textures_2 = self.settings.path_textures_2
        self.texture_images = [f'{self.path_textures}wall{i}.png' for i in range(self.settings.num_textures)]
        self.texture_2_images = [f'{self.path_textures_2}wall{i}.png' for i in range(self.settings.num_textures)]
        if wall_text == -1:
            if self.game.level == 0:
                self.wall = 0
            else:
                # select textures
                self.wall = randint(0, len(self.texture_images) - 1)
        else:
            self.wall = wall_text

        self.texture = self.texture_images[self.wall]
        self.texture_2 = self.texture_2_images[self.wall]
        self.wall_textures = self.load_wall_textures()

        self.sky_image = self.get_texture(self.settings.sky_image, (self.settings.WIDTH, self.settings.HALF_HEIGHT))
        self.blood_screen = self.get_texture(self.settings.blood_screen, self.settings.RES)

        self.digit_size = self.settings.digit_size
        self.path_digits = self.settings.path_digit_images
        self.digit_images = [self.get_texture(f'{self.path_digits}{i}.png', [self.digit_size] * 2)
                             for i in range(13)]
        self.digits = dict(zip(map(str, range(13)), self.digit_images))

        self.game_over_image = self.get_texture(self.settings.game_over_image, self.settings.RES)
        self.win_image = self.get_texture(self.settings.win_image, self.settings.RES)

    def load_wall_textures(self):
        return {
            1: self.get_texture(self.texture),
            2: self.get_texture(self.settings.wall_2),
            3: self.get_texture(self.texture_2),
        }

    def draw(self):
        super().draw()
        self.draw_level()
        self.draw_number_enemies()

    def draw_level(self):
        level = str(self.game.level)
        self.screen.blit(self.digits['11'], ((self.game.settings.WIDTH - 210), 0))
        for i, char in enumerate(level):
            self.screen.blit(self.digits[char], ((self.game.settings.WIDTH - 150) + i * self.digit_size, 0))

    def draw_number_enemies(self):
        enemies = str(len(self.game.object_handler.get_npc_positions))
        self.screen.blit(self.digits['12'], ((self.game.settings.WIDTH / 2 - 60), 0))
        for i, char in enumerate(enemies):
            self.screen.blit(self.digits[char], ((self.game.settings.WIDTH / 2) + i * self.digit_size, 0))
