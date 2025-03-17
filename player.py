from settings import *
import pygame as pg
import math

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.shot = False
        self.stamina = 150
        self.wornout = False
        self.maxstamina = 150
        self.health = 3
        self.invulnframes = 0
        self.loss = False
        self.health_recovery_delay = 7000
        self.time_prev = pg.time.get_ticks()
        self.inpuzzle = False
        self.won = False

    def recover_health(self):
        if not self.loss:
            if self.check_health_recovery_delay() and self.health < PLAYER_MAX_HEALTH:
                self.health += 1

    def check_health_recovery_delay(self):
        time_now = pg.time.get_ticks()
        if time_now - self.time_prev > self.health_recovery_delay:
            self.time_prev = time_now
            return True
        
    def get_damage(self,damage):
        if not self.game.escape:
            if not self.health < 1:
                if self.invulnframes == 0:
                    self.health -= damage
                    self.game.object_renderer.player_damage()
                    self.game.Sound.player_pain.play()
                    self.invulnframes = 50

    def check_game_over(self):
        if (self.health < 1):
            self.game.object_renderer.game_over()
            pg.display.flip()
            if (self.loss == False):
                self.loss = True
                self.game.Sound.lose.play()

    def check_game_won(self):
        if (self.game.escape): 
            self.game.object_renderer.game_won()
            pg.display.flip()
            if (self.won == False):
                self.won = True
                pg.mixer.stop
                self.game.Sound.win.play()

    def single_fire_event(self,event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if (self.health > 1):
                if (self.game.weapon.active == True):
                    if event.button == 1 and not self.shot:
                        self.game.Sound.spider.play()
                        self.shot = True
                        self.game.weapon.active = False
            else:
                self.game.gtfo()

    def staminaincrease(self):
        global PLAYER_SPEED
        if PLAYER_SPEED == 0.004:
            if self.stamina < self.maxstamina:
                self.stamina += 1
            if self.stamina == self.maxstamina:
                self.wornout = False

    def staminadecrease(self):
        if PLAYER_SPEED > 0.004:
            self.stamina -= 1


    def sprint(self,sprinting):
        if not self.inpuzzle:
            global PLAYER_SPEED
            if self.health > 0:
                if sprinting and not self.wornout:
                    self.stamina -= 1
                    if self.stamina > 0:
                        while PLAYER_SPEED != 0.006:
                            PLAYER_SPEED += 0.001
                    else:
                        self.wornout = True
                else:
                    while PLAYER_SPEED != 0.004:
                        PLAYER_SPEED -= 0.001
                if (not sprinting) or self.wornout:
                    self.staminaincrease()
    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0,0        
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        if self.health > 0 and not self.inpuzzle:
            keys = pg.key.get_pressed()
            if keys[pg.K_w]:
                dx += speed_cos
                dy += speed_sin
            if keys[pg.K_s]:
                dx += -speed_cos
                dy += -speed_sin
            if keys[pg.K_a]:
                dx += speed_sin
                dy += -speed_cos
            if keys[pg.K_d]:
                dx += -speed_sin
                dy += speed_cos

        self.check_wall_collision(dx, dy)


        #if keys[pg.K_LEFT]:
        #    self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
       # if keys[pg.K_RIGHT]:
        #    self.angle += PLAYER_ROT_SPEED * self.game.delta_time

        self.angle %= math.tau

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def draw(self):
        #pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
        #            (self.x * 100 + WIDTH * math.cos(self.angle),
        #            self.y * 100 + WIDTH * math.sin(self.angle)),2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)
        
    def frames(self):
        if self.invulnframes > 0:
            self.invulnframes -= 1

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time
    def update(self):
        self.frames()
        self.movement()
        self.mouse_control()
        self.check_game_over()
        self.check_game_won()
        self.recover_health()
    @property
    def pos(self):
        return self.x, self.y
    
    @property
    def map_pos(self):
        return int(self.x), int(self.y)