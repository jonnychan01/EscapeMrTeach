from sprite_object import *
from random import randint, random ,choice

class NPC(AnimatedSprite):
    def __init__(self, game, path='resources/animated_sprites/teacher/0.png', pos=(23,10), scale=1.2, shift=0.05, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.path = path.rsplit('/', 1)[0]
        self.attack_images = self.get_images(self.path + '/walk')
        self.transform_images = self.get_images(self.path + '/transform')
        self.idle_images = self.get_images(self.path)
        self.rage_images = self.get_images(self.path + '/rage')
        self.walk_images = self.get_images(self.path + '/walk')

        self.puzzlespeed = 0.002
        self.attack_dist = 1
        self.speed = 0.03
        self.size = 10
        self.health = 1000000000
        self.feartimer = 0
        self.attack_damage = 1
        self.accuracy = 0.87
        self.alive = True
        self.fear = False
        self.rage = False
        self.ray_cast_value = False
        self.findquestion = False
        self.frame_counter = 0
        self.player_search_trigger = False
        self.enragetimer = 500
        self.seentime = 0
        self.playingrage = False
        self.framedelay = 0
        self.chasesong = False
        self.maxseentime = 600
        self.wrong = False

    def newpath(self,newpath):
        self.path = newpath.rsplit('/', 1)[0]

    def update(self):
        if not self.game.escape:
            self.check_animation_time()
            self.get_sprite()
            self.walkspeed()
            self.run_logic()
            self.wrongfalse()

    def wrongfalse(self):
        if self.wrong:
            if self.framedelay > 8:
                self.wrong = False
            else:
                self.framedelay += 1
    def wrongspeed(self):
        self.wrong = True
        self.framedelay = 0

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    def movement(self):
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.game.player.map_pos)
        next_x, next_y = next_pos
        angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
        dx = math.cos(angle) * (self.speed + (self.game.puzzles * self.puzzlespeed))
        dy = math.sin(angle) * (self.speed + (self.game.puzzles * self.puzzlespeed))
        self.check_wall_collision(dx, dy)
        
    
    def fearmovement(self):
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.game.player.map_pos)
        next_x, next_y = next_pos
        angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
        dx = math.cos(angle) * -0.09
        dy = math.sin(angle) * -0.09
        self.check_wall_collision(dx, dy)

    def check_hit_in_npc(self):
        if self.ray_cast_value and self.game.player.shot:
            if HALF_WIDTH - self.sprite_half_width< self.screen_x < HALF_WIDTH + self.sprite_half_width:
                self.game.player.shot = False
                self.fear = True
                self.feartimer = 350
                self.game.Sound.flee.play()

    def animate_pain(self):
        self.animate(self.pain_images)
        if self.animation_trigger:
            self.fear == False

    def walkspeed(self):
        if self.playingrage == False:
            self.ray_cast_value = self.ray_cast_player_npc()
            if self.wrong == True:
                self.speed = 0.55
            elif (self.ray_cast_value) and (self.rage == False):
                if (self.fear == False):
                    self.seentime += 1
                self.speed = 0.05
            elif (self.ray_cast_value == False) and (self.rage == False):
                self.speed = 0.025
            elif self.rage:
                self.speed = 0.085
                self.enragetimer -= 1

    def attack(self):
        if self.animation_trigger:
            if random() < self.accuracy:
                self.game.player.get_damage(self.attack_damage)

    def rageorwalk(self):
        if self.game.escape:
            if self.chasesong == True:
                self.game.Sound.step.stop()
        if not self.game.player.loss:
            if self.rage:
                self.animate(self.rage_images)
                if self.chasesong == False:
                    self.chasesong = True
                    self.game.Sound.step.play(0,0,100)
            else:
                self.animate(self.walk_images)
                if self.chasesong == True:
                    self.chasesong = False
                    self.game.Sound.step.fadeout(400)
        else:
            self.game.Sound.step.stop()
    def run_logic(self):
        if (self.enragetimer == 0) and (self.rage == True):
            self.rage = False
            self.frame_counter = 0
        if self.alive:
            self.ray_cast_value = self.ray_cast_player_npc()
            if self.ray_cast_value or self.seentime > self.maxseentime:
                if self.seentime > self.maxseentime and (not self.game.player.loss):
                    if not self.rage:
                        self.playingrage = True
                        self.speed = 0
                    if self.playingrage and not self.rage:
                        if (self.frame_counter < (len(self.transform_images) - 1)):
                            self.transform_images.rotate(-1)
                            self.image = self.transform_images[0]
                            self.frame_counter += 1
                        elif (self.frame_counter < (len(self.transform_images) - 1)):
                            self.playingrage = False
                            self.rage = True
                        else:
                            self.playingrage = False
                            self.rage = True
                    else:
                        self.enragetimer = 500
                        self.seentime = 0
            self.check_hit_in_npc()
            if not self.playingrage:
                if self.fear:
                    if self.feartimer > 0:
                        self.feartimer -= 1
                    else:
                        self.fear = False
                    self.animate(self.walk_images)
                    self.fearmovement()
                elif self.findquestion:
                    if self.ray_cast_value:
                        if self.dist < self.attack_dist:
                            self.rageorwalk()
                            self.attack()
                        else:
                            self.findquestion = False
                    else:
                        self.player_search_trigger = True
                        self.rageorwalk()
                        self.movement()
                elif self.ray_cast_value:
                    if self.dist < self.attack_dist:
                        self.rageorwalk()
                        self.attack()
                    else:
                        self.player_search_trigger = True
                        self.rageorwalk()
                        self.movement()
                elif self.player_search_trigger:
                    self.rageorwalk()
                    self.movement()
                else:
                    self.animate(self.idle_images)
        else:
            self.animate_death()

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
    
    def ray_cast_player_npc(self):
        if self.game.player.map_pos == self.map_pos:
            return True

        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0


        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.theta
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # horizontals
        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a

        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        # verticals
        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth
        
        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False
    