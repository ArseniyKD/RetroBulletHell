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

#BLACK = (23, 23, 23)
BLACK = (0,0,0)
WHITE = (254,254,254)

playerFireDelay = 250  # number of milliseconds between player firing
enemyFireDelay = 1000 # number of milliseconds between enemy firing
enemyWaveDelay = 3000 # number of milliseconds between enemyWave generation
enemyMoveDelay = 40  # number of milliseconds between enemy waves moving down
enemyStep = int((shared.enemyImgHeight+2.5*shared.enemyBuffer)*enemyMoveDelay/enemyWaveDelay)

pygame.init()  # initialize module
screen = pygame.display.set_mode((shared.width, shared.height)) # create screen surface on
# which to draw things
screen.fill(BLACK) # draw background
backdropbox = screen.get_rect()

playerBullets = []
enemyBullets = []
enemyWaves = []
bullet_list = pygame.sprite.Group()
player_list = pygame.sprite.Group()

exit = False
prevPlayerFireTime = prevEnemyMoveTime = prevEnemyFireTime = pygame.time.get_ticks()

load = True

if load:
    try:
        save = SaveFile.loadFile()

        enemyWaves, enemyBullets, playerBullets, player, shared.score = save
        for b in enemyBullets:
            bullet_list.add(b)
        for b in playerBullets:
            bullet_list.add(b)

        player_list.add(player)
        prevEnemySpawnTime = pygame.time.get_ticks()


    except:
        load = False

        # clear anything that may have been edited
        playerBullets = []
        enemyBullets = []
        enemyWaves = []
        shared.enemy_list = pygame.sprite.Group()
        player_bullet_list = pygame.sprite.Group()
        enemy_bullet_list = pygame.sprite.Group()
        player_list = pygame.sprite.Group()
        shared.score = 0


if not load:
    player = PlayerMovement.Player()   # spawn player
    # go to starting point
    player.rect.x = shared.width/2 - shared.imgWidth/2
    player.rect.y = shared.height - shared.height/4 - shared.imgHeight/2
    player_list.add(player)

    prevEnemySpawnTime = pygame.time.get_ticks() - enemyWaveDelay

GameOver = False
drawGameOverSequence = False
Restart = False

while not exit:
    if Restart and not load:
        player.reset()

        # clear anything that may have been edited
        playerBullets = []
        enemyBullets = []
        enemyWaves = []
        shared.enemy_list = pygame.sprite.Group()
        player_bullet_list = pygame.sprite.Group()
        enemy_bullet_list = pygame.sprite.Group()
        shared.score = 0

        prevEnemySpawnTime = pygame.time.get_ticks() - enemyWaveDelay
        prevPlayerFireTime = prevEnemyMoveTime = prevEnemyFireTime = pygame.time.get_ticks()

        shared.playerName = ''
        Restart = False

    flag = False
    for event in pygame.event.get():
        # quit the game if they press the x button on the window
        if event.type == pygame.QUIT:
            exit = True
            break

        if GameOver and not drawGameOverSequence:
            Menu = GameOverScreen.gameOverInput(event)
            if Menu:
                GameOver = False
                load = False
                Restart = True

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    SaveFile.saveFile(enemyWaves, enemyBullets, playerBullets, player, shared.score)

            # handle player movement
            flag = PlayerMovement.Move(event, player)
            player.update()  # update player position

    if GameOver:
        if drawGameOverSequence:
            GameOverScreen.gameOverSequence()
            drawGameOverSequence = False

    else:
        if not flag:
            player.update()

        # Spawn an enemy wave after an enemyWaveDelay, with a max of 4 waves on
        # screen at once
        if (pygame.time.get_ticks() - prevEnemySpawnTime) >= enemyWaveDelay and (len(enemyWaves) < 4):
            prevEnemySpawnTime = pygame.time.get_ticks()
            enemyWaves.append(EnemyCreation.EnemyWave())
            enemyWaves[-1].CreateEnemyWave()

        #update and move all enemy waves
        if (pygame.time.get_ticks() - prevEnemyMoveTime >= enemyMoveDelay):
            prevEnemyMoveTime = pygame.time.get_ticks()
            toRemove = []
            for i in range(len(enemyWaves)):
                enemyWaves[i].move(enemyStep)
                # remove enemies if they move off screen
                if enemyWaves[i].currentY > shared.height :
                    for j in enemyWaves[i].activeIndecies:
                        shared.enemy_list.remove(enemyWaves[i].IndexEnemyWave(j))
                        shared.score -= enemyWaves[i].Etype*100*enemyWaves[i].Size
                    toRemove.append(enemyWaves[i])
            for e in toRemove:
                enemyWaves.remove(e)

        # fire a player bullet
        if pygame.time.get_ticks() - prevPlayerFireTime >= playerFireDelay:
            prevPlayerFireTime = pygame.time.get_ticks()
            playerBullets.append(Bullets.Bullet("p1", player))
            player_bullet_list.add(playerBullets[-1])

        # fire enemy bullet(s)
        if pygame.time.get_ticks() - prevEnemyFireTime >= enemyFireDelay:
            prevEnemyFireTime = pygame.time.get_ticks()
            randomIndex = random.randint(0, len(enemyWaves) - 1)
            for i in enemyWaves[randomIndex].activeIndecies:
                randomAngle = random.randint(-20, 20)
                enemyBullets.append(Bullets.Bullet("e1", enemyWaves[randomIndex].IndexEnemyWave(i), randomAngle))
                enemy_bullet_list.add(enemyBullets[-1])

        screen.fill(BLACK) # draw background
        shared.enemy_list.draw(screen) # draw enemyWaves
        player_list.draw(screen) # draw player
        # draw bullets
        player_bullet_list.draw(screen)
        enemy_bullet_list.draw(screen)

        bToRemove = []
        # check for collision between player and enemy bullets
        collision = pygame.sprite.spritecollideany(player, enemy_bullet_list, pygame.sprite.collide_mask)
        if collision is not None:
            player.image = player.images[3][player.type1]
            player_list.draw(screen) # draw player
            pygame.display.update()
            time.sleep(0.25)
            player.image = player.images[player.type0][player.type1]
            player_list.draw(screen) # draw player
            pygame.display.update()
            time.sleep(0.25)
            player.image = player.images[3][player.type1]
            player_list.draw(screen) # draw player
            pygame.display.update()
            time.sleep(0.25)
            player.image = player.images[player.type0][player.type1]
            player_list.draw(screen) # draw player
            pygame.display.update()

            flag = player.changeHealth(-1)
            if flag:
                GameOver = drawGameOverSequence = True


            collision.setActive(False)


        # iterate through enemy bullets. move them and check for collisions
        for b in enemyBullets:
            '''
            flag = False
            if b.rect.bottom >= player.rect.top and b.rect.top <= player.rect.bottom:
                # if the player is hit
                if b.rect.right >= player.rect.left and b.rect.left <= player.rect.right:
                    b.setActive(False)

                    player.image = player.images[3][player.type1]
                    player_list.draw(screen) # draw player
                    pygame.display.update()
                    time.sleep(0.25)
                    player.image = player.images[player.type0][player.type1]
                    player_list.draw(screen) # draw player
                    pygame.display.update()
                    time.sleep(0.25)
                    player.image = player.images[3][player.type1]
                    player_list.draw(screen) # draw player
                    pygame.display.update()
                    time.sleep(0.25)
                    player.image = player.images[player.type0][player.type1]
                    player_list.draw(screen) # draw player
                    pygame.display.update()

                    flag = player.changeHealth(-1)
                    if flag:
                        GameOver = drawGameOverSequence = True
            '''

            if not b.getActive():
                bToRemove.append(b)
            else:
                b.update()

        for b in bToRemove:
            enemy_bullet_list.remove(b)
            enemyBullets.remove(b)

        # iterate through player bullets. move them and check for collisions
        bToRemove = []
        for b in playerBullets:
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
            playerBullets.remove(b)



    pygame.display.flip()  # required to show changes to screen
    shared.clock.tick(shared.fps) # limit fps of game to shared.fps

pygame.quit()
sys.exit()
