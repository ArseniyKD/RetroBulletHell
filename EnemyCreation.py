import pygame
import sys     # let python use the file system
import os      # help python identify the OS
from avl_dict import AVLDict as aDict
from random import *
import shared

class Enemy(pygame.sprite.Sprite):
    def __init__(self, Etype):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.image.load(os.path.join('images','enemy' + str(Etype) + '.png')).convert()
        self.image = pygame.image.load(os.path.join('images','player' + '11' + '.png')).convert()
        self.image.convert_alpha()     # optimise alpha
        self.image.set_alpha(255)
        self.rect  = self.image.get_rect()

        self.Etype = Etype
        self.imageSize = 39
        self.healthValue = 0
        self.reDraw = True

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

    def getHealth(self):
        return self.healthValue

    def setImageSize(self, newSize: int):
        self.imageSize = newSize

    def getImageSize(self):
        return self.imageSize

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
        self.initialX = 1
        self.currentY = -shared.width

    def randomEtype(self):
        randomValue = randint(0, 1000)
        if randomValue < 800:
            self.Etype = 0  # "Common"
        elif randomValue < 900:
            self.Etype = 1  # "Rare"
        elif randomValue < 975:
            self.Etype = 2  # "Epic"
        else:
            self.Etype = 3 # "Legendary"

    def setInitialX(self, iX: int):
        self.initialX = iX

    def getInitialX(self):
        return self.initialX

    def impactEnemyAtX(self, impactX, Damage):
        if not self.wave[impactX].getReDraw():
            return False
        else:
            self.wave[impactX] = self.wave[impactX].impact(Damage)
            if not self.wave[impactX].getReDraw():
                self.Size -= 1
        return True

    def checkSize(self):
        return self.Size

    def CreateEnemyWave(self):
        self.randomEtype()
        currEnemyData = Enemy(self.Etype)
        shared.enemy_list.add(currEnemyData)
        for i in range(self.Size):
            currEnemyData.rect.x = self.initialX + i*(shared.enemyImgWidth + 10)
            currEnemyData.rect.y = self.currentY
            self.wave[currEnemyData.rect.x] = currEnemyData

    def update(self, step):
        self.currentY += step
        for i in range(shared.waveSize):
            self.wave[self.initialX + i*(shared.enemyImgWidth + 10)].rect.y = self.currentY

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
