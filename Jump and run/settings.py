

Titel = "Doodle jump Rip off"
#settings
WIDTH = 480
HEIGHT = 600
FPS = 60
FONT_NAME = "arial"
HS_FILE = "highscore.txt"
SPRITESHEET = "spritesheet.png"
SPRITESHEET2 = "spritesheet2.png"

#farben
White = (255,255,255)
Black = (0,0,0)
Red = (255,0,0)
Green = (0,255,0)
Blue = (0,0,255)
YELLOW = (255,255,0)
LIGHTBLUE = (0,155,155)
BGCOLOR = Blue


#player
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 25


#game
BOOST_POWER = 60
POWERUP_SPAWN_PCT = 8
MOB_rate = 5000
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POWERUP_LAYER = 1
MOB_LAYER = 2
COIN_LAYER = 1
COIN_SPAWN_PCT = 5


#start platformen
PLATFORMEN_list = [(0, HEIGHT - 50, WIDTH, 40),
                     (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20),
                     (125, HEIGHT - 350, 100, 20), 
                     (350, 200, 100, 20),
                     (175, 100, 50, 20)]