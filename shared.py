import pygame
import HighScoreTracking

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
score = 0
playerName = ''
difficulty = 1

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (249, 166, 2)
BLUE = (0, 0, 255)
GRAY = (134, 136, 138)
RED = (255, 0, 0)
DARKBLUE = (16,24,115)
