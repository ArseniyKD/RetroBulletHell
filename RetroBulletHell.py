import pygame  # load pygame keywords
import sys     # let python use the file system
import os      # help python identify the OS
import Bullets
import PlayerMovement
import shared
import EnemyCreation
import random
import SaveFile
import GameOverScreen
import time
import highScoreScreen
import StartScreen
import MenuScreen
import PauseScreen
from GameState import GameState

pygame.init()  # initialize module
screen = pygame.display.set_mode((shared.width, shared.height)) # create screen surface on
# which to draw things
screen.fill(shared.BLACK) # draw background
backdropbox = screen.get_rect()

player = PlayerMovement.Player()
playerBullets = []
enemyBullets = []
enemyWaves = []
bullet_list = pygame.sprite.Group()
player_list = pygame.sprite.Group()
player_bullet_list = pygame.sprite.Group()
enemy_bullet_list = pygame.sprite.Group()
player_list.add(player)

prevPlayerFireTime = prevEnemyMoveTime = prevEnemyFireTime = pygame.time.get_ticks()
prevEnemySpawnTime = pygame.time.get_ticks() - shared.enemyWaveDelay

Restart = toHighScores = toMenu = drawGameOverSequence = GameOver = load = Game = Quit = False
startSequence = True

while not Quit:
    if startSequence:
        screen.fill(shared.BLACK)
        if StartScreen.StartScreenSequence():
            exit = True
        else:
            toMenu = True
            startSequence = False

    if toMenu:
        screen.fill(shared.BLACK)
        menuFlag = MenuScreen.sequence()
        if menuFlag == 1:
            Restart = True
        elif menuFlag == 0:
            toHighScores = True
        elif menuFlag == 2:
            load = True
        toMenu = False

    if Game:
        check = GameState(screen, player, playerBullets, enemyBullets, enemyWaves, enemy_bullet_list, bullet_list, player_list, player_bullet_list, prevPlayerFireTime, prevEnemySpawnTime, prevEnemyMoveTime, prevEnemyFireTime)
        if check:
            Game = False
            toMenu = True
        else:
            Game = False
            GameOver = True

    if GameOver:
        GameOverScreen.sequence()
        GameOver = False
        toHighScores = True

    if toHighScores:
        screen.fill(shared.BLACK)
        highScoreScreen.sequence()
        toHighScores = False
        toMenu = True

    if Restart:
        screen.fill(shared.BLACK)
        player.reset()

        playerBullets = []
        enemyBullets = []
        enemyWaves = []
        shared.enemy_list = pygame.sprite.Group()
        player_bullet_list = pygame.sprite.Group()
        enemy_bullet_list = pygame.sprite.Group()
        shared.score = 0

        prevEnemySpawnTime = pygame.time.get_ticks() - shared.enemyWaveDelay
        prevPlayerFireTime = prevEnemyMoveTime = prevEnemyFireTime = pygame.time.get_ticks()

        shared.playerName = ''
        Restart = False
        Game = True

    if load:
        screen.fill(shared.BLACK)
        player.reset()

        playerBullets = []
        enemyBullets = []
        enemyWaves = []
        shared.enemy_list = pygame.sprite.Group()
        player_bullet_list = pygame.sprite.Group()
        enemy_bullet_list = pygame.sprite.Group()
        shared.score = 0

        prevEnemySpawnTime = pygame.time.get_ticks() - shared.enemyWaveDelay
        prevPlayerFireTime = prevEnemyMoveTime = prevEnemyFireTime = pygame.time.get_ticks()

        shared.playerName = ''
        save = SaveFile.loadFile()
        if save:
            enemyWaves, enemyBullets, playerBullets, player, shared.score = save
            for b in enemyBullets:
                enemy_bullet_list.add(b)
            for b in playerBullets:
                player_bullet_list.add(b)

            prevEnemySpawnTime = pygame.time.get_ticks()
            player_list.empty()
            player_list.add(player)

        # restart if no save file is detected
        else:
            Restart = True
        load = False
        Game = True

    pygame.display.flip()  # required to show changes to screen
    shared.clock.tick(shared.fps) # limit fps of game to shared.fps

pygame.quit()
sys.exit()
