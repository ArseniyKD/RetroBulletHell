from avl_dict import AVLDict as aDict
from uuid import uuid4
from random import *

class Enemy:
    def __init__(self, Etype):
        self.Etype = Etype

    def Einfo(self):
        if self.Etype == "Common":
            return 2
        elif self.Etype == "Rare":
            return 3
        elif self.Etype == "Epic":
            return 4
        elif self.Etype == "Legendary":
            return 5

    def __str__(self):
        return str(self.Etype)


class EnemyWave:
    def __init__(self, Size: int):
        self.Etype = None
        self.Size = Size
        self.wave = aDict()

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


    def CreateEnemyWave(self):
        self.randomEtype()
        currEnemyData = Enemy(self.Etype)
        for i in range(self.Size):
            key = str(uuid4())
            self.wave[key[:8]] = currEnemyData

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
