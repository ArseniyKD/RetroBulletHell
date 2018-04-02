import pygame  # load pygame keywords
import sys     # let python use the file system
import os      # help python identify the OS
import Bullets
import PlayerMovement
import shared
import EnemyCreation

# consider using BLACK = (23, 23, 23)
BLACK = (0,0,0)
WHITE = (254,254,254)

playerFireDelay = 250  # number of milliseconds between firing
enemyWaveDelay = 3000 # number of milliseconds between enemyWave generation
enemyMoveDelay = 40  # number of milliseconds between enemy waves moving down
enemyStep = int((shared.enemyImgHeight+2.5*shared.enemyBuffer)*enemyMoveDelay/enemyWaveDelay)

pygame.init()  # initialize module
screen = pygame.display.set_mode((shared.width, shared.height)) # create screen surface on
# which to draw things
screen.fill(BLACK) # draw background
backdropbox = screen.get_rect()

player = PlayerMovement.Player()   # spawn player
# go to starting point
player.rect.x = shared.width/2 - shared.imgWidth/2
player.rect.y = shared.height - shared.height/4 - shared.imgHeight/2

player_list = pygame.sprite.Group()
player_list.add(player)

bullets = []
bullet_list = pygame.sprite.Group()

enemyWaves = []

exit = False
prevFireTime = prevEnemyMoveTime = pygame.time.get_ticks()
prevEnemySpawnTime = pygame.time.get_ticks() - enemyWaveDelay

while not exit:
    flag = False
    for event in pygame.event.get():
        # quit the game if they press the x button on the window
        if event.type == pygame.QUIT:
            exit = True
            break

        # handle player movement
        flag = PlayerMovement.Move(event, player)
        player.update()  # update player position

    if not flag:
        player.update()

    if (pygame.time.get_ticks() - prevEnemySpawnTime) >= enemyWaveDelay and (len(enemyWaves) < 4):
        prevEnemySpawnTime = pygame.time.get_ticks()
        print("spawn an enemy")
        # spawn an enemy wave
        enemyWaves.append(EnemyCreation.EnemyWave(shared.waveSize))
        enemyWaves[-1].CreateEnemyWave()

    if (pygame.time.get_ticks() - prevEnemyMoveTime >= enemyMoveDelay):
        prevEnemyMoveTime = pygame.time.get_ticks()
        #update all enemy waves
        for i in range(len(enemyWaves)):
            enemyWaves[i].update(enemyStep)

    if pygame.time.get_ticks() - prevFireTime >= playerFireDelay:
        prevFireTime = pygame.time.get_ticks()
        bullets.append(Bullets.Bullet("p1", player))
        bullet_list.add(bullets[-1])

    bToRemove = []
    for b in bullets:
        flag = False
        for EWave in enemyWaves:
            # if bullet is in range of wave
            if b.rect.y <= EWave.getCurrentY() + shared.enemyImgHeight and EWave.getCurrentY() <= b.rect.y:
                for i in EWave.activeIndecies:
                    currEnemy = EWave.IndexEnemyWave(i)
                    # if bullet is in range of enemy
                    if b.rect.x <= currEnemy.rect.x + shared.enemyImgHeight and currEnemy.rect.x <= b.rect.x:
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
        bullet_list.remove(b)
        bullets.remove(b)

    screen.fill(BLACK) # draw background
    shared.enemy_list.draw(screen) # draw enemyWaves
    player_list.draw(screen) # draw player
    bullet_list.draw(screen) # draw bullets
    pygame.display.flip()  # required to show changes to screen
    shared.clock.tick(shared.fps) # limit fps of game to shared.fps

pygame.quit()
sys.exit()
