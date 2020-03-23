from Gameplay import Constants, ValidMoveAlgo


class LevelOneOpponent:

    def __init__(self, color):
        # Color is black or white
        self.color = color
        self.validateMoveAlgo = ValidMoveAlgo.ValidMoveAlgo()


    def getMove(self, board):
        legalMoves = set()
        legalMoves = self.validateMoveAlgo.getValidMovesForPlayer(self.color, board)
        pass



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
        return Constants.Constants.LevelOneOpo