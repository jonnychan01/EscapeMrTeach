import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import * 
from object_renderer import *
from sprite_object import * 
from object_handler import * 
from weapon import * 
from sound import * 
from pathfinding import *
import random


class Game():
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.new_game()
        self.sprinting = False
        self.puzzles = 0
        self.escape = False
        self.wrongans = False

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.Sound = Sound(self)
        self.pathfinding = PathFinding(self)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update() 
        self.weapon.update()

        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(str(self.player.stamina))
        #pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        #self.screen.fill('black')
        self.object_renderer.draw()
        self.weapon.draw()
        #self.map.draw()
        #self.player.draw()

    def gtfo(self):
        pg.quit()

    def check_events(self):
        global PLAYER_SPEED
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)
            if event.type == pg.KEYDOWN and (event.key == pg.K_LSHIFT or event.key == pg.K_RSHIFT):
                self.sprinting = True
            if event.type == pg.KEYUP and (event.key == pg.K_LSHIFT or event.key == pg.K_RSHIFT):
                self.sprinting = False
            #if event.type == pg.KEYDOWN and (event.key == pg.K_r):
            #    self.player.start_new_game()
            self.player.sprint(self.sprinting)
            if (event.type == pg.KEYDOWN and event.key == pg.K_e):
                playx, playy = self.player.pos
                for i in range(0, (len(self.object_handler.sprite_list))):
                    try:
                        if(playx < placedlocs[i][0] + 1) and (playy < placedlocs[i][1] + 1) and (playx > placedlocs[i][0] - 1) and (playy > placedlocs[i][1] - 1):
                            if self.object_handler.sprite_list[i].pos == spiderloc[0]:
                                self.weapon.active = True
                            if self.object_handler.sprite_list[i].pos != doorloc[0]:
                                if self.object_handler.sprite_list[i].pos != spiderloc[0]:
                                    
                                    #CALL A PUZZLE FUNCTION HERE
                                    ran = random.randint(0,len(inMapPuzzles)-1)
                                    inMapPuzzles[ran].checkAns(self) #the self in main.py is the game in game.blit
                                    self.puzzles += 1
                                    inMapPuzzles.pop(ran)
                                    if self.wrongans == True: #if wrong answer
                                        self.wrongans = False  
                                        self.object_handler.npc_list[0].wrongspeed()
                                placedlocs.pop(i)
                                self.object_handler.sprite_list.pop(i)

                            elif self.object_handler.sprite_list[i].pos == doorloc[0] and (self.puzzles >= 3):
                                self.escape = True
                                placedlocs.pop(i)
                                self.object_handler.sprite_list.pop(i)
                    except:
                        IndexError


    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = Game()
    game.run()