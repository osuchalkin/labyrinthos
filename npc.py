from util.pseudo3d import NPC3d


class Soldier(NPC3d):
    def __init__(self, game, path='data/sprites/npc/soldier/0.png', pos=(1.5, 1.5),
                 scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)


class Demon(NPC3d):
    def __init__(self, game, path='data/sprites/npc/caco_demon/0.png', pos=(1.5, 1.5),
                 scale=0.7, shift=0.27, animation_time=250):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_dist = 1.0
        self.health = 200
        self.attack_damage = 25
        self.speed = 0.01
        self.accuracy = 0.35


class CyberMinotaur(NPC3d):
    def __init__(self, game, path='data/sprites/npc/cyber_min/0.png', pos=(1.5, 1.5),
                 scale=1.0, shift=0.04, animation_time=210):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.game = game
        self.attack_dist = 6
        self.health = 400
        self.attack_damage = 15
        self.speed = 0.055
        self.accuracy = 0.25

    def movement(self):
        pass

    def check_health(self):
        if self.health < 1:
            self.alive = False
            self.game.minotaurus = False
            self.game.sound.npc_death.play()
