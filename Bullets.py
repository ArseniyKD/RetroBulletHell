# Created by Arseniy Kouzmenkov 1542302 and Patrisha de Boon 1496979

import pygame  # load pygame keywords
import sys     # let python use the file system
import os      # help python identify the OS
import PlayerMovement
import EnemyCreation
import shared
import math

# the get_image function will load in the correct image for the bullets
# only once, and will store the image in a dictionary so that it doesn't have
# to be loaded in pixel by pixel every time a new bullet is spawned. This code
# came from this source https://nerdparadise.com/programming/pygame/part2.
# Note: the current game only uses one type of bullet, so this is not necessary
# with the current implementation, but will improve the efficiency of future
# versions
_image_library = {}
def get_image(path):
        global _image_library
        image = _image_library.get(path)
        if image == None:
                image = pygame.image.load(path).convert_alpha()
                _image_library[path] = image
        return image

# the sprite we used for the bullet are from here:
# https://www.oryxdesignlab.com/products/16-bit-sci-fi-tileset
# if we are to release this game publicly we have to either buy this sprite sheet
# or chose a different sprite since we originally found this image on social media
# but later found that the original author has copyrighted the image
class Bullet(pygame.sprite.Sprite):
    def __init__(self, Type, origin = None, angle = None, x = None, y = None):
        self.type = Type # type of bullet (will later have multiple types)
        self.active = True # set the bullet as active initially
        self.angle = angle  # angle from the verticle

        # get the image for the sprite
        pygame.sprite.Sprite.__init__(self)
        self.image = get_image(os.path.join('images', 'bullet' + self.type + '.png'))
        self.rect  = self.image.get_rect()

        # if we know what object fired the bullet, set coordinates accordingly
        if origin is not None:
            if self.type[0] == 'p':
                self.rect.top = origin.rect.top
            elif self.type[0] == 'e':
                self.rect.bottom = origin.rect.bottom
            self.rect.x = origin.rect.x + origin.image.get_width()/2 - self.image.get_width()/2

        # if specific coordinates have been provided, set them
        if x is not None:
            self.rect.x = x
        if y is not None:
            self.rect.y = y

    # get the current value of self.active
    def getActive(self):
        return self.active

    # set the value of self.active
    def setActive(self, value):
        self.active = value

    # update the sprite position
    def update(self):
        # if the bullet is fired from the player, move it up
        if self.type[0] == 'p':
            # update the position of the images and constrain them to the screen
            self.rect.y -= shared.playerBulletStep

        # if the bullet is fired from an enemy, move it downwards at self.angle
        elif self.type[0] == 'e':
            # find the amount the bullet must move in the x and y direction
            rad = math.radians(self.angle)
            dx = math.sin(rad) * shared.enemyBulletStep
            dy = math.cos(rad) * shared.enemyBulletStep
            # update the position of the images and constrain them to the screen
            self.rect.x += dx
            self.rect.y += dy
        # bounce of the side walls
        if self.rect.left <= 0 or self.rect.right >= shared.width:
            self.angle = -self.angle
        # set the bullets as inactive if they leave the screen
        if self.rect.bottom < 0 or self.rect.top > shared.height:
            self.active = False
