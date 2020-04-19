from Gameplay import Constants, ValidMoveAlgo
from Test import TestsMethods
import random, copy, sys

# Classic Minimax.
class LevelTwoOpponent:

    def __init__(self, color):
        # Color is black or white
        self.color = color
        self.validateMoveAlgo = ValidMoveAlgo.ValidMoveAlgo()
        self.toDoMoves = list()
        self.maxBoards = list()
        self.depth = 0


    def getMove(self, board):
        if len(self.toDoMoves) == 0:
            l = list()
            l.append(board)
            #print("start board: " + str(l[0]))
            self.maxBoards = list()
            self.depth = 4
            max = self.__minimax(l, 4, self.color, self.color)
            print("max[0]: " + str(max))
            #print("max[1][1:]: " + str(max[1][1:]))
            #print("maxBoards:")
            captureMaxBoards = list()
            nonCaptureMaxBoards = list()
            for bo in self.maxBoards:
                #test = TestsMethods.TestsMethods()
                #test.printBoard(bo[0])
                #print(str(bo[0]))
                #print(str(bo[1:]))
                # Check if capture move is avaliable
                boardActuall = bo[0]
                moves = bo[1:]
                firstMove = moves[0]
                if abs(firstMove[0] - firstMove[2]) == 2:
                    captureMaxBoards.append(bo)
                else:
                    nonCaptureMaxBoards.append(bo)

            boardToPlay = list()
            if len(captureMaxBoards) > 0:
                boardToPlay = random.choice(captureMaxBoards)
            else:
                boardToPlay = random.choice(nonCaptureMaxBoards)
            actBoard = boardToPlay[0]
            actMoves = boardToPlay[1:]
            #print(actMoves)
            firstMove = actMoves[0]
            lastMove = firstMove
            for move in actMoves[1:]:
                #print("move: " + str(move))
                if (lastMove[2], lastMove[3]) == (move[0], move[1]):
                    #print("double jump:" + str(lastMove[2]) + str(lastMove[3]) + " to " + str(move[0]) + str(move[1]))
                    self.toDoMoves.append(move)
                    lastMove = move
                else:
                    break

            return firstMove
        else:
            #print("to do: " + str(self.toDoMoves[0]))
            return self.toDoMoves.pop(0)


    def __minimax(self, board, depth, playerInTurnDynamic, maximizingPlayer):
        if depth == 0 or self.__isGameOver(board):
            #print("depth = 0")
            return self.calcBoardValue(board, maximizingPlayer)

        if playerInTurnDynamic == maximizingPlayer:
            maxValue = -10000000
            childBoards = self.getChildBoards(board, playerInTurnDynamic)
            for child in childBoards:
                newPlayerInTurn = self.__getNewPlayerInTurn(playerInTurnDynamic)
                value = self.__minimax(child, depth - 1, newPlayerInTurn, maximizingPlayer)
                if self.depth == depth:
                    if maxValue == value or maxValue == -10000000:
                        self.maxBoards.append(child)
                    elif maxValue < value:
                        self.maxBoards = list()
                        self.maxBoards.append(child)
                maxValue = max(maxValue, value)
            return maxValue
        else:
            minValue = 10000000
            childBoards = self.getChildBoards(board, playerInTurnDynamic)
            for child in childBoards:
                newPlayerInTurn = self.__getNewPlayerInTurn(playerInTurnDynamic)
                value = self.__minimax(child, depth - 1, newPlayerInTurn, maximizingPlayer)
                minValue = min(minValue, value)
            return minValue


    def calcBoardValue(self, board, maximizingPlayer):
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


    def __getNewPlayerInTurn(self, player):
        if player == Constants.Constants.WhitePlayer:
            return Constants.Constants.BlackPlayer
        else:
            return Constants.Constants.WhitePlayer

    # All sequences of multiple captures count as one move.
    # ChildBoards is a list af list (the board at [0] and the moves to get to that board at [1:])
    def getChildBoards(self, board, playerColor):
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