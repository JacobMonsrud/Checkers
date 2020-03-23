from Gameplay import Constants

class PvpOpponent:

    def __init__(self, color):
        # Color is black or white
        self.color = color


    def getMove(self, board):
        return (-1, -1, -1, -1)


    def getColor(self):
        return self.color


    def getOpponentType(self):
        return Constants.Constants.PvpOpo