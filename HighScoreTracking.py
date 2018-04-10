class HighScore:
    def __init__(self):
        self.scores = []
        try:
            self.file = open('highScore', 'r+')
        except:
            open('highScore', 'w').close()
            self.file = open('highScore', 'r+')
        counter = 0
        for line in self.file:
            temp = line.strip().split()
            self.scores.append((int(temp[0]), temp[1]))
            counter += 1
            if counter > 9:
                break
        self.file.close()
        self.score = 0
        self.name = ""

    def ScoreKeeping(self, extraScore: int):
        self.score += extraScore

    def resetScore(self):
        self.score = 0

    def getScore(self):
        return self.score

    def setName(self, nameOfScore):
        self.name = nameOfScore

    def getName(self):
        return self.name

    def getAllHighScores(self):
        return self.scores

    def updateHighScoresFile(self, newName):
        self.setName(newName)
        self.scores.append((self.score, self.getName()))
        self.file = open('highScore', 'w')
        self.scores = sorted(self.scores, reverse=True)
        for score in self.scores:
            self.file.write(str(score[0]) + " " + str(score[1]) + '\n')
        self.file.close()
        self.resetScore()
