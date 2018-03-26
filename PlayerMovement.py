import pygame
import Game

step = 1  # step is the number of units the character moves each key press
xMax = width  # allows us to place further restrictions later
yMax = height  # allows us to place further restrictions later

class location:
    def __init__(self, x=0, y=0):
        self.x = y
        self.y = x

# pass a pygame event to the function to check if it is an arrow key press.
# This allows for users to use wasd keys for movement
def CheckMovement(event):
    if event.type == pygame.KEYDOWN:
        flag = False
        output = ""
        if event.key == pygame.K_LEFT or event.key == ord('a'):
            output += "l"
            flag = True
        elif event.key == pygame.K_RIGHT or event.key == ord('d'):
            output += "r"
            flag = True
        if event.key == pygame.K_UP or event.key == ord('w'):
            output += "u"
            flag = True
        elif event.key == pygame.K_DOWN or event.key == ord('s'):
            output += "d"
            flag = True
        if flag:
            return output
    return False

# pass a string of directions and the player's location as a location struct.
# move the player according to the directions in "direction"
def Move(diretion, location):
    for c in direction:
        if c == 'l':
            location.x -= step
        elif c == 'r':
            location.x += step
        if c == 'u':
            location.y += step
        else c == 'd':
            location.y -= step
    return location
