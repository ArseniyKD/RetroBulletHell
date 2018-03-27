import pygame  # load pygame keywords
import sys     # let python use the file system
import os      # help python identify the OS
import PlayerMovement
import shared

# consider using BLACK = (23, 23, 23)
BLACK = (0,0,0)
WHITE = (254,254,254)

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

exit = False
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

    screen.fill(BLACK) # draw background
    player_list.draw(screen) # draw player
    pygame.display.flip()  # required to show changes to screen
    shared.clock.tick(shared.fps) # advance internal clock

pygame.quit()
sys.exit()
