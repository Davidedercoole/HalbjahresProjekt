#sprites
import pygame as pg
import os
from settings import *
from random import choice, randrange
vec = pg.math.Vector2


class spritesheet:
    #zum laden von spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
        self.spritesheet2 = pg.image.load(filename).convert() 

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image.blit(self.spritesheet2, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        return image


class Player(pg.sprite.Sprite):
    def __init__(self,game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.laufen = False
        self.sprung = False
        self.current_frame = 0
        self.last_update = 0
        self.bild_laden()
        self.image = self.stehen_frames[0]
        
      
        self.rect = self.image.get_rect()
        self.rect.center = (40, HEIGHT - 100)
        self.pos = vec(40, HEIGHT - 100)
        self.vel = vec(0, 0)
        self.speed = vec(0, 0)


    def bild_laden(self):
        self.stehen_frames = [self.game.spritesheet.get_image( 260, 1032, 128, 256),
                            self.game.spritesheet.get_image(260 ,258 ,128 ,256)]
        for frame in self.stehen_frames:
            frame.set_colorkey(Black)
        self.laufen_frames_r = [self.game.spritesheet.get_image(130, 1290, 128, 256),
                            self.game.spritesheet.get_image(130 ,1032 ,128 ,256)]
        for frame in self.laufen_frames_r:
            frame.set_colorkey(Black)

        self.laufen_frames_l =[]
        for frame in self.laufen_frames_r:
            frame.set_colorkey(Black)
            self.laufen_frames_l.append(pg.transform.flip(frame, True, False))

        self.sprung_frames = [self.game.spritesheet.get_image(260, 516, 128, 256)]
        for frame in self.sprung_frames:
            frame.set_colorkey(Black)

    def jump_cut(self):
        if self.sprung:
            if self.vel.y < -5:
                self.vel.y = -5


    def jump(self):
        #nur spring wenn auf platform
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.platformen, False)
        self.rect.x -= 2
        if hits and not self.sprung:
            self.game.jump_sound.play()
            self.sprung = True
            self.vel.y = -PLAYER_JUMP
        


    def update(self):
        self.animate()
        self.speed = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.speed.x -= PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.speed.x = PLAYER_ACC
        
        self.speed.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.speed
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.speed

        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2
        

        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.laufen = True
        else:
            self.laufen = False
        #lauf animation
        if self.laufen:
            if now - self.last_update > 300:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.laufen_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.laufen_frames_r[self.current_frame]
                else:
                    self.image = self.laufen_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        #idle animation
        if not self.sprung and not self.laufen:
            if now - self.last_update > 400:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.stehen_frames)
                bottom = self.rect.bottom
                top = self.rect.top
                self.image = self.stehen_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                self.rect.top = top

        self.mask = pg.mask.from_surface(self.image)

class Platfrom(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.platformen
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.spritesheet2.get_image(0, 288, 380, 94),
                  self.game.spritesheet2.get_image(213, 1662, 201, 100)]
        self.image = choice(images)
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if randrange(100) < POWERUP_SPAWN_PCT:
            Powerup(self.game, self)
        if randrange(100) < COIN_SPAWN_PCT:
            coin(self.game, self)


class Powerup(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = POWERUP_LAYER
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = choice(["boost"])
        self.image = self.game.spritesheet.get_image(1950, 1430, 128, 128)
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 1

    def update(self):
        self.rect.bottom = self.plat.rect.top - 1
        if not self.game.platformen.has(self.plat):
            self.kill()


class Mob(pg.sprite.Sprite):


    def __init__(self, game):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_up = self.game.spritesheet.get_image(3380, 390, 128, 128)
        self.image_up.set_colorkey(Black)
        self.image_down = self.game.spritesheet.get_image(3380, 520, 128, 128)
        self.image_down.set_colorkey(Black)
        self.image = self.image_down
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, WIDTH + 100])
        self.vx = randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y = randrange(HEIGHT / 2)
        self.vy = 0
        self.dy = 0.5


    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        if self.dy < 0:
            self.image = self.image_up
        else:
            self.image = self.image_down
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.center = center
        self.rect.y += self.vy
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()


        
class coin(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = COIN_LAYER
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = choice(["münze"])
        images = [self.game.spritesheet2.get_image(698, 1931, 84, 84),
                  self.game.spritesheet2.get_image(829, 0, 66, 84),self.game.spritesheet2.get_image(897, 1574, 50, 84)]
        self.image = choice(images)
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 3

    def update(self):
        self.rect.bottom = self.plat.rect.top - 3
        if not self.game.platformen.has(self.plat):
            self.kill()