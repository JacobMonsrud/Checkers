from Gameplay import Constants

class LevelZeroOpponent:

    def __init__(self, color):
        # Color is black or white
        self.color = color



    def getMove(self, board):


        return (2, 1, 3, 0)


    # Value = how many enemy pieces has been captured
    def __calcBoardValue(self, board):
        piecesList = list()
        if self.color == Constants.Constants.BlackPlayer:
            piecesList = [(r, c) for (r, c) in board if board[(r, c)].color in {Constants.Constants.WhiteMen, Constants.Constants.WhiteKing}]
        else:
            piecesList = [(r, c) for (r, c) in board if board[(r, c)].color in {Constants.Constants.BlackMen, Constants.Constants.BlackKing}]
        return 12 - len(piecesList)



    def getColor(self):
        return self.color


    def getOpponentType(self):
        return Constants.Constants.LevelZeroOpo