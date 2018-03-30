class CollisionDetection:
    def __init__(self, bulletX, bulletY, YtoCheck, XtoCheck, imageSizeX, imageSizeY):
        self.bulletX = bulletX
        self.bulletY = bulletY
        self.YtoCheck = YtoCheck
        self.XtoCheck = XtoCheck
        self.imageSizeX = imageSizeX
        self.imageSizeY = imageSizeY

    def detectCollision(self):
        if self.bulletY <= self.YtoCheck + self.imageSizeY and self.YtoCheck <= self.bulletY:
            if self.bulletX <= self.YtoCheck + self.imageSizeY and self.YtoCheck <= self.bulletY:
                return True
            else:
                return False
        else:
            return False
