from Gameplay import Constants, ValidMoveAlgo
import random, copy, sys

# Classic Minimax. No algorithm optimization.
class LevelTwoOpponent:

    def __init__(self, color):
        # Color is black or white
        self.color = color
        self.validateMoveAlgo = ValidMoveAlgo.ValidMoveAlgo()


    def getMove(self, board):
        max = self.__minimax(board, 4, self.color, self.color)
        print(str(max))
        legalMoves = set()

        childBoards = self.__getChildBoards(board, self.color)
        boardKeys = set(board.keys())
        for child in childBoards:
            if self.__calcBoardValue(child, self.color) == max:
                boardKeys = set(board.keys())
                childKeys = set(child.keys())
                # Logic not correct
                (rowFrom, colFrom) = list(boardKeys - childKeys)[0]
                (rowTo, colTo) = list(childKeys - boardKeys)[0]
                legalMoves.add((rowFrom, colFrom, rowTo, colTo))

        return random.choice(tuple(legalMoves))


    def __minimax(self, board, depth, maximizingPlayerDynamic, maximizingPlayer):
        if depth == 0 or self.__isGameOver(board):
            return (self.__calcBoardValue(board, maximizingPlayer))

        if maximizingPlayerDynamic == maximizingPlayer:
            maxValue = -10000000
            (maxRowFrom, maxColFrom, maxRowTo, maxColTo) = (0, 0, 0, 0)
            childBoards = self.__getChildBoards(board, maximizingPlayerDynamic)
            for child in childBoards:
                newMaximizingPlayer = self.__getNewMaximizingPlayer(maximizingPlayerDynamic)
                value = self.__minimax(child, depth - 1, newMaximizingPlayer, maximizingPlayer)
                maxValue = max(maxValue, value[0])
            return maxValue
        else:
            minValue = 10000000
            childBoards = self.__getChildBoards(board, maximizingPlayerDynamic)
            for child in childBoards:
                newMaximizingPlayer = self.__getNewMaximizingPlayer(maximizingPlayerDynamic)
                value = self.__minimax(child, depth - 1, newMaximizingPlayer, maximizingPlayer)
                minValue = min(minValue, value)
            return minValue


    def __calcBoardValue(self, board, maximizingPlayer):
        whiteValue = 0
        blackValue = 0
        for (r, c) in board:
            if board[(r, c)].color == Constants.Constants.WhiteMen:
                whiteValue += 1
            elif board[(r, c)].color == Constants.Constants.WhiteKing:
                whiteValue += 2
            elif board[(r, c)].color == Constants.Constants.BlackMen:
                blackValue += 1
            elif board[(r, c)].color == Constants.Constants.BlackKing:
                blackValue += 2
        if maximizingPlayer == Constants.Constants.WhitePlayer:
            return whiteValue - blackValue
        else:
            return blackValue - whiteValue


    def __getNewMaximizingPlayer(self, player):
        if player == Constants.Constants.WhitePlayer:
            return Constants.Constants.BlackPlayer
        else:
            return Constants.Constants.WhitePlayer

    # All sequences of multiple captures count as one move.
    def __getChildBoards(self, board, playerColor):
        childBoards = list()
        validMoves = self.validateMoveAlgo.getValidMovesForPlayer(playerColor, board)
        for moves in validMoves:
            # capture move
            if abs(moves[0] - moves[2]) == 2:
                boardCaptureCopy = copy.deepcopy(board)
                self.__movePieceFromToDeLight(moves[0], moves[1], moves[2], moves[3], boardCaptureCopy)

                culmSetOfBoards = list()
                self.__captureMovesHelper(culmSetOfBoards, moves[2], moves[3], boardCaptureCopy)
                for b in culmSetOfBoards:
                    childBoards.append(b) # Måske give movet med her?

            else:
                boardCopy = copy.deepcopy(board)
                self.__movePieceFromToDeLight(moves[0], moves[1], moves[2], moves[3], boardCopy)
                childBoards.append(boardCopy)

        return childBoards


    def __captureMovesHelper(self, setOfBoards, row, col, board):
        moves = self.__getCaptureMovesFromPos(row, col, board)
        if len(moves) == 0:
            setOfBoards.append(board)
        else:
            for move in moves:
                (rf, cf , rt, ct) = move
                boardCopy = copy.deepcopy(board)
                self.__movePieceFromToDeLight(rf, cf, rt, ct, boardCopy)
                self.__captureMovesHelper(setOfBoards, rt, ct, boardCopy)


    def __getCaptureMovesFromPos(self, row, col, board):
        legalMoves = set()

        for move in {(row - 2, col - 2), (row - 2, col + 2), (row + 2, col - 2), (row + 2, col + 2)}:
            if self.validateMoveAlgo.isValidMoveCalc(row, col, move[0], move[1], board):
                legalMoves.add((row, col, move[0], move[1]))

        return legalMoves


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


    def __isGameOver(self, board):
        return False


    def getColor(self):
        return self.color


    def getOpponentType(self):
        return Constants.Constants.LevelTwoOpo