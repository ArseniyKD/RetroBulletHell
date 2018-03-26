import pygame
import PlayerMovement

width = 400
height = 300
fps = 5

pygame.init()  # initialize module
screen = pygame.display.set_mode((width, height)) # create screen surface on
# which to draw things

PlayerLocation = location(width/2, yStart/8)

exit = False
while not exit:
    for event in pygame.event.get():
        # quit the game if they press the x button on the window
        if event.type == pygame.QUIT:
            exit = True
            break

        # handle player movement
        Input = CheckMovement(event)
        if Input is not False:
            Move(Input, PlayerLocation)

    pygame.display.flip()  # required to show changes to screen

pygame.quit()
sys.exit()
