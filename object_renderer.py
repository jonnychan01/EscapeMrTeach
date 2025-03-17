import pygame as pg
from settings import*

class ObjectRenderer:
    def __init__(self,game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('resources/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0 
        self.blood_screen = self.get_texture('resources/textures/bigpain.png', RES)
        self.digit_size = 90
        self.digit_images = [self.get_texture(f'resources/textures/digits/{i}.png', [self.digit_size] * 2)
                             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        self.game_over_image = self.get_texture('resources/textures/game_over.png', RES)
        self.win_image = self.get_texture('resources/textures/gamewon.jpg', RES)
        self.healthheart = self.get_texture('resources/textures/heart.png', (30, 30))
        self.staminaicon = self.get_texture('resources/textures/stamina-icon.png', (20, 20))
        #self.win_image = self.get_texture('resources/textures/win.png', RES)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE,TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture,res)
    
    def player_damage(self):
        self.screen.blit(self.blood_screen, (0,0))

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        # floor
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def game_won(self):
        self.screen.blit(self.win_image, (0, 0))
        

    def draw_player_health(self):
        # health = str(round(((self.game.player.health)/PLAYER_MAX_HEALTH) * 100))
        # for i, char in enumerate(health):
        #     self.screen.blit(self.digits[char], (i * self.digit_size, HEIGHT-100))
        # self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, HEIGHT-100))

        #calculate health to damage ratio
        ratio = self.game.player.health / PLAYER_MAX_HEALTH
        pg.draw.rect(self.screen, "red", (50, 825, 300, 40)) #red bar in background
        pg.draw.rect(self.screen, "green", (50, 825, 300 * ratio, 40)) #green bar
        self.screen.blit(self.healthheart, (355, 830)) #adds heart icon

    def draw_player_stamina(self):
        # stamina = str(round((self.game.player.stamina)/(self.game.player.maxstamina) * 100))
        # if round((self.game.player.stamina)/(self.game.player.maxstamina) * 100) == 100:
        #     for i, char in enumerate(stamina):
        #         self.screen.blit(self.digits[char], (((i * self.digit_size)) + 1240, HEIGHT-100))
        #     self.screen.blit(self.digits['10'], (((i + 1) * self.digit_size) + 1240, HEIGHT-100))
        # else:
        #     for i, char in enumerate(stamina):
        #         self.screen.blit(self.digits[char], (((i * self.digit_size)) + 1330, HEIGHT-100))
        #     self.screen.blit(self.digits['10'], (((i + 1) * self.digit_size) + 1330, HEIGHT-100))

        staminaratio = self.game.player.stamina / self.game.player.maxstamina
        pg.draw.rect(self.screen, "grey", (50, 800, 300, 20)) # grey background bar
        pg.draw.rect(self.screen, "white", (50, 800, 300 * staminaratio, 20)) # white background bar
        self.screen.blit(self.staminaicon, (355, 805)) #adds stamina icon

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()
        self.draw_player_stamina()

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)
    
    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/2.png'),
            3: self.get_texture('resources/textures/3.png'),
            4: self.get_texture('resources/textures/4.png'),
            5: self.get_texture('resources/textures/1.png'),
        }