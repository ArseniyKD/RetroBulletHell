import pygame  # load pygame keywords
import sys     # let python use the file system
import os      # help python identify the OS
import PlayerMovement
import EnemyCreation
import shared
import math

class Bullet(pygame.sprite.Sprite):
    '''
    Create a bullet fired from origin sprite
    '''
    def __init__(self, Type, origin, angle = None):
        self.type = Type
        self.active = True
        self.angle = angle  # angle from the origin

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images', 'bullet' + self.type + '.png')).convert_alpha()
        self.rect  = self.image.get_rect()

        if self.type[0] == 'p':
            self.rect.y = origin.rect.top
        elif self.type[0] == 'e':
            self.rect.y = origin.rect.bottom

        self.rect.x = origin.rect.x + origin.image.get_width()/2 - self.image.get_width()/2

    def getActive(self):
        return self.active

    def setActive(self, value):
        self.active = value

    def update(self):
        '''
        Update sprite position
        '''
        # if the bullet is going up
        if self.type[0] == 'p':
            # update the position of the images and constrain them to the screen
            self.rect.y -= shared.playerBulletStep

        # if the bullet is going down
        elif self.type[0] == 'e':
            rad = math.radians(self.angle)
            dx = math.sin(rad) * shared.enemyBulletStep
            dy = math.cos(rad) * shared.enemyBulletStep
            # update the position of the images and constrain them to the screen
            self.rect.x += dx
            self.rect.y += dy

        if self.rect.left <= 0 or self.rect.right >= shared.width:
            self.angle = -self.angle

        if self.rect.bottom < 0 or self.rect.top > shared.height:
            self.active = False
