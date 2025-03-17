import pygame as pg


class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = 'resources/sound/'
        self.flee = pg.mixer.Sound(self.path + 'skedaddle.mp3')
        self.lose = pg.mixer.Sound(self.path + 'GAMEOVER.mp3')
        self.win = pg.mixer.Sound(self.path + 'hooray.mp3')
        self.step = pg.mixer.Sound(self.path + 'run.mp3')
        self.spider = pg.mixer.Sound(self.path + 'spider.mp3')
        self.player_pain = pg.mixer.Sound(self.path + 'damage.mp3')
        self.footstep = pg.mixer.Sound(self.path + 'footstep.mp3')
        self.softstep1 = pg.mixer.Sound(self.path + 'softstep_1.wav')
        self.softstep2 = pg.mixer.Sound(self.path + 'softstep_2.wav')
        self.softstep3 = pg.mixer.Sound(self.path + 'softstep_3.wav')
        self.softstep4 = pg.mixer.Sound(self.path + 'softstep_4.wav')

        self.softarray = [self.softstep1,self.softstep2,self.softstep3,self.softstep4]



        self.player_pain.set_volume(0.3)
        self.footstep.set_volume(0.3)
        self.step.set_volume(0.3)