# Created by Arseniy Kouzmenkov 1542302 and Patrisha de Boon 1496979

import pygame
import HighScoreTracking

# some specific shared constants for the game
width = 500
height = 700
imgWidth = 39
imgHeight = 43
enemyImgWidth = 39
enemyImgHeight = 43
enemyBuffer = 20
step = 5  # step is the number of pixels the character moves each key press
playerBulletStep = 12
enemyBulletStep = 5
fps = 60
clock = pygame.time.Clock()
bullets = [] # list of bullets
enemy_list = pygame.sprite.Group()
# this keeps track of the current score the name of the player.
score = 0
playerName = ''
# default difficulty being at medium.
difficulty = 2

# this is the list of all the main necessary colours.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (249, 166, 2)
BLUE = (0, 0, 255)
GRAY = (134, 136, 138)
RED = (255, 0, 0)
DARKBLUE = (16,24,115)

playerFireDelay = 250  # number of milliseconds between player firing
enemyFireDelay = 1000 # number of milliseconds between enemy firing
enemyWaveDelay = 2000 # number of milliseconds between enemyWave generation
enemyMoveDelay = 40  # number of milliseconds between enemy waves moving down
# the length in units of how far each enemy moves down the screen per game tick.
enemyStep = int((enemyImgHeight+2.5*enemyBuffer)*enemyMoveDelay/enemyWaveDelay)
