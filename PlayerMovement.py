# Created by Arseniy Kouzmenkov 1542302 and Patrisha de Boon 1496979

import pygame  # load pygame keywords
import sys     # let python use the file system
import os      # help python identify the OS
import shared
import time

xMax = shared.width  # allows us to place further restrictions later
yMax = shared.height  # allows us to place further restrictions later

# the get_image function will load in the correct image for each enemy
# only once, and will store the image in a dictionary so that it doesn't have
# to be loaded in pixel by pixel every time a new bullet is spawned. This code
# came from this source https://nerdparadise.com/programming/pygame/part2.
_image_library = {}
def get_image(path):
        global _image_library
        image = _image_library.get(path)
        if image == None:
            image = pygame.image.load(path).convert_alpha()
            _image_library[path] = image
        return image

# this was adapted from the get_image function and will allow the masks of each
# image to be laoded once and only once even if multiple cases of the player
# class are made
_mask_library = {}
def get_mask(image):
    global _mask_library
    mask = _mask_library.get(image)
    if mask == None:
        mask = pygame.mask.from_surface(image)
        _mask_library[image] = mask
    return mask

# the following was created using the help of this tutorial:
# https://opensource.com/article/17/12/game-python-add-a-player
# And the sprites we used for the player came from here:
# https://arboris.deviantart.com/art/Spaceship-sprites-43030167
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.health = 5 # set initial player health to 5
        self.movex = 0 # move along X
        self.movey = 0 # move along Y
        self.images = []  # dictionary of 39 by 43 images for sprites
        self.masks = [] # dictionary of masks for each image
        self.type0 = 1 # verticle direction of movement. 0 is down, 1 is unchanging, 2 is up
        self.type1 = 1 # horizontal direction of movement. 0 is left, 1 is unchanginer, 2 is right
        # populate the images and masks dictionary
        for i in range(4):
            self.images.append([])
            if i < 3:
                self.masks.append([])
            for j in range(3):
                img = get_image(os.path.join('images','player' + str(i) + str(j) + '.png'))
                self.images[i].append(img)
                if i < 3:
                    mask = get_mask(self.images[i][j])
                    self.masks[i].append(mask)

        # set the current mask and image according and rect
        self.mask = self.masks[self.type0][self.type1]
        self.image = self.images[self.type0][self.type1]
        self.rect  = self.image.get_rect()

    # change the health of the player by change amount
    def changeHealth(self, change, screen, player_list):
        # if the player is damaged, play the damage animation
        if change < 0:
            self.image = self.images[3][self.type1]
            player_list.draw(screen) # draw player
            pygame.display.update()
            time.sleep(0.25)
            self.image = self.images[self.type0][self.type1]
            player_list.draw(screen) # draw player
            pygame.display.update()
            time.sleep(0.25)
            self.image = self.images[3][self.type1]
            player_list.draw(screen) # draw player
            pygame.display.update()
            time.sleep(0.25)
            self.image = self.images[self.type0][self.type1]
            player_list.draw(screen) # draw player
            pygame.display.update()

        # adjust the player's health
        self.health += change
        if self.health > 0:
            return False # if the player is not killed
        else:
            return True # if the player is killed

    # move the player dx spaces horizontally and dy spaces virtically
    def move(self,dx,dy):
        self.movex += dx
        self.movey += dy

    # constrain the player to the screen
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

    # move the player on screen acording to player input
    def update(self):
        # record movex and movey before constraining so the correct images can
        # be used
        Movex = self.movex
        Movey = self.movey

        # update the position of the images and constrain them to the screen
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey
        self.constrain()

        #change player image to match movement input

        # default positions
        i = 1
        j = 1

        # if moving down
        if Movey > 0:
            i = 0
        # if moving up
        elif Movey < 0:
            i = 2

        # if moving left
        if Movex < 0:
            j = 0
        # if moving right
        elif Movex > 0:
            j = 2

        self.type0 = i
        self.type1 = j
        self.constrain()
        self.image = self.images[i][j]
        self.mask = self.masks[self.type0][self.type1]

    # reset player as if a new game has begun
    def reset(self):
        self.health = 5
        self.movex = 0
        self.movey = 0
        self.rect.x = shared.width/2 - shared.imgWidth/2
        self.rect.y = shared.height - shared.height/4 - shared.imgHeight/2
        self.type0 = 1
        self.type1 = 1


# pass a pygame event to the function to check if it is a keypress or release
# that affects mmovement. Returns true if the player moves, and false if it did
# not
# This allows for users to use wasd and arrow keys for movement. Both key
# presses can have an effect at the same time, so pressing 'd' and the left arrow
# key will cancel out and the player will not move, but pressing 'd' and the
# right arrow key will cause the player to move faster
def Move(event, player):
    moveFlag = False
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT or event.key == ord('a'):
            player.move(-shared.step, 0)
            moveFlag = True
        elif event.key == pygame.K_RIGHT or event.key == ord('d'):
            player.move(shared.step, 0)
            moveFlag = True
        if event.key == pygame.K_UP or event.key == ord('w'):
            player.move(0, -shared.step)
            moveFlag = True
        elif event.key == pygame.K_DOWN or event.key == ord('s'):
            player.move(0, shared.step)
            moveFlag = True

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == ord('a'):
            player.move(shared.step, 0)
            moveFlag = True
        elif event.key == pygame.K_RIGHT or event.key == ord('d'):
            player.move(-shared.step, 0)
            moveFlag = True
        if event.key == pygame.K_UP or event.key == ord('w'):
            player.move(0, shared.step)
            moveFlag = True
        elif event.key == pygame.K_DOWN or event.key == ord('s'):
            player.move(0, -shared.step)
            moveFlag = True
    return moveFlag
