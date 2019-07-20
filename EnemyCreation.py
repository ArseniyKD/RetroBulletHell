import pygame
import sys     # let python use the file system
import os      # help python identify the OS
from random import *
import shared

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

# the sprites we used for the enemies came from here:
# https://opengameart.org/content/retro-spaceships
# this is the enemy class which stores the data of only one enemy.
class Enemy(pygame.sprite.Sprite):
    # this is the initialiser which will set the health values that differ
    # for each enemy type and also depends on the difficulty level.
    def __init__(self, Etype):
        self.Etype = Etype

        if self.Etype == 0 or self.Etype == 1:
            self.health = int(0.5*shared.difficulty + 0.5)
        elif self.Etype == 2:
            self.health = 2*shared.difficulty
        elif self.Etype == 3:
            self.health = 5*shared.difficulty

        self.reDraw = True

        pygame.sprite.Sprite.__init__(self)
        self.image = get_image(os.path.join('images','enemy' + str(self.Etype) + '.png'))
        self.rect  = self.image.get_rect()

    # returns the required information for the current enemy type.
    def Einfo(self):
        if self.Etype == 0:  # "Common"
            return 0
        elif self.Etype == 1:  # "Rare"
            return 1
        elif self.Etype == 2:  # "Epic"
            return 2
        elif self.Etype == 3:  # "Legendary"
            return 3

    # a health setter
    def setHealth(self, hp):
        self.health = hp

    # this is will deal damage to the enemy, reducing their health by the damage.
    def impact(self, Damage):
        self.health -= Damage
        if self.health <= 0:
            self.reDraw = False
            return True # return trye if the enemy is killed
        else:
            return False # return false if the enemy is not killed

    # a health getter.
    def getHealth(self):
        return self.health

    # redraw is used to check if the enemy needs to be redrawn. This is a basic setter.
    def setReDraw(self, flag: bool):
        self.reDraw = flag

    # this is a simple getter for redraw.
    def getReDraw(self):
        return self.reDraw

    # this is a to string method for this class.
    def __str__(self):
        return str(self.Etype)

# this class is a collection of enemies in one wave.
class EnemyWave:
    # this is the initialiser for this class.
    # the wave variable is an avl tree dictionary developed as an assignment in class.
    def __init__(self, Etype = None):
        self.Etype = Etype
        self.Size = None
        self.wave = {}
        self.initialX = None
        self.currentY = 0
        self.width = None
        self.height = None
        self.activeIndecies = []

    # this is our randomiser for what type of enemy this wave will have.
    def randomEtype(self):
        randomValue = randint(0, 1000)
        if randomValue < 500:
            self.Etype = 0  # "Common"
        elif randomValue < 700:
            self.Etype = 1  # "Rare"
        elif randomValue < 950:
            self.Etype = 2  # "Epic"
        else:
            self.Etype = 3 # "Legendary"

    # this determines the wave size depending on the enemy type.
    def determineSize(self):
        if self.Etype == 0:
            self.Size = 8
        elif self.Etype == 1:
            self.Size = 4
        elif self.Etype == 2:
            self.Size = 2
        elif self.Etype == 3:
            self.Size = 1

    # this sets the initial x value at which the first enemy in the wave will be drawn at.
    def setInitialX(self, iX: int):
        self.initialX = iX

    # this gets the initial x value.
    def getInitialX(self):
        return self.initialX

    # this method impact the enemy at a specific x value.
    def impactEnemyAtX(self, index, Damage):
        impactX = self.initialX + index*(self.width + shared.enemyBuffer)

        if not self.wave[impactX].getReDraw():
            return False
        else:
            if self.wave[impactX].impact(Damage):
                self.activeIndecies.remove(index)
                self.Size -= 1
                shared.enemy_list.remove(self.wave[impactX])
                shared.score += int(self.Etype*100*shared.difficulty)
            return True

    # a size getter.
    def getSize(self):
        return self.Size

    # this function actually creates the enemy wave itself.
    def CreateEnemyWave(self, initialX = None, currentY = None):
        # gets the random enemy type.
        if self.Etype is None:
            self.randomEtype()

        # gets the enemy date and determines the wave size from the enemy data.
        currEnemyData = Enemy(self.Etype)
        self.determineSize()

        # image width and height of each enemy
        self.width = currEnemyData.rect.width
        self.height = currEnemyData.rect.height
        # creates the enemy wave off the screen or at a certain location on the screen.
        if currentY == None:
            self.currentY -= self.height+shared.enemyBuffer
        else:
            self.currentY = currentY
        # will create the enmy wave at a specific location on the screen or a predetermined one instead.
        if initialX is None:
            self.initialX = randint(shared.enemyBuffer, abs(shared.width-self.Size*(self.width+shared.enemyBuffer)))
        else:
            self.initialX = initialX

        # this will finally create the wave itself.
        for i in range(self.Size):
            if i > 0:
                currEnemyData = Enemy(self.Etype)

            self.activeIndecies.append(i)
            shared.enemy_list.add(currEnemyData)
            currEnemyData.rect.x = self.initialX + i*(self.width + shared.enemyBuffer)
            currEnemyData.rect.y = self.currentY
            self.wave[currEnemyData.rect.x] = currEnemyData

    # this will return the enmy information at a certain index in the wave.
    def IndexEnemyWave(self, index):
        return self.wave[self.initialX + index*(self.width + shared.enemyBuffer)]

    # this will move the entire wave down by the value of step. only enemies that get re drawn
    # will move.
    def move(self, step):
        self.currentY += step
        for i in self.activeIndecies:
            self.wave[self.initialX + i*(self.width + shared.enemyBuffer)].rect.y = self.currentY

    # y coordinate getter
    def getCurrentY(self):
        return self.currentY

    # y coordinate setter
    def setCurrentY(self, Y):
        self.currentY = Y

    # this is the to string method for the class.
    def __str__(self):
        output = []
        for i in range(self.Size):
            output.append(str(self.wave[self.wave.ith_key(i)]))

        return " ".join(output)
