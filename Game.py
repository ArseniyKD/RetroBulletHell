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
# import highScoreTracking

pygame.init()  # initialize module
screen = pygame.display.set_mode((shared.width, shared.height)) # create screen surface on
# which to draw things
screen.fill(shared.BLACK) # draw background
backdropbox = screen.get_rect()

player = PlayerMovement.Player()
enemyWaves = []
player_list = pygame.sprite.Group()
player_bullet_list = pygame.sprite.Group()
enemy_bullet_list = pygame.sprite.Group()
player_list.add(player)

prevPlayerFireTime = prevEnemyMoveTime = prevEnemyFireTime = pygame.time.get_ticks()
prevEnemySpawnTime = pygame.time.get_ticks() - shared.enemyWaveDelay

# declare flags to mimic functional state machine
Restart = toHighScores = toMenu = drawGameOverSequence = GameOver = load = Game = False
startSequence = True

exit = False
while not exit:
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
            toHighScore = False
            load = False
        elif menuFlag == 0:
            Restart = False
            toHighScores = True
            load = False
        elif menuFlag == 2:
            Restart = True
            toHighScore = False
            load = True

        if shared.difficulty == 0.5:
            shared.enemyFireDelay = 1500
        elif shared.difficulty == 1:
            shared.enemyFireDelay = 1000
        elif shared.difficulty == 1.5:
            shared.enemyFireDelay = 750

        toMenu = False


    # clear anything that may have been edited
    if Restart:
        screen.fill(shared.BLACK)
        player.reset()

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

    # read a save file
    if load:
        save = SaveFile.loadFile()
        if save:
            enemyWaves, enemy_bullet_list, player_bullet_list, player, shared.score = save

            prevEnemySpawnTime = pygame.time.get_ticks()
            player_list.empty()
            player_list.add(player)

        # restart if no save file is detected
        else:
            Restart = True

        load = False
        Game = True

    if toHighScores:
        screen.fill(shared.BLACK)
        highScoreScreen.sequence()
        toHighScores = False
        toMenu = True

    if GameOver:
        if drawGameOverSequence:
            GameOverScreen.gameOverSequence()
            drawGameOverSequence = False
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True
                    break

                GameOverInput = GameOverScreen.gameOverInput(event)
                if GameOverInput:
                    GameOver = False
                    Game = True
                    load = False
                    Restart = False
                    toHighScores = True
                    screen.fill(shared.BLACK)

    if Game:
        flag = False
        for event in pygame.event.get():
            # quit the game if they press the x button on the window
            if event.type == pygame.QUIT:
                exit = True
                break

            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pauseFlag = PauseScreen.pauseSequence()
                        if pauseFlag == 2:
                            SaveFile.saveFile(enemyWaves, enemy_bullet_list, player_bullet_list, player, shared.score)
                        elif pauseFlag == 3:
                            toMenu = True
                            Game = False

                # handle player movement
                flag = PlayerMovement.Move(event, player)
                player.update()  # update player position

        if not flag:
            player.update()

        # Spawn an enemy wave after an enemyWaveDelay, with a max of 4 waves on
        # screen at once
        if (pygame.time.get_ticks() - prevEnemySpawnTime) >= shared.enemyWaveDelay and (len(enemyWaves) < 4):
            prevEnemySpawnTime = pygame.time.get_ticks()
            enemyWaves.append(EnemyCreation.EnemyWave())
            if len(enemyWaves) > 1:
                if enemyWaves[-2].currentY < -shared.enemyBuffer:
                    enemyWaves[-1].currentY = enemyWaves[-2].currentY
            enemyWaves[-1].CreateEnemyWave()

        # update and move all enemy waves
        if (pygame.time.get_ticks() - prevEnemyMoveTime >= shared.enemyMoveDelay):
            prevEnemyMoveTime = pygame.time.get_ticks()
            toRemove = []
            for i in range(len(enemyWaves)):
                enemyWaves[i].move(shared.enemyStep)
                # remove enemies if they move off screen
                if enemyWaves[i].currentY > shared.height :
                    for j in enemyWaves[i].activeIndecies:
                        shared.enemy_list.remove(enemyWaves[i].IndexEnemyWave(j))
                        shared.score -= int(enemyWaves[i].Etype*100*enemyWaves[i].Size*shared.difficulty)
                    toRemove.append(enemyWaves[i])
            for e in toRemove:
                enemyWaves.remove(e)

        # fire a player bullet
        if pygame.time.get_ticks() - prevPlayerFireTime >= shared.playerFireDelay:
            prevPlayerFireTime = pygame.time.get_ticks()
            player_bullet_list.add(Bullets.Bullet("p1", player))

        # fire enemy bullet(s)
        if pygame.time.get_ticks() - prevEnemyFireTime >= shared.enemyFireDelay:
            prevEnemyFireTime = pygame.time.get_ticks()
            randomIndex = random.randint(0, len(enemyWaves) - 1)
            bulletNum = 1
            if enemyWaves[randomIndex].Etype == 2:
                bulletNum = int(3*shared.difficulty)
            elif enemyWaves[randomIndex].Etype == 3:
                bulletNum = int(6*shared.difficulty)
            prevAngle = 0
            for j in range(bulletNum):
                for i in enemyWaves[randomIndex].activeIndecies:
                    randomAngle = random.randint(-20, 20)
                    if i == 0:
                        if prevAngle - 2 < randomAngle and randomAngle < prevAngle + 2:
                            randomAngle += random.randint(-5, 5)
                    prevAngle = randomAngle
                    enemy_bullet_list.add(Bullets.Bullet("e1", enemyWaves[randomIndex].IndexEnemyWave(i), randomAngle))

        screen.fill(shared.BLACK) # draw background
        shared.enemy_list.draw(screen) # draw enemyWaves
        player_list.draw(screen) # draw player
        # draw bullets
        player_bullet_list.draw(screen)
        enemy_bullet_list.draw(screen)

        bToRemove = []
        # check for collision between player and enemy bullets
        collision = pygame.sprite.spritecollideany(player, enemy_bullet_list, pygame.sprite.collide_mask)
        if collision is not None:
            flag = player.changeHealth(-1, screen, player_list)
            if flag:
                GameOver = drawGameOverSequence = True
                Game = False
            collision.setActive(False)

        # iterate through enemy bullets. move them and check for collisions
        for b in enemy_bullet_list:
            if not b.getActive():
                bToRemove.append(b)
            else:
                b.update()

        for b in bToRemove:
            enemy_bullet_list.remove(b)

        # iterate through player bullets. move them and check for collisions
        bToRemove = []
        for b in player_bullet_list:
            flag = False
            for EWave in enemyWaves:
                # if bullet is in range of wave
                if b.rect.y <= EWave.getCurrentY() + shared.enemyImgHeight and EWave.getCurrentY() <= b.rect.y:
                    for i in EWave.activeIndecies:
                        currEnemy = EWave.IndexEnemyWave(i)
                        # if bullet is in range of enemy
                        if b.rect.x <= currEnemy.rect.right and currEnemy.rect.left <= b.rect.x:
                            b.setActive(False)
                            EWave.impactEnemyAtX(i, 1)
                            flag = True
                            break
                if flag:
                    if EWave.getSize() <= 0:
                        enemyWaves.remove(EWave)
                        break

            if not b.getActive():
                bToRemove.append(b)
            else:
                b.update()

        for b in bToRemove:
            player_bullet_list.remove(b)

        for e in enemyWaves:
            flag = False
            if e.getCurrentY() <= player.rect.bottom and e.getCurrentY() + e.height >= player.rect.top:
                for i in e.activeIndecies:
                    currEnemy = e.IndexEnemyWave(i)
                    # if bullet is in range of enemy
                    if player.rect.x <= currEnemy.rect.right and currEnemy.rect.left <= player.rect.right:
                        flag = player.changeHealth(-1, screen, player_list)
                        if flag:
                            GameOver = drawGameOverSequence = True
                            Game = False
                        e.impactEnemyAtX(i, 1)
                        flag = True
                        break
            if flag:
                if e.getSize() <= 0:
                    enemyWaves.remove(e)
                    break

        pygame.display.flip()  # required to show changes to screen
        shared.clock.tick(shared.fps) # limit fps of game to shared.fps

pygame.quit()
sys.exit()
