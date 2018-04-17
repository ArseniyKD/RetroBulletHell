# Created by Arseniy Kouzmenkov 1542302 and Patrisha de Boon 1496979

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

# run the game state where the player controls the player character to destroy
# enemies
def GameState(screen):
    exit = False
    quit = False
    # remain in the loop until the player exits the game state, either by
    # quiting the game or returning to the menu.
    while not exit:
        moveFlag = False

        # handle player input
        for event in pygame.event.get():
            # quit the game if they press the x button on the window
            if event.type == pygame.QUIT:
                exit = True
                quit = True
                break

            else:
                if event.type == pygame.KEYDOWN:
                    # enter the pause screen if they press escapse
                    if event.key == pygame.K_ESCAPE:
                        pauseFlag = PauseScreen.pauseSequence()
                        # save the game then resume playing if that is what
                        # the player choses
                        if pauseFlag == 2:
                            SaveFile.saveFile(gameStateVariables.enemyWaves, gameStateVariables.enemy_bullet_list, gameStateVariables.player_bullet_list, gameStateVariables.player, shared.score)
                        # return true to leave the game state and return to the
                        # menu if that is what the player choses
                        elif pauseFlag == 3:
                            return True

                # handle player movement
                moveFlag = PlayerMovement.Move(event, gameStateVariables.player)
                gameStateVariables.player.update()  # update player position

        # this is needed to make the player move smoothely
        if not moveFlag:
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
            # iterate through all enemywaves and update their positions
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

        # fire a player bullet after a set delay
        if pygame.time.get_ticks() - gameStateVariables.prevPlayerFireTime >= shared.playerFireDelay:
            gameStateVariables.prevPlayerFireTime = pygame.time.get_ticks()
            gameStateVariables.player_bullet_list.add(Bullets.Bullet("p1", gameStateVariables.player))

        # fire enemy bullet(s) after a set delay
        if pygame.time.get_ticks() - gameStateVariables.prevEnemyFireTime >= shared.enemyFireDelay:
            gameStateVariables.prevEnemyFireTime = pygame.time.get_ticks()
            # chose a random wave from which to fire bullets
            randomIndex = random.randint(0, len(gameStateVariables.enemyWaves) - 1)
            # set the number of bullets to fire according to the enemy type and
            # the difficluty of the game
            bulletNum = 1
            if gameStateVariables.enemyWaves[randomIndex].Etype == 2:
                bulletNum = int(3*shared.difficulty)
            elif gameStateVariables.enemyWaves[randomIndex].Etype == 3:
                bulletNum = int(6*shared.difficulty)
            # fire bulletNum bullets from each active enemy in the wave at a
            # random angle
            prevAngle = 0
            for j in range(bulletNum):
                for i in gameStateVariables.enemyWaves[randomIndex].activeIndecies:
                    randomAngle = random.randint(-20, 20)
                    if i == 0:
                        if prevAngle - 2 < randomAngle and randomAngle < prevAngle + 2:
                            randomAngle += random.randint(-5, 5)
                    prevAngle = randomAngle
                    gameStateVariables.enemy_bullet_list.add(Bullets.Bullet("e1", gameStateVariables.enemyWaves[randomIndex].IndexEnemyWave(i), randomAngle))

        screen.fill(shared.BLACK) # draw background
        shared.enemy_list.draw(screen) # draw enemyWaves
        gameStateVariables.player_list.draw(screen) # draw player
        # draw bullets
        gameStateVariables.player_bullet_list.draw(screen)
        gameStateVariables.enemy_bullet_list.draw(screen)

        bToRemove = []
        # check for collision between player and enemy bullets, damage the
        # player if necessary and destroy the bullet
        collision = pygame.sprite.spritecollideany(gameStateVariables.player, gameStateVariables.enemy_bullet_list, pygame.sprite.collide_mask)
        if collision is not None:
            flag = gameStateVariables.player.changeHealth(-1, screen, gameStateVariables.player_list)
            if flag:
                exit = True
            collision.setActive(False)

        # iterate through enemy bullets. move them and remove the bullets if
        # there was a collisions
        for b in gameStateVariables.enemy_bullet_list:
            if not b.getActive():
                bToRemove.append(b)
            else:
                b.update()
        for b in bToRemove:
            gameStateVariables.enemy_bullet_list.remove(b)

        # iterate through player bullets, move them and check for collisions
        bToRemove = []
        for b in gameStateVariables.player_bullet_list:
            # iterate through all enemy waves to check for collisions
            for EWave in gameStateVariables.enemyWaves:
                collisionFlag = False
                # if bullet is in range of wave in the y direction
                if b.rect.y <= EWave.getCurrentY() + shared.enemyImgHeight and EWave.getCurrentY() <= b.rect.y:
                    # iterate through all active enemies in the wave
                    for i in EWave.activeIndecies:
                        currEnemy = EWave.IndexEnemyWave(i)
                        # if bullet is in range of enemy, damage the enemy and
                        # set the bullet as no longer active
                        if b.rect.x <= currEnemy.rect.right and currEnemy.rect.left <= b.rect.x:
                            b.setActive(False)
                            EWave.impactEnemyAtX(i, 1)
                            collisionFlag = True
                            break
                # if there has been a collision, check the size of the wave
                # and remove the wave if all enemies have been destroyed
                if collisionFlag:
                    if EWave.getSize() <= 0:
                        gameStateVariables.enemyWaves.remove(EWave)
                        break
            # remove bullets that have collided with enemies, and update the
            # position of the remaining bullets
            if not b.getActive():
                bToRemove.append(b)
            else:
                b.update()
        for b in bToRemove:
            gameStateVariables.player_bullet_list.remove(b)

        # check for collision between the player character and all enemies
        for e in gameStateVariables.enemyWaves:
            playerDeath = False
            # only run further checks if the player's y coordinates are in
            # range of the enemy wave
            if e.getCurrentY() <= gameStateVariables.player.rect.bottom and e.getCurrentY() + e.height >= gameStateVariables.player.rect.top:
                for i in e.activeIndecies:
                    currEnemy = e.IndexEnemyWave(i)
                    # if player is in range of individual enemy, then damage
                    # the player and exit the game state if the player dies
                    if gameStateVariables.player.rect.x <= currEnemy.rect.right and currEnemy.rect.left <= gameStateVariables.player.rect.right:
                        playerDeath = gameStateVariables.player.changeHealth(-1, screen, gameStateVariables.player_list)
                        if playerDeath:
                            exit = True
                        e.impactEnemyAtX(i, 1)
                        break
            if e.getSize() <= 0:
                gameStateVariables.enemyWaves.remove(e)
                break

        pygame.display.flip()  # required to show changes to screen
        shared.clock.tick(shared.fps) # limit fps of game to shared.fps
    # if the player exited the game, quit pygame and sys
    if quit:
        pygame.quit()
        sys.exit()
    return False # show that the player is not returning to the menu
