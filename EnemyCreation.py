import pygame
import sys     # let python use the file system
import os      # help python identify the OS
from avl_dict import AVLDict as aDict
from random import *
import shared

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
class Enemy(pygame.sprite.Sprite):
    def __init__(self, Etype):
        self.Etype = Etype

        if self.Etype == 0 or self.Etype == 1:
            self.health = 1*shared.difficulty
        elif self.Etype == 2:
            self.health = 4*shared.difficulty
        elif self.Etype == 3:
            self.health = 10*shared.difficulty

        self.reDraw = True

        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.image.load(os.path.join('images','enemy' + str(self.Etype) + '.png')).convert_alpha()
        self.image = get_image(os.path.join('images','enemy' + str(self.Etype) + '.png'))
        self.rect  = self.image.get_rect()


    def Einfo(self):
        if self.Etype == 0:  # "Common"
            return 0
        elif self.Etype == 1:  # "Rare"
            return 1
        elif self.Etype == 2:  # "Epic"
            return 2
        elif self.Etype == 3:  # "Legendary"
            return 3

    def setHealth(self, hp): # TODO: use this : , Etype):
        self.health = hp

    def impact(self, Damage):
        self.health -= Damage
        if self.health <= 0:
            self.reDraw = False
            return True # return trye if the enemy is killed
        else:
            return False # return false if the enemy is not killed

    def getHealth(self):
        return self.health

    def setReDraw(self, flag: bool):
        self.reDraw = flag

    def getReDraw(self):
        return self.reDraw

    def __str__(self):
        return str(self.Etype)


class EnemyWave:
    def __init__(self, Etype = None):
        self.Etype = Etype
        self.Size = None
        self.wave = aDict()
        # self.initialX = int((shared.width-self.Size*(shared.enemyImgWidth+shared.enemyBuffer)+shared.enemyBuffer)/2)
        self.initialX = None
        self.currentY = 0
        self.width = None
        self.height = None
        self.activeIndecies = []

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

    def determineSize(self):
        if self.Etype == 0:
            self.Size = 8
        elif self.Etype == 1:
            self.Size = 4
        elif self.Etype == 2:
            self.Size = 2
        elif self.Etype == 3:
            self.Size = 1

    def setInitialX(self, iX: int):
        self.initialX = iX

    def getInitialX(self):
        return self.initialX

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

    def getSize(self):
        return self.Size

    def CreateEnemyWave(self, initialX = None, currentY = None):
        if self.Etype is None:
            self.randomEtype()

        currEnemyData = Enemy(self.Etype)
        self.determineSize()

        self.width = currEnemyData.rect.width
        self.height = currEnemyData.rect.height
        # self.Size = int(shared.width/(self.width+shared.enemyBuffer))
        if currentY == None:
            self.currentY -= self.height+shared.enemyBuffer
        else:
            self.currentY = currentY
        if initialX is None:
            self.initialX = randint(shared.enemyBuffer, abs(shared.width-self.Size*(self.width+shared.enemyBuffer)))
        else:
            self.initialX = initialX

        for i in range(self.Size):
            if i > 0:
                currEnemyData = Enemy(self.Etype)

            self.activeIndecies.append(i)
            shared.enemy_list.add(currEnemyData)
            currEnemyData.rect.x = self.initialX + i*(self.width + shared.enemyBuffer)
            currEnemyData.rect.y = self.currentY
            self.wave[currEnemyData.rect.x] = currEnemyData

    def IndexEnemyWave(self, index):
        return self.wave[self.initialX + index*(self.width + shared.enemyBuffer)]

    def move(self, step):
        self.currentY += step
        for i in self.activeIndecies:
            self.wave[self.initialX + i*(self.width + shared.enemyBuffer)].rect.y = self.currentY

    def getCurrentY(self):
        return self.currentY

    def setCurrentY(self, Y):
        self.currentY = Y

    def __str__(self):
        output = []
        for i in range(self.Size):
            output.append(str(self.wave[self.wave.ith_key(i)]))

        return " ".join(output)


if __name__ == "__main__":
    a = EnemyWave(8)
    a.CreateEnemyWave()
    print(a)
    print(a.wave.ith_key(1))
    print(a.wave[a.wave.ith_key(1)])
