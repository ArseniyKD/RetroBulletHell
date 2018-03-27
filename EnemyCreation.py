from avl_dict import AVLDict as aDict
from random import *

class Enemy:
    def __init__(self, Etype):
        self.Etype = Etype
        self.imageSize = 24
        self.healthValue = 0
        self.reDraw = True

    def Einfo(self):
        if self.Etype == "Common":
            return 2
        elif self.Etype == "Rare":
            return 3
        elif self.Etype == "Epic":
            return 4
        elif self.Etype == "Legendary":
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
        self.initialX = 0

    def randomEtype(self):
        randomValue = randint(0, 1000)
        if randomValue < 800:
            self.Etype = "Common"
        elif randomValue < 900:
            self.Etype = "Rare"
        elif randomValue < 975:
            self.Etype = "Epic"
        else:
            self.Etype = "Legendary"

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
        for i in range(self.Size):
            self.wave[self.initialX + i*currEnemyData.imageSize] = currEnemyData

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
