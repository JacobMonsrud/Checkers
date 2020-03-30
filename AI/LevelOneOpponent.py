from Gameplay import Constants, ValidMoveAlgo
import copy
import random

class LevelOneOpponent:

    def __init__(self, color):
        # Color is black or white
        self.color = color
        self.validateMoveAlgo = ValidMoveAlgo.ValidMoveAlgo()


    def getMove(self, board):
        legalMoves = set()
        legalMoves = self.validateMoveAlgo.getValidMovesForPlayer(self.color, board)
        # Get all moves that does not lead to an enemy capture
        # Do the move on the board. Then get valid moves for the other player and check if any capture moves
        noCapMoves = set()
        for moves in legalMoves:
            board2 = copy.deepcopy(board)
            self.__movePieceFromToDeLight(moves[0], moves[1], moves[2], moves[3], board2)
            if self.color == Constants.Constants.BlackPlayer:
                legalMovesForOtherPlayer = self.validateMoveAlgo.getValidMovesForPlayer(Constants.Constants.WhitePlayer, board2)
            else:
                legalMovesForOtherPlayer = self.validateMoveAlgo.getValidMovesForPlayer(Constants.Constants.BlackPlayer, board2)
            # Check if there is a capture move:
            isCapture = False
            for m in legalMovesForOtherPlayer:
                if abs(m[0] - m[2]) == 2:
                    isCapture = True
                    break

            if not isCapture:
                noCapMoves.add(moves)

        if len(noCapMoves) > 0:
            return random.choice(tuple(noCapMoves))
        else:
            return random.choice(tuple(legalMoves))


    def __movePieceFromToDeLight(self, rowFrom, colFrom, rowTo, colTo, board):
        pieceToMove = board[(rowFrom, colFrom)]
        pieceToMove.row = rowTo
        pieceToMove.col = colTo
        if rowTo == 0 and Constants.Constants.BlackMen:
            pieceToMove.color = Constants.Constants.BlackKing
        elif rowTo == 7 and pieceToMove.color == Constants.Constants.WhiteMen:
            pieceToMove.color = Constants.Constants.WhiteKing
        board[(rowTo, colTo)] = pieceToMove
        del board[(rowFrom, colFrom)]

        # Capture move
        if abs(rowFrom - rowTo) == 2:
            rowDel = (max(rowFrom, rowTo) + min(rowFrom, rowTo)) // 2
            colDel = (max(colFrom, colTo) + min(colFrom, colTo)) // 2
            del board[(rowDel, colDel)]


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