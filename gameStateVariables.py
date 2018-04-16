import pygame
import PlayerMovement

# this is a file of all the constants and variables that are required to run the
# game state of the FSM.
player = PlayerMovement.Player()
playerBullets = []
enemyBullets = []
enemyWaves = []
enemy_bullet_list = pygame.sprite.Group()
bullet_list  = pygame.sprite.Group()
player_list  = pygame.sprite.Group()
player_bullet_list  = pygame.sprite.Group()
prevPlayerFireTime = 0
prevEnemySpawnTime = 0
prevEnemyMoveTime = 0
prevEnemyFireTime = 0
