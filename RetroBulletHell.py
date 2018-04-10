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
import gameStateVariables

pygame.init()  # initialize module
screen = pygame.display.set_mode((shared.width, shared.height)) # create screen surface on
# which to draw things
screen.fill(shared.BLACK) # draw background
backdropbox = screen.get_rect()

gameStateVariables.player_list.add(gameStateVariables.player)

gameStateVariables.prevPlayerFireTime = gameStateVariables.prevEnemyMoveTime = gameStateVariables.prevEnemyFireTime = pygame.time.get_ticks()
gameStateVariables.prevEnemySpawnTime = pygame.time.get_ticks() - shared.enemyWaveDelay

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
        check = GameState(screen)
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
        gameStateVariables.player.reset()

        gameStateVariables.playerBullets = []
        gameStateVariables.enemyBullets = []
        gameStateVariables.enemyWaves = []
        shared.enemy_list = pygame.sprite.Group()
        gameStateVariables.player_bullet_list = pygame.sprite.Group()
        gameStateVariables.enemy_bullet_list = pygame.sprite.Group()
        shared.score = 0

        gameStateVariables.prevEnemySpawnTime = pygame.time.get_ticks() - shared.enemyWaveDelay
        gameStateVariables.prevPlayerFireTime = gameStateVariables.prevEnemyMoveTime = gameStateVariables.prevEnemyFireTime = pygame.time.get_ticks()

        shared.playerName = ''
        Restart = False
        Game = True

    if load:
        screen.fill(shared.BLACK)
        gameStateVariables.player.reset()

        gameStateVariables.playerBullets = []
        gameStateVariables.enemyBullets = []
        gameStateVariables.enemyWaves = []
        shared.enemy_list = pygame.sprite.Group()
        gameStateVariables.player_bullet_list = pygame.sprite.Group()
        gameStateVariables.enemy_bullet_list = pygame.sprite.Group()
        shared.score = 0

        gameStateVariables.prevEnemySpawnTime = pygame.time.get_ticks() - shared.enemyWaveDelay
        gameStateVariables.prevPlayerFireTime = gameStateVariables.prevEnemyMoveTime = gameStateVariables.prevEnemyFireTime = pygame.time.get_ticks()

        shared.playerName = ''
        save = SaveFile.loadFile()
        if save:
            gameStateVariables.enemyWaves, gameStateVariables.enemyBullets, gameStateVariables.playerBullets, gameStateVariables.player, shared.score = save
            for b in gameStateVariables.enemyBullets:
                gameStateVariables.enemy_bullet_list.add(b)
            for b in gameStateVariables.playerBullets:
                gameStateVariables.player_bullet_list.add(b)

            gameStateVariables.prevEnemySpawnTime = pygame.time.get_ticks()
            gameStateVariables.player_list.empty()
            gameStateVariables.player_list.add(gameStateVariables.player)

        # restart if no save file is detected
        else:
            Restart = True
        load = False
        Game = True

    pygame.display.flip()  # required to show changes to screen
    shared.clock.tick(shared.fps) # limit fps of game to shared.fps

pygame.quit()
sys.exit()
