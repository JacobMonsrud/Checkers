from Gameplay import Constants, Piece, ValidMoveAlgo
import copy

class Game:

    def __init__(self, opponent):
        self.opponent = opponent
        self.playerColor = self.__calcPlayerColor()
        self.playerInTurn = Constants.Constants.BlackPlayer
        self.validateMoveAlgo = ValidMoveAlgo.ValidMoveAlgo()
        self.lastMoveWasCapture = False
        self.shouldAnimate = (-1, -1, -1, -1, False)
        self.lastCaptureMovePos = (10, 10)
        self.currentWinner = Constants.Constants.NoWinner
        self.hashedBoards = dict()
        self.numberOfNoCaptures = 0
        # Setup the board. Map from (row, col) to Pieces (class). (0,0) is top-left.
        self.piecesMap = dict()
        self.__setupPieces()

        self.initGame()


    def __setupPieces(self) -> None:
        # Setup the white pieces
        for row in range(0, 3):
            if (row % 2 == 0):
                for col in range(1, 8, 2):
                    self.piecesMap[(row, col)] = Piece.Piece(row, col, Constants.Constants.WhiteMen)
            else:
                for col in range(0, 8, 2):
                    self.piecesMap[(row, col)] = Piece.Piece(row, col, Constants.Constants.WhiteMen)

        # Setup black
        for row in range(5, 8):
            if (row % 2 == 0):
                for col in range(1, 8, 2):
                    self.piecesMap[(row, col)] = Piece.Piece(row, col, Constants.Constants.BlackMen)
            else:
                for col in range(0, 8, 2):
                    self.piecesMap[(row, col)] = Piece.Piece(row, col, Constants.Constants.BlackMen)


    def initGame(self):
        # Black always starts
        if self.opponent.getColor() == Constants.Constants.BlackPlayer:
            (rf, cf, rt, ct) = self.getOpponentMove()
            if not (rf, cf, rt, ct) == (-1, -1, -1, -1):
                self.movePieceFromTo(rf, cf, rt, ct)


    def getPiecesMap(self) -> dict:
        # Risky not to return a copy, but is only used by the GUI. Good for preformence
        return self.piecesMap


    def getOpponent(self):
        return self.opponent


    def shouldAnimateMove(self):
        return self.shouldAnimate


    def terminateAnimation(self):
        self.shouldAnimate = (-1, -1, -1, -1, False)
        self.nextMove()


    def getPlayerColor(self):
        return self.playerColor


    def __calcPlayerColor(self):
        if self.opponent.getColor() == Constants.Constants.WhitePlayer:
            return Constants.Constants.BlackPlayer
        else:
            return Constants.Constants.WhitePlayer


    def removePieceAt(self, row, col) -> None:
        del self.piecesMap[(row, col)]


    def switchPlayerInTurn(self) -> None:
        if self.playerInTurn == Constants.Constants.BlackPlayer:
            self.playerInTurn = Constants.Constants.WhitePlayer
        else:
            self.playerInTurn = Constants.Constants.BlackPlayer



    # Should only be used by GUI, not AI's.
    def isValidMove(self, rowFrom, colFrom, rowTo, colTo) -> bool:
        # Game must not have ended
        if self.currentWinner in {Constants.Constants.WhitePlayer, Constants.Constants.BlackPlayer, Constants.Constants.Draw}:
            return False

        if self.shouldAnimate[4]:
            return False

        pieceFrom = self.piecesMap[(rowFrom, colFrom)]

        # Must be players turn. Must be players pieces. Except PvpOpo
        if pieceFrom.color in {Constants.Constants.WhiteMen, Constants.Constants.WhiteKing}:
            if not self.playerInTurn == Constants.Constants.WhitePlayer:
                return False
            if not self.opponent.getOpponentType() == Constants.Constants.PvpOpo:
                if not self.playerColor == Constants.Constants.WhitePlayer:
                    return False
        elif pieceFrom.color in {Constants.Constants.BlackMen, Constants.Constants.BlackKing}:
            if not self.playerInTurn == Constants.Constants.BlackPlayer:
                return False
            if not self.opponent.getOpponentType() == Constants.Constants.PvpOpo:
                if not self.playerColor == Constants.Constants.BlackPlayer:
                    return False

        # As I want a general purpose method for calculating valid moves.
        allValidMoves = self.validateMoveAlgo.getValidMovesForPlayer(self.playerInTurn, self.piecesMap)
        if (rowFrom, colFrom, rowTo, colTo) in allValidMoves:
            # Force double capture
            if self.lastMoveWasCapture:
                return abs(rowFrom - rowTo) == 2 and self.lastCaptureMovePos == (rowFrom, colFrom)
            else:
                return True


    # Precondition: The move is checked valid. Returns isComputerMove
    def movePieceFromTo(self, rowFrom, colFrom, rowTo, colTo):
        pieceToMove = self.piecesMap[(rowFrom, colFrom)]
        pieceToMove.row = rowTo
        pieceToMove.col = colTo
        if rowTo == 0 and Constants.Constants.BlackMen:
            pieceToMove.color = Constants.Constants.BlackKing
        elif rowTo == 7 and pieceToMove.color == Constants.Constants.WhiteMen:
            pieceToMove.color = Constants.Constants.WhiteKing
        self.piecesMap[(rowTo, colTo)] = pieceToMove
        self.removePieceAt(rowFrom, colFrom)

        self.lastMoveWasCapture = False
        self.lastCaptureMovePos = (10, 10)
        newTurn = True
        # Capture move
        if abs(rowFrom - rowTo) == 2:
            rowDel = (max(rowFrom, rowTo) + min(rowFrom, rowTo)) // 2
            colDel = (max(colFrom, colTo) + min(colFrom, colTo)) // 2
            self.removePieceAt(rowDel, colDel)
            self.numberOfNoCaptures = 0
            if self.isCaptureMoveFromPos(rowTo, colTo, self.piecesMap):
                self.lastMoveWasCapture = True
                self.lastCaptureMovePos = (rowTo, colTo)
                newTurn = False
        else:
            self.numberOfNoCaptures += 1

        if newTurn:
            self.switchPlayerInTurn()

        hashCurrentBoard = self.getHashForBoard()
        if hashCurrentBoard in self.hashedBoards:
            times = self.hashedBoards[hashCurrentBoard]
            times += 1
            self.hashedBoards[hashCurrentBoard] = times
        else:
            self.hashedBoards[hashCurrentBoard] = 1

        self.checkForWinner()

        if self.currentWinner == Constants.Constants.NoWinner:
            if not self.shouldAnimate[4]:
                self.nextMove()



    def nextMove(self):
        if self.playerInTurn == self.opponent.getColor():
            (rf, cf, rt, ct) = self.getOpponentMove()
            if not (rf, cf, rt, ct) == (-1, -1, -1, -1):
                self.shouldAnimate = (rf, cf, rt, ct, True)
                self.movePieceFromTo(rf, cf, rt, ct)


    def isCaptureMoveFromPos(self, row, col, board) -> bool:
        for move in {(row - 2, col - 2), (row - 2, col + 2), (row + 2, col - 2), (row + 2, col + 2)}:
            if self.validateMoveAlgo.isValidMoveCalc(row, col, move[0], move[1], board):
                return True
        return False


    # Win = opponent has no legal moves or no pieces left. As little calculation as possible
    def checkForWinner(self) -> int:
        if self.numberOfNoCaptures >= 50:
            self.currentWinner = Constants.Constants.Draw
            return Constants.Constants.Draw
        for board in self.hashedBoards.values():
            if board >= 3:
                self.currentWinner = Constants.Constants.Draw
                return Constants.Constants.Draw

        piecesWhite = [(r, c) for (r, c) in self.piecesMap if self.piecesMap[(r, c)].color in {Constants.Constants.WhiteMen, Constants.Constants.WhiteKing}]
        piecesBlack = [(r, c) for (r, c) in self.piecesMap if self.piecesMap[(r, c)].color in {Constants.Constants.BlackMen, Constants.Constants.BlackKing}]

        if len(piecesWhite) == 0 and self.playerInTurn == Constants.Constants.WhitePlayer:
            self.currentWinner = Constants.Constants.BlackPlayer
            return Constants.Constants.BlackPlayer
        elif len(piecesBlack) == 0 and self.playerInTurn == Constants.Constants.BlackPlayer:
            self.currentWinner = Constants.Constants.WhitePlayer
            return Constants.Constants.WhitePlayer

        whiteHasAMove = False
        blackHasAmove = False
        for piece in piecesWhite:
            (row, col) = piece
            for move in {(row - 1, col - 1), (row - 1, col + 1), (row + 1, col - 1), (row + 1, col + 1), (row - 2, col - 2), (row - 2, col + 2), (row + 2, col - 2), (row + 2, col + 2)}:
                if self.validateMoveAlgo.isValidMoveCalc(row, col, move[0], move[1], self.piecesMap):
                    whiteHasAMove = True
                    break
        for piece in piecesBlack:
            (row, col) = piece
            for move in {(row - 1, col - 1), (row - 1, col + 1), (row + 1, col - 1), (row + 1, col + 1), (row - 2, col - 2), (row - 2, col + 2), (row + 2, col - 2), (row + 2, col + 2)}:
                if self.validateMoveAlgo.isValidMoveCalc(row, col, move[0], move[1], self.piecesMap):
                    blackHasAmove = True
                    break

        if (whiteHasAMove and self.playerInTurn == Constants.Constants.WhitePlayer) or (blackHasAmove and self.playerInTurn == Constants.Constants.BlackPlayer):
            self.currentWinner = Constants.Constants.NoWinner
            return Constants.Constants.NoWinner
        if whiteHasAMove is False and self.playerInTurn == Constants.Constants.WhitePlayer:
            self.currentWinner = Constants.Constants.BlackPlayer
            return Constants.Constants.BlackPlayer
        if blackHasAmove is False and self.playerInTurn == Constants.Constants.BlackPlayer:
            self.currentWinner = Constants.Constants.WhitePlayer
            return Constants.Constants.WhitePlayer


    def getHashForBoard(self) -> str:
        # Loop as I want the same order every time
        hashStr = ''
        for row in range(0, 8):
            for col in range(0, 8):
                if (row, col) in self.piecesMap:
                    hashStr += self.piecesMap[(row, col)].getHash()
        return hashStr


    # Ask the opponent for a move to make
    def getOpponentMove(self):
        board = copy.deepcopy(self.piecesMap)
        # return: (rowFrom, colFrom, rowTo, colTo)
        return self.opponent.getMove(board)


