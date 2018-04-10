import pygame  # load pygame keywords
import sys     # let python use the file system
import os      # help python identify the OS
import Bullets
import PlayerMovement
import shared
import random
import time
import PauseScreen
import EnemyCreation
import SaveFile
import gameStateVariables

def GameState(screen):
    exit = False
    quit = False
    while not exit:
        flag = False
        for event in pygame.event.get():
            # quit the game if they press the x button on the window
            if event.type == pygame.QUIT:
                exit = True
                quit = True
                break

            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pauseFlag = PauseScreen.pauseSequence()
                        if pauseFlag == 2:
                            SaveFile.saveFile(gameStateVariables.enemyWaves, gameStateVariables.enemyBullets, gameStateVariables.playerBullets, gameStateVariables.player, shared.score)
                        elif pauseFlag == 3:
                            return True

                # handle player movement
                flag = PlayerMovement.Move(event, gameStateVariables.player)
                gameStateVariables.player.update()  # update player position

        if not flag:
            gameStateVariables.player.update()

        # Spawn an enemy wave after an enemyWaveDelay, with a max of 4 waves on
        # screen at once
        if (pygame.time.get_ticks() - gameStateVariables.prevEnemySpawnTime) >= shared.enemyWaveDelay and (len(gameStateVariables.enemyWaves) < 4):
            gameStateVariables.prevEnemySpawnTime = pygame.time.get_ticks()
            gameStateVariables.enemyWaves.append(EnemyCreation.EnemyWave())
            if len(gameStateVariables.enemyWaves) > 1:
                if gameStateVariables.enemyWaves[-2].currentY < -shared.enemyBuffer:
                    gameStateVariables.enemyWaves[-1].currentY = gameStateVariables.enemyWaves[-2].currentY
            gameStateVariables.enemyWaves[-1].CreateEnemyWave()

        # update and move all enemy waves
        if (pygame.time.get_ticks() - gameStateVariables.prevEnemyMoveTime >= shared.enemyMoveDelay):
            gameStateVariables.prevEnemyMoveTime = pygame.time.get_ticks()
            toRemove = []
            for i in range(len(gameStateVariables.enemyWaves)):
                gameStateVariables.enemyWaves[i].move(shared.enemyStep)
                # remove enemies if they move off screen
                if gameStateVariables.enemyWaves[i].currentY > shared.height :
                    for j in gameStateVariables.enemyWaves[i].activeIndecies:
                        shared.enemy_list.remove(gameStateVariables.enemyWaves[i].IndexEnemyWave(j))
                        shared.score -= int(gameStateVariables.enemyWaves[i].Etype*100*gameStateVariables.enemyWaves[i].Size*shared.difficulty)
                    toRemove.append(gameStateVariables.enemyWaves[i])
            for e in toRemove:
                gameStateVariables.enemyWaves.remove(e)

        # fire a player bullet
        if pygame.time.get_ticks() - gameStateVariables.prevPlayerFireTime >= shared.playerFireDelay:
            gameStateVariables.prevPlayerFireTime = pygame.time.get_ticks()
            gameStateVariables.playerBullets.append(Bullets.Bullet("p1", gameStateVariables.player))
            gameStateVariables.player_bullet_list.add(gameStateVariables.playerBullets[-1])

        # fire enemy bullet(s)
        if pygame.time.get_ticks() - gameStateVariables.prevEnemyFireTime >= shared.enemyFireDelay:
            gameStateVariables.prevEnemyFireTime = pygame.time.get_ticks()
            randomIndex = random.randint(0, len(gameStateVariables.enemyWaves) - 1)
            bulletNum = 1
            if gameStateVariables.enemyWaves[randomIndex].Etype == 2:
                bulletNum = int(3*shared.difficulty)
            elif gameStateVariables.enemyWaves[randomIndex].Etype == 3:
                bulletNum = int(6*shared.difficulty)
            prevAngle = 0
            for j in range(bulletNum):
                for i in gameStateVariables.enemyWaves[randomIndex].activeIndecies:
                    randomAngle = random.randint(-20, 20)
                    if i == 0:
                        if prevAngle - 2 < randomAngle and randomAngle < prevAngle + 2:
                            randomAngle += random.randint(-5, 5)
                    prevAngle = randomAngle
                    gameStateVariables.enemyBullets.append(Bullets.Bullet("e1", gameStateVariables.enemyWaves[randomIndex].IndexEnemyWave(i), randomAngle))
                    gameStateVariables.enemy_bullet_list.add(gameStateVariables.enemyBullets[-1])

        screen.fill(shared.BLACK) # draw background
        shared.enemy_list.draw(screen) # draw enemyWaves
        gameStateVariables.player_list.draw(screen) # draw player
        # draw bullets
        gameStateVariables.player_bullet_list.draw(screen)
        gameStateVariables.enemy_bullet_list.draw(screen)

        bToRemove = []
        # check for collision between player and enemy bullets
        collision = pygame.sprite.spritecollideany(gameStateVariables.player, gameStateVariables.enemy_bullet_list, pygame.sprite.collide_mask)
        if collision is not None:
            flag = gameStateVariables.player.changeHealth(-1, screen, gameStateVariables.player_list)
            if flag:
                exit = True
            collision.setActive(False)

        # iterate through enemy bullets. move them and check for collisions
        for b in gameStateVariables.enemyBullets:
            if not b.getActive():
                bToRemove.append(b)
            else:
                b.update()

        for b in bToRemove:
            gameStateVariables.enemy_bullet_list.remove(b)
            gameStateVariables.enemyBullets.remove(b)

        # iterate through player bullets. move them and check for collisions
        bToRemove = []
        for b in gameStateVariables.playerBullets:
            flag = False
            for EWave in gameStateVariables.enemyWaves:
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
                        gameStateVariables.enemyWaves.remove(EWave)
                        break

            if not b.getActive():
                bToRemove.append(b)
            else:
                b.update()

        for b in bToRemove:
            gameStateVariables.player_bullet_list.remove(b)
            gameStateVariables.playerBullets.remove(b)

        for e in gameStateVariables.enemyWaves:
            flag = False
            if e.getCurrentY() <= gameStateVariables.player.rect.bottom and e.getCurrentY() + e.height >= gameStateVariables.player.rect.top:
                for i in e.activeIndecies:
                    currEnemy = e.IndexEnemyWave(i)
                    # if bullet is in range of enemy
                    if gameStateVariables.player.rect.x <= currEnemy.rect.right and currEnemy.rect.left <= gameStateVariables.player.rect.right:
                        flag = gameStateVariables.player.changeHealth(-1, screen, gameStateVariables.player_list)
                        if flag:
                            exit = True
                        e.impactEnemyAtX(i, 1)
                        flag = True
                        break
            if flag:
                if e.getSize() <= 0:
                    gameStateVariables.enemyWaves.remove(e)
                    break

        pygame.display.flip()  # required to show changes to screen
        shared.clock.tick(shared.fps) # limit fps of game to shared.fps
    if quit:
        pygame.quit()
        sys.exit()
    return False
