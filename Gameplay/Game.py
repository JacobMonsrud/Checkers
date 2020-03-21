from Gameplay import Constants, Piece


class Game:

    def __init__(self, opponent):
        self.opponent = opponent
        self.playerInTurn = Constants.Constants.BlackPlayer
        self.lastMoveWasCapture = False
        self.lastCaptureMovePos = (0, 0)
        # Setup the board. Map form (row, col) to Pieces (class). (0,0) is top-left.
        self.piecesMap = dict()
        self.setupPieces()


    def setupPieces(self) -> None:
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


    def getPiecesMap(self) -> dict:
        return self.piecesMap


    def getOpponent(self):
        return self.opponent


    def removePieceAt(self, row, col) -> None:
        del self.piecesMap[(row, col)]


    def switchPlayerInTurn(self) -> None:
        if self.playerInTurn == Constants.Constants.BlackPlayer:
            self.playerInTurn = Constants.Constants.WhitePlayer
        else:
            self.playerInTurn = Constants.Constants.BlackPlayer


    def isValidMove(self, rowFrom, colFrom, rowTo, colTo) -> bool:
        pieceFrom = self.piecesMap[(rowFrom, colFrom)]
        # Must be players turn
        if pieceFrom.color in {Constants.Constants.WhiteMen, Constants.Constants.WhiteKing}:
            if not self.playerInTurn == Constants.Constants.WhitePlayer:
                return False
        elif pieceFrom.color in {Constants.Constants.BlackMen, Constants.Constants.BlackKing}:
            if not self.playerInTurn == Constants.Constants.BlackPlayer:
                return False

        # As I want a general purpose method for calculating valid moves.
        allValidMoves = self.getValidMovesForPlayer(self.playerInTurn)
        if (rowFrom, colFrom, rowTo, colTo) in allValidMoves:
            # Force double capture
            if self.lastMoveWasCapture:
                return abs(rowFrom - rowTo) == 2
            else:
                return True


    # This only checks, does NOT change the board
    def isValidMoveCalc(self, rowFrom, colFrom, rowTo, colTo) -> bool:
        pieceFrom = self.piecesMap[(rowFrom, colFrom)]
        # Must be a piece at from pos
        if (rowFrom, colFrom) not in self.piecesMap:
            return False

        # No piece at to pos
        if (rowTo, colTo) in self.piecesMap:
            return False

        # Must be within the board
        for i in {rowFrom, rowTo, colFrom, colTo}:
            if not i in range(0, 8):
                return False

        # Only allow black squares
        if (rowTo + colTo) % 2 == 0:
            return False

        # DELEGATE FROM HERE
        if pieceFrom.color in {Constants.Constants.WhiteMen, Constants.Constants.BlackMen}:
            return self.__isValidMoveMen(rowFrom, colFrom, rowTo, colTo)
        elif pieceFrom.color in {Constants.Constants.WhiteKing, Constants.Constants.BlackKing}:
            return self.__isValidMoveKing(rowFrom, colFrom, rowTo, colTo)
        else:
            # should never be reached
            return False


    # Precondition: Piece at from. No piece at to. Move to black square. Within the board
    # This only checks, does NOT change the board
    def __isValidMoveMen(self, rowFrom, colFrom, rowTo, colTo) -> bool:
        fromPiece = self.piecesMap[(rowFrom, colFrom)]
        colMovement = abs(colFrom - colTo)

        # Simple white move. No capture
        if colMovement == 1 and rowFrom + 1 == rowTo and fromPiece.color == Constants.Constants.WhiteMen:
            return True
        # Simple black move. No capture
        elif colMovement == 1 and rowFrom - 1 == rowTo and fromPiece.color == Constants.Constants.BlackMen:
            return True
        # White capture move
        elif colMovement == 2 and rowFrom + 2 == rowTo and fromPiece.color == Constants.Constants.WhiteMen:
            if colFrom > colTo:
                # left jump | is jumping an enemy
                if (rowFrom + 1, colFrom - 1) in self.piecesMap:
                    return self.piecesMap[(rowFrom + 1, colFrom - 1)].color in {Constants.Constants.BlackMen, Constants.Constants.BlackKing}
                else:
                    return False

            else:
                #right jump
                if (rowFrom + 1, colFrom + 1) in self.piecesMap:
                    return self.piecesMap[(rowFrom + 1, colFrom + 1)].color in {Constants.Constants.BlackMen, Constants.Constants.BlackKing}
                else:
                    return False
        # Black capture move
        elif colMovement == 2 and rowFrom - 2 == rowTo and fromPiece.color == Constants.Constants.BlackMen:
            if colFrom > colTo:
                # left jump | is jumping an enemy
                if (rowFrom - 1, colFrom - 1) in self.piecesMap:
                    return self.piecesMap[(rowFrom - 1, colFrom - 1)].color in {Constants.Constants.WhiteMen, Constants.Constants.WhiteKing}
                else:
                    return False

            else:
                #right jump
                if (rowFrom - 1, colFrom + 1) in self.piecesMap:
                    return self.piecesMap[(rowFrom - 1, colFrom + 1)].color in {Constants.Constants.WhiteMen, Constants.Constants.WhiteKing}
                else:
                    return False
        else:
            return False


    # Precondition: Piece at from. No piece at to. Move to black-square. Within the board
    # This only checks, does NOT change the board
    def __isValidMoveKing(self, rowFrom, colFrom, rowTo, colTo) -> bool:
        fromPiece = self.piecesMap[(rowFrom, colFrom)]
        colMovement = abs(colFrom - colTo)
        rowMovement = abs(rowFrom - rowTo)

        # Simple white or black move. No capture
        if colMovement == 1 and rowMovement == 1:
            return True
        # Capture
        elif colMovement == 2 and rowMovement == 2:
            checkRow = (max(rowFrom, rowTo) + min(rowFrom, rowTo)) / 2
            checkCol = (max(colFrom, colTo) + min(colFrom, colTo)) / 2
            if (checkRow, checkCol) in self.piecesMap:
                if fromPiece.color == Constants.Constants.WhiteKing:
                    return self.piecesMap[(checkRow, checkCol)].color in {Constants.Constants.BlackMen, Constants.Constants.BlackKing}
                elif fromPiece.color == Constants.Constants.BlackKing:
                    return self.piecesMap[(checkRow, checkCol)].color in {Constants.Constants.WhiteMen, Constants.Constants.WhiteKing}
            else:
                return False
        else:
            return False


    #Precondition: The move is checked valid.
    def movePieceFromTo(self, rowFrom, colFrom, rowTo, colTo) -> None:
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
        newTurn = True
        # Capture move
        if abs(rowFrom - rowTo) == 2:
            rowDel = (max(rowFrom, rowTo) + min(rowFrom, rowTo)) // 2
            colDel = (max(colFrom, colTo) + min(colFrom, colTo)) // 2
            self.removePieceAt(rowDel, colDel)

            if self.isCaptureMoveFromPos(rowTo, colTo):
                self.lastMoveWasCapture = True
                self.lastCaptureMovePos = (rowTo, colTo)
                newTurn = False

        if newTurn:
            self.switchPlayerInTurn()


    def getValidMovesForPlayer(self, player) -> set:
        # Map from start pos to end pos.
        legalMoves = set()
        piecesList = list()
        # Get pos of all players pieces
        if player == Constants.Constants.WhitePlayer:
            piecesList = [(r, c) for (r, c) in self.piecesMap if self.piecesMap[(r, c)].color in {Constants.Constants.WhiteMen, Constants.Constants.WhiteKing}]
        else:
            piecesList = [(r, c) for (r, c) in self.piecesMap if self.piecesMap[(r, c)].color in {Constants.Constants.BlackMen, Constants.Constants.BlackKing}]

        for piecePos in piecesList:
            # Search first for capture moves, as these MUST be done if avaliable before normal moves.
            row = int(piecePos[0])
            col = int(piecePos[1])
            for move in {(row - 2, col - 2), (row - 2, col + 2), (row + 2, col - 2), (row + 2, col + 2)}:
                 if self.isValidMoveCalc(row, col, int(move[0]), int(move[1])):
                    legalMoves.add((row, col, int(move[0]), int(move[1])))

        if len(legalMoves) > 0:
            return legalMoves
        else:
            for piecePos in piecesList:
                row = int(piecePos[0])
                col = int(piecePos[1])
                for moveOne in {(row - 1, col - 1), (row - 1, col + 1), (row + 1, col - 1), (row + 1, col + 1)}:
                    if self.isValidMoveCalc(row, col, int(moveOne[0]), int(moveOne[1])):
                        legalMoves.add((row, col, int(moveOne[0]), int(moveOne[1])))
            return legalMoves


    def isCaptureMoveFromPos(self, row, col) -> bool:
        for move in {(row - 2, col - 2), (row - 2, col + 2), (row + 2, col - 2), (row + 2, col + 2)}:
            if self.isValidMoveCalc(row, col, int(move[0]), int(move[1])):
                return True
        return False


    # Win = opponent has no legal moves or no pieces left
    def checkForWinner(self):
        pass