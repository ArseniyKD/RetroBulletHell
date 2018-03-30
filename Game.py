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
enemyWaveDelay = 1000 # number of milliseconds between enemyWave generation
enemyMoveDelay = 700  # number of milliseconds between enemy waves moving down
enemyStep = 1

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

enemies = []

exit = False
prevEnemyTime = prevFireTime = pygame.time.get_ticks()

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

    if pygame.time.get_ticks() - prevEnemyTime >= enemyWaveDelay:
        # spawn an enemy wave
        enemies.append(EnemyCreation.EnemyWave(shared.waveSize))   # spawn an enemy wave
        enemies[-1].CreateEnemyWave()

    if pygame.time.get_ticks() - prevFireTime >= playerFireDelay:
        prevFireTime = pygame.time.get_ticks()
        bullets.append(Bullets.Bullet("p1", player))
        bullet_list.add(bullets[-1])

    #update all enemy waves
    for i in range(len(enemies)):
        enemies[i].update(enemyStep)

    toRemove = []
    for b in bullets:
        if not b.active:
            toRemove.append(b)
        else:
            b.update()

    for b in toRemove:
        bullets.remove(b)

    screen.fill(BLACK) # draw background
    shared.enemy_list.draw(screen) # draw enemies
    player_list.draw(screen) # draw player
    bullet_list.draw(screen) # draw bullets
    pygame.display.flip()  # required to show changes to screen
    shared.clock.tick(shared.fps) # limit fps of game to shared.fps

pygame.quit()
sys.exit()
