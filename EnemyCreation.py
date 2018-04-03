import pygame
import sys     # let python use the file system
import os      # help python identify the OS
from avl_dict import AVLDict as aDict
from random import *
import shared

class Enemy(pygame.sprite.Sprite):
    def __init__(self, Etype):
        self.Etype = Etype
        self.healthValue = 1
        self.reDraw = True

        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.image.load(os.path.join('images','enemy' + str(Etype) + '.png')).convert()
        self.image = pygame.image.load(os.path.join('images','enemy' + str(self.Etype) + '.png')).convert_alpha()
        self.rect  = self.image.get_rect()


    def Einfo(self):
        if self.Etype == 0:  # "Common"
            return 2
        elif self.Etype == 1:  # "Rare"
            return 3
        elif self.Etype == 2:  # "Epic"
            return 4
        elif self.Etype == 3:  # "Legendary"
            return 5

    def setHealth(self, hp): # TODO: use this : , Etype):
        self.healthValue = hp

    def impact(self, Damage):
        self.healthValue -= Damage
        if self.healthValue <= 0:
            self.reDraw = False
            return True
        else:
            return False

    def getHealth(self):
        return self.healthValue

    def setReDraw(self, flag: bool):
        self.reDraw = flag

    def getReDraw(self):
        return self.reDraw

    def __str__(self):
        return str(self.Etype)


class EnemyWave:
    def __init__(self, Size: int):
        self.Etype = None
        self.Size = Size
        self.wave = aDict()
        # self.initialX = int((shared.width-self.Size*(shared.enemyImgWidth+shared.enemyBuffer)+shared.enemyBuffer)/2)
        self.initialX = None
        self.currentY = None
        self.width = None
        self.height = None
        self.activeIndecies = []

    def randomEtype(self):
        randomValue = randint(0, 1000)
        if randomValue < 800:
            self.Etype = 0  # "Common"
            self.Size = 8
        elif randomValue < 900:
            self.Etype = 1  # "Rare"
            self.Size = 4
        elif randomValue < 975:
            self.Etype = 2  # "Epic"
            self.Size = 2
        else:
            self.Etype = 3 # "Legendary"
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
            return True

    def getSize(self):
        return self.Size

    def CreateEnemyWave(self):
        self.randomEtype()
        currEnemyData = Enemy(self.Etype)

        self.width = currEnemyData.rect.width
        self.height = currEnemyData.rect.height
        # self.Size = int(shared.width/(self.width+shared.enemyBuffer))
        self.currentY = -(self.height+shared.enemyBuffer)
        self.initialX = randint(shared.enemyBuffer, abs(shared.width-self.Size*(self.width+shared.enemyBuffer)))

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
