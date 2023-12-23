import pygame as pg
from settings import Settings


class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.settings = Settings()
        self.path = self.settings.path_sound
        self.volume = self.settings.volume

        self.shotgun = pg.mixer.Sound(self.path + self.settings.shotgun)
        self.npc_pain = pg.mixer.Sound(self.path + self.settings.npc_pain)
        self.npc_death = pg.mixer.Sound(self.path + self.settings.npc_death)
        self.npc_shot = pg.mixer.Sound(self.path + self.settings.npc_attack)
        self.player_pain = pg.mixer.Sound(self.path + self.settings.player_pain)
        self.bonus = pg.mixer.Sound(self.path + self.settings.bonus)

        self.shotgun.set_volume(self.volume)
        self.npc_shot.set_volume(self.volume)
        self.npc_pain.set_volume(self.volume)
        self.npc_death.set_volume(self.volume)
        self.player_pain.set_volume(self.volume)

