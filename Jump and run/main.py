import pygame as pg
import random
from settings import *
from sprites import *
import os
from os import path 

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(Titel)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()


    def load_data(self):
        # load highscore   
        self.dir = path.dirname(__file__)
        images_dir = path.join(self.dir, 'images')
        with open(path.join(self.dir, HS_FILE), 'r+') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

        sound_dir = path.join(self.dir, 'sounds')
        self.spritesheet = spritesheet(path.join(images_dir, SPRITESHEET))
        self.spritesheet2 = spritesheet(path.join(images_dir, SPRITESHEET2))
        #sounds
        self.sound_dir= path.join(self.dir, 'sounds')
        self.jump_sound = pg.mixer.Sound(path.join(sound_dir, 'jump.mp3'))
        self.boost_sound = pg.mixer.Sound(path.join(sound_dir, 'boost.mp3'))
        self.coin_sound = pg.mixer.Sound(path.join(sound_dir, 'coin.mp3'))
       

    def newgame(self):
        # start a newgame 
        self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platformen = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.player = Player(self)
       
        for plat in PLATFORMEN_list:
             Platfrom(self, *plat)
        self.mob_timer = 0
        pg.mixer.music.load(path.join(self.sound_dir, 'hintergrund.mp3'))
        self.run()

    def run(self):
        # Game Loop
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        #gegner spawnen
        now = pg.time.get_ticks()
        if now - self.mob_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)
        #checken ob player mit mob kollidiert
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask)
        if mob_hits:
            self.playing = False

        #schauen ob spieler eine platform beim fallen berührt
        if self.player.vel.y > 0:

            hits = pg.sprite.spritecollide(self.player, self.platformen, False)
            if hits:
                niedriegste = hits[0]
                for hit in hits:
                    if hit.rect.bottom > niedriegste.rect.bottom:
                        niedriegste = hit
                if self.player.pos.x < niedriegste.rect.right + 10 and \
                     self.player.pos.x > niedriegste.rect.left - 10:
                    if self.player.pos.y < niedriegste.rect.centery: 
                        self.player.pos.y = niedriegste.rect.top 
                        self.player.vel.y = 0
                        self.player.sprung = False

        #checkt ob der spieler oben am bildschirm ist und scrollt
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y), 2)
            for plat in self.platformen:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 1

        #player powerup
        powerup_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for powerup in powerup_hits:
            if powerup.type == 'boost':
                self.boost_sound.play()
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False

        #player coin
        coin_hits = pg.sprite.spritecollide(self.player, self.coins, True)
        for coin in coin_hits:
            self.score += 10
            self.coin_sound.play()
            

        #Gameover
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platformen) == 0:
            self.playing = False

        #spawn neue platformen
        while len(self.platformen) < 5:
            width = random.randrange(40, 120)
            Platfrom(self, random.randrange(0, WIDTH-width),
                    random.randrange(-75, -30),
                     width, 20)

            
                    

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()


    def draw(self):
        # Game Loop - draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, White, WIDTH / 2, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()


    def abwarten(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False
            


    def start_screen(self):
        # game splash/start screen
        
        self.screen.fill(BGCOLOR)
        self.draw_text(Titel, 48, White, WIDTH / 9, HEIGHT / 4)
        self.draw_text("Pfeile-Tasten zum bewegen, Leertaste zum springen", 22, White, WIDTH /13, HEIGHT / 2)
        self.draw_text("Taste zum spielen drücken", 22, White, WIDTH / 4, HEIGHT * 3 / 4)
        self.draw_text("Highscore: " + str(self.highscore), 22, White, WIDTH / 3, 15)
        pg.display.flip()
        self.abwarten()
        

    def go_screen(self):

        # game over/continue
        if not self.running:
            return 
        self.screen.fill(Black)
        self.draw_text("Game Over", 48, Red, WIDTH / 4, HEIGHT / 4)
        self.draw_text("score: "+ str(self.score), 22, YELLOW, WIDTH /3, HEIGHT / 2)
        self.draw_text("Taste für neustart drücken", 22, Red, WIDTH / 4, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("Neuer Highscore!", 22, YELLOW, WIDTH / 3, HEIGHT / 2+ 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("Highscore: " + str(self.highscore), 22, YELLOW, WIDTH / 4, HEIGHT / 2+ 40)

        pg.display.flip()
        self.abwarten()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midleft = (x, y)
        self.screen.blit(text_surface, text_rect)


g = Game()
g.start_screen()
while g.running:
    g.newgame()
    g.go_screen()

pg.quit()
