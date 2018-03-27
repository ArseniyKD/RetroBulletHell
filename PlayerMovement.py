import pygame  # load pygame keywords
import sys     # let python use the file system
import os      # help python identify the OS
import shared

xMax = shared.width  # allows us to place further restrictions later
yMax = shared.height  # allows us to place further restrictions later

# the following was created using the help of this tutorial:
# https://opensource.com/article/17/12/game-python-add-a-player
# And the sprites we used came from here:
# https://arboris.deviantart.com/art/Spaceship-sprites-43030167
class Player(pygame.sprite.Sprite):
    '''
    Spawn a player
    '''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0 # move along X
        self.movey = 0 # move along Y
        self.images = []
        for i in range(3):
            self.images.append([])
            for j in range(3):
                img = pygame.image.load(os.path.join('images','player' + str(i) + str(j) + '.png')).convert()
                img.convert_alpha()     # optimise alpha
                self.images[i].append(img)
        self.image = self.images[0][1]
        self.rect  = self.image.get_rect()

    def move(self,x,y):
        '''
        change sprite's location
        '''
        self.movex += x
        self.movey += y

    def constrain(self):
        if self.movex > 0:
            if self.rect.x + shared.imgWidth > shared.width - 5:
                self.rect.x = shared.width - shared.imgWidth - 5
        elif self.movex < 0:
            if self.rect.x < 0 + 5:
                self.rect.x = 0 + 5
        if self.movey > 0:
            if self.rect.y + shared.imgHeight > shared.height - 5:
                self.rect.y = shared.height - shared.imgHeight - 2
        elif self.movey < 0:
            if self.rect.y < 0 + 5:
                self.rect.y = 0 + 5

    def update(self):
        '''
        Update sprite position
        '''
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey

        # moving left only
        if self.movex < 0 and self.movey == 0:
            self.constrain()
            self.image = self.images[1][0]

        # moving right only
        if self.movex > 0 and self.movey == 0:
            self.constrain()
            self.image = self.images[1][2]

        # moving up only
        if self.movex == 0 and self.movey < 0:
            self.constrain()
            self.image = self.images[2][1]

        # moving down only
        if self.movex == 0 and self.movey > 0:
            self.constrain()
            self.image = self.images[0][1]

        # moving left and up
        if self.movex < 0 and self.movey < 0:
            self.constrain()
            self.image = self.images[2][0]

        # moving left and down
        if self.movex < 0 and self.movey > 0:
            self.constrain()
            self.image = self.images[0][0]

        # moving right and up
        if self.movex > 0 and self.movey < 0:
            self.constrain()
            self.image = self.images[2][2]

        # moving right and down
        if self.movex > 0 and self.movey > 0:
            self.constrain()
            self.image = self.images[0][2]

        # returning to center
        if self.movex == 0 and self.movey == 0:
            self.constrain()
            self.image = self.images[1][1]



# pass a pygame event to the function to check if it is a keypress or release
# that affects mmovement.Returns true if the player moves, and false if it did
# not
# This allows for users to use wasd keys for movement
def Move(event, player):
    flag = False
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT or event.key == ord('a'):
            player.move(-shared.step, 0)
            flag = True
        elif event.key == pygame.K_RIGHT or event.key == ord('d'):
            player.move(shared.step, 0)
            flag = True
        if event.key == pygame.K_UP or event.key == ord('w'):
            player.move(0, -shared.step)
            flag = True
        elif event.key == pygame.K_DOWN or event.key == ord('s'):
            player.move(0, shared.step)
            flag = True

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == ord('a'):
            player.move(shared.step, 0)
            flag = True
        elif event.key == pygame.K_RIGHT or event.key == ord('d'):
            player.move(-shared.step, 0)
            flag = True
        if event.key == pygame.K_UP or event.key == ord('w'):
            player.move(0, shared.step)
            flag = True
        elif event.key == pygame.K_DOWN or event.key == ord('s'):
            player.move(0, -shared.step)
            flag = True
    return flag
