from sprite_object import *
from npc import *
from map import placedlocs, doorloc
class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.static_sprite_path = 'resources/textures'
        self.anim_sprite_path = 'resources/textures/animated_sprites'
        self.anim_sprite_path = 'resources/textures/animated_sprites/teacher'
        add_sprite = self.add_sprite
        add_npc = self.add_npc

        add_sprite(SpriteObject(game, pos=placedlocs[0]))
        add_sprite(SpriteObject(game, pos=placedlocs[1]))
        add_sprite(SpriteObject(game, pos=placedlocs[2]))
        add_sprite(SpriteObject(game, path='resources/weapon/spider/0.png',pos=placedlocs[3], objtype=2))
        add_sprite(SpriteObject(game, path='resources/textures/emptyexit.png',pos=placedlocs[4], objtype=4))
    
        add_npc(NPC(game))
        self.npc_positions = {}

    def update(self):
        if self.game.puzzles >= 3:
            for count in range(len(self.sprite_list)):
                if self.sprite_list[count].path == 'resources/textures/emptyexit.png':
                    self.sprite_list[count].path = 'resources/textures/exit.png'
                    self.sprite_list[count].image = pg.image.load(self.sprite_list[count].path).convert_alpha()
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]

    def add_npc(self,npc):
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)