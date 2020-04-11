from Gameplay import Constants, ValidMoveAlgo
import random, copy, sys

# Classic Minimax. No algorithm optimization.
class LevelTwoOpponent:

    def __init__(self, color):
        # Color is black or white
        self.color = color
        self.validateMoveAlgo = ValidMoveAlgo.ValidMoveAlgo()
        self.toDoMoves = list()


    def getMove(self, board):
        if len(self.toDoMoves) == 0:
            l = list()
            l.append(board)
            #print("start board: " + str(l[0]))
            max = self.__minimax(l, 3, self.color, self.color)
            print("max[0]: " + str(max[0]))
            print("max[1][1:]: " + str(max[1][1:]))

            lastMove = (0, 0, 0, 0)
            for move in max[1][1:]:
                print("move: " + str(move))
                if lastMove == (0, 0, 0, 0):
                    lastMove = move
                else:
                    if (lastMove[2], lastMove[3]) == (move[0], move[1]):
                        print("double jump:" + str(lastMove[2]) + str(lastMove[3]) + " to " + str(move[0]) + str(move[1]))
                        self.toDoMoves.append(move)
                        lastMove = move

            return max[1][1]
        else:
            print("todo: " + str(self.toDoMoves[0]))
            return self.toDoMoves.pop(0)


    def __minimax(self, board, depth, maximizingPlayerDynamic, maximizingPlayer):
        if depth == 0 or self.__isGameOver(board):
            #print("depth = 0")
            return (self.__calcBoardValue(board, maximizingPlayer), board)

        if maximizingPlayerDynamic == maximizingPlayer:
            maxValue = -10000000
            maxBoard = list()
            childBoards = self.__getChildBoards(board, maximizingPlayerDynamic)
            for child in childBoards:
                newMaximizingPlayer = self.__getNewMaximizingPlayer(maximizingPlayerDynamic)
                value = self.__minimax(child, depth - 1, newMaximizingPlayer, maximizingPlayer)
                maxValue = max(maxValue, value[0])
                if maxValue == value[0]:
                    maxBoard = value[1]

            return (maxValue, maxBoard)
        else:
            minValue = 10000000
            minBoard = list()
            childBoards = self.__getChildBoards(board, maximizingPlayerDynamic)
            for child in childBoards:
                newMaximizingPlayer = self.__getNewMaximizingPlayer(maximizingPlayerDynamic)
                value = self.__minimax(child, depth - 1, newMaximizingPlayer, maximizingPlayer)
                minValue = min(minValue, value[0])
                if minValue == value[0]:
                    minBoard = value[1]
            return (minValue, minBoard)


    def __calcBoardValue(self, board, maximizingPlayer):
        whiteValue = 0
        blackValue = 0
        #print("calc: " + str(board[1]))
        #print("calc board[0] : " + str(board[0]))
        #print("calc board : " + str(board))
        for (r, c) in board[0]:
            if board[0][(r, c)].color == Constants.Constants.WhiteMen:
                whiteValue += 1
            elif board[0][(r, c)].color == Constants.Constants.WhiteKing:
                whiteValue += 2
            elif board[0][(r, c)].color == Constants.Constants.BlackMen:
                blackValue += 1
            elif board[0][(r, c)].color == Constants.Constants.BlackKing:
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
    # ChildBoards is a list af list (the board at [0] and the moves to get to that board at [1:])
    def __getChildBoards(self, board, playerColor):
        childBoards = list()
        validMoves = self.validateMoveAlgo.getValidMovesForPlayer(playerColor, board[0])
        for moves in validMoves:
            # capture move
            if abs(moves[0] - moves[2]) == 2:
                boardCaptureCopy = copy.deepcopy(board)
                self.__movePieceFromToDeLight(moves[0], moves[1], moves[2], moves[3], boardCaptureCopy)

                culmSetOfBoards = list()
                madeMoves = list()
                madeMoves.append(moves)
                self.__captureMovesHelper(culmSetOfBoards, madeMoves, boardCaptureCopy)
                for b in culmSetOfBoards:
                    childBoards.append(b)

            else:
                boardCopy = copy.deepcopy(board)
                self.__movePieceFromToDeLight(moves[0], moves[1], moves[2], moves[3], boardCopy)
                boardCopy.append(moves)
                #print("valid moves: " + str(boardCopy[1]))
                childBoards.append(boardCopy)

        return childBoards


    def __captureMovesHelper(self, culmSetOfBoards, madeMoves, board):
        lastMove = madeMoves[-1]
        moves = self.__getCaptureMovesFromPos(lastMove[2], lastMove[3], board)
        if len(moves) == 0:
            for m in madeMoves:
                board.append(m)
            culmSetOfBoards.append(board)
        else:
            for move in moves:
                (rf, cf , rt, ct) = move
                boardCopy = copy.deepcopy(board)
                self.__movePieceFromToDeLight(rf, cf, rt, ct, boardCopy)
                madeMovesCopy = copy.deepcopy(madeMoves)
                madeMovesCopy.append(move)
                self.__captureMovesHelper(culmSetOfBoards, madeMovesCopy, boardCopy)


    def __getCaptureMovesFromPos(self, row, col, board):
        legalMoves = set()

        for move in {(row - 2, col - 2), (row - 2, col + 2), (row + 2, col - 2), (row + 2, col + 2)}:
            if self.validateMoveAlgo.isValidMoveCalc(row, col, move[0], move[1], board[0]):
                legalMoves.add((row, col, move[0], move[1]))

        return legalMoves


    def __movePieceFromToDeLight(self, rowFrom, colFrom, rowTo, colTo, board):
        pieceToMove = board[0][(rowFrom, colFrom)]
        pieceToMove.row = rowTo
        pieceToMove.col = colTo
        if rowTo == 0 and Constants.Constants.BlackMen:
            pieceToMove.color = Constants.Constants.BlackKing
        elif rowTo == 7 and pieceToMove.color == Constants.Constants.WhiteMen:
            pieceToMove.color = Constants.Constants.WhiteKing
        board[0][(rowTo, colTo)] = pieceToMove
        del board[0][(rowFrom, colFrom)]

        # Capture move
        if abs(rowFrom - rowTo) == 2:
            rowDel = (max(rowFrom, rowTo) + min(rowFrom, rowTo)) // 2
            colDel = (max(colFrom, colTo) + min(colFrom, colTo)) // 2
            del board[0][(rowDel, colDel)]


    def __isGameOver(self, board):
        return False


    def getColor(self):
        return self.color


    def getOpponentType(self):
        return Constants.Constants.LevelTwoOpo