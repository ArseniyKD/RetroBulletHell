import pygame  # load pygame keywords
import sys     # let python use the file system
import os      # help python identify the OS
import PlayerMovement
import EnemyCreation
import shared

class Bullet(pygame.sprite.Sprite):
    '''
    Create a bullet fired from origin sprite
    '''
    def __init__(self, Type, origin, angle = None):
        self.active = True
        self.angle = angle  # angle from the origin

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images', 'bullet' + Type + '.png')).convert()
        self.image.convert_alpha() # optimise alpha
        self.image.set_alpha(255)
        self.rect  = self.image.get_rect()
        self.rect.y = origin.rect.y
        self.rect.x = origin.rect.x + origin.image.get_width()/2 - self.image.get_width()/2

    def getActive(self):
        return self.active

    def setActive(self, value):
        self.active = value

    def update(self):
        '''
        Update sprite position
        '''

        # update the position of the images and constrain them to the screen
        self.rect.y = self.rect.y - shared.bulletStep

        if self.rect.y < -self.image.get_height():
            self.active = False
