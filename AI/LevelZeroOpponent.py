from Gameplay import Constants

class LevelZeroOpponent:

    def __init__(self, color):
        # Color is black or white
        self.color = color



    def getMove(self, board):
        pass


    def getColor(self):
        return self.color


    def getOpponentType(self):
        return Constants.Constants.LevelZeroOpo