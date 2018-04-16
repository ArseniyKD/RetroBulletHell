# this is out high score tracking class. It keeps track of all the
# high scores in a very specific format.
class HighScore:
    # the initialiser of the class.
    def __init__(self):
        # the list of scores stores all the scores and the names attached to them.
        self.scores = []
        # this checks whether the file exists, and if it doesn't, creates the file.
        try:
            self.file = open('highScore', 'r+')
        except:
            open('highScore', 'w').close()
            self.file = open('highScore', 'r+')
        # the counter is basically to make sure that no more than 10 scores are ever loaded.
        counter = 0
        for line in self.file:
            temp = line.strip().split()
            # a single score is basically a tuple that stores the score value in the first
            # half and the name associated with the score in the second half.
            self.scores.append((int(temp[0]), temp[1]))
            counter += 1
            if counter > 9:
                break
        self.file.close()
        # initialises the new score to 0
        self.score = 0
        # initialises the new name to an empty string.
        self.name = ""

    # this function adds the score provided by the user to the internal score variable.
    def ScoreKeeping(self, extraScore: int):
        self.score += extraScore

    # resets the current score back to zero.
    def resetScore(self):
        self.score = 0

    # simple score value getter.
    def getScore(self):
        return self.score

    # simple name setter
    def setName(self, nameOfScore):
        self.name = nameOfScore

    # simple name getter.
    def getName(self):
        return self.name

    # returns all the scores upon request.
    def getAllHighScores(self):
        return self.scores

    # this updates the high score file and sorts it in ascending order.
    def updateHighScoresFile(self, newName):
        self.setName(newName)
        self.scores.append((self.score, self.getName()))
        self.file = open('highScore', 'w')
        self.scores = sorted(self.scores, reverse=True)
        for score in self.scores:
            self.file.write(str(score[0]) + " " + str(score[1]) + '\n')
        self.file.close()
        self.resetScore()
