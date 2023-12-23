from util.pseudo3d import Settings3d


class Settings(Settings3d):
    def __init__(self):
        super().__init__()
        # window
        self.caption = 'ΛΑΒΥΡΙΝΘΟΙ'
        self.ico = 'data/labyrinth.ico'

        # textures
        self.num_textures = 5  # number of texture files
        self.path_textures = 'data/textures/walls/'
        self.path_textures_2 = 'data/textures/walls-2/'
        self.sky_image = 'data/textures/sky2.png'
        self.blood_screen = 'data/textures/blood_screen.png'
        self.digit_size = 50
        self.path_digit_images = 'data/textures/digits/'  # png!
        self.game_over_image = 'data/textures/game_over.png'
        self.win_image = 'data/textures/win.png'

        self.wall_1 = f'{self.path_textures}wall0.png'
        self.wall_2 = 'data/textures/Edward_Burne-Jones-Theseus_and_the_Minotaur.png'
        self.wall_11 = f'{self.path_textures_2}wall0.png'

        # sprites
        self.static_sprite_path = 'data/sprites/static/'
        self.anim_sprite_path = 'data/sprites/animated/'
        self.vase = 'vase.png'
        self.green_light = 'green_light/0.png'
        self.red_light = 'red_light/0.png'

        # npc
        self.npc_sprite_path = 'data/sprites/npc/'
        self.soldier = 'data/sprites/npc/soldier/0.png'
        self.num_npc = 5

        # weapon
        self.weapon = 'data/sprites/weapon/shotgun/0.png'

        # sound
        self.path_sound = 'data/sound/'
        self.shotgun = 'shotgun.wav'
        self.npc_pain = 'npc_pain.wav'
        self.npc_death = 'npc_death.wav'
        self.npc_attack = 'npc_attack.wav'
        self.player_pain = 'player_pain.wav'
        self.bonus = 'bonus.wav'

        self.volume = 0.1  # not loudly
