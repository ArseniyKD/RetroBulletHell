import pygame
import PlayerMovement

player = PlayerMovement.Player()
enemyWaves = []
enemy_bullet_list = pygame.sprite.Group()
player_list  = pygame.sprite.Group()
player_bullet_list  = pygame.sprite.Group()
prevPlayerFireTime = 0
prevEnemySpawnTime = 0
prevEnemyMoveTime = 0
prevEnemyFireTime = 0
