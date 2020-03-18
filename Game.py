import Piece, Constants


class Game:

    def __init__(self):
        self.playerInTurn = Constants.Constants.BlackPlayerTurn
        # Setup the board. Map form (row, col) to Pieces (class). (0,0) is top-left.
        self.piecesMap = dict()
        self.setupPieces()

    def setupPieces(self):
        # Setup the white pieces
        for row in range(0, 3):
            if (row % 2 == 0):
                for col in range(1, 8, 2):
                    self.piecesMap[(row, col)] = Piece.Piece(row, col, Constants.Constants.White)
            else:
                for col in range(0, 8, 2):
                    self.piecesMap[(row, col)] = Piece.Piece(row, col, Constants.Constants.White)

        # Setup black
        for row in range(5, 8):
            if (row % 2 == 0):
                for col in range(1, 8, 2):
                    self.piecesMap[(row, col)] = Piece.Piece(row, col, Constants.Constants.Black)
            else:
                for col in range(0, 8, 2):
                    self.piecesMap[(row, col)] = Piece.Piece(row, col, Constants.Constants.Black)


    def getPiecesMap(self):
        return self.piecesMap


    def removePieceAt(self, row, col):
        del self.piecesMap[(row, col)]


    def switchPlayerInTurn(self):
        if self.playerInTurn == Constants.Constants.BlackPlayerTurn:
            self.playerInTurn = Constants.Constants.WhitePlayerTurn
        else:
            self.playerInTurn = Constants.Constants.BlackPlayerTurn


    def isValidMove(self, rowFrom, colFrom, rowTo, colTo):
        # Must be a piece at from pos
        if (rowFrom, colFrom) not in self.piecesMap:
            return False

        # No piece at to pos
        if (rowTo, colTo) in self.piecesMap:
            return False

        # Only allow black squares
        if (rowTo + colTo) % 2 == 0:
            return False

        # Must be players turn
        if self.piecesMap[(rowFrom, colFrom)].color in {Constants.Constants.White, Constants.Constants.WhiteKing}:
            if not self.playerInTurn == Constants.Constants.WhitePlayerTurn:
                return False
        elif self.piecesMap[(rowFrom, colFrom)].color in {Constants.Constants.Black, Constants.Constants.BlackKing}:
            if not self.playerInTurn == Constants.Constants.BlackPlayerTurn:
                return False

        # Only allow forward movement for normal pieces
        if self.piecesMap[(rowFrom, colFrom)].color == Constants.Constants.White:
            if rowFrom >= rowTo:
                return False
        elif self.piecesMap[(rowFrom, colFrom)].color == Constants.Constants.Black:
            if rowFrom <= rowTo:
                return False

        # Only god knows how this works
        if self.piecesMap[(rowFrom, colFrom)].color in {Constants.Constants.White, Constants.Constants.WhiteKing}:
            legal = True
            if (colFrom + 1 == colTo or colFrom - 1 == colTo) and rowFrom == rowTo - 1 and self.piecesMap[(rowFrom, colFrom)].color == Constants.Constants.White:
                legal = True
            elif (colFrom + 1 == colTo or colFrom - 1 == colTo) and (rowFrom == rowTo - 1 or rowFrom == rowTo + 1) and self.piecesMap[(rowFrom, colFrom)].color == Constants.Constants.WhiteKing:
                legal = True
            # ^^ Illegal unless its jump an opponent
            elif abs(colFrom - colTo) == 2 and abs(rowFrom - rowTo) == 2:
                if colFrom > colTo:
                    # left jump
                    if (rowFrom + 1, colFrom - 1) in self.piecesMap:
                        if self.piecesMap[(rowFrom + 1, colFrom - 1)].color in {Constants.Constants.Black, Constants.Constants.BlackKing}:
                            legal = True
                            self.removePieceAt(rowFrom + 1, colFrom - 1)
                        else:
                            legal = False
                    elif (rowFrom - 1, colFrom - 1) in self.piecesMap and self.piecesMap[((rowFrom, colFrom))].color == Constants.Constants.WhiteKing:
                        if self.piecesMap[(rowFrom - 1, colFrom - 1)].color in {Constants.Constants.Black, Constants.Constants.BlackKing}:
                            legal = True
                            self.removePieceAt(rowFrom - 1, colFrom - 1)
                        else:
                            legal = False
                    else:
                        legal = False
                else:
                    # right jump
                    if (rowFrom + 1, colFrom + 1) in self.piecesMap:
                        if self.piecesMap[(rowFrom + 1, colFrom + 1)].color in {Constants.Constants.Black, Constants.Constants.BlackKing}:
                            legal = True
                            self.removePieceAt(rowFrom + 1, colFrom + 1)
                        else:
                            legal = False
                    elif (rowFrom - 1, colFrom + 1) in self.piecesMap and self.piecesMap[((rowFrom, colFrom))].color == Constants.Constants.WhiteKing:
                        if self.piecesMap[(rowFrom - 1, colFrom + 1)].color in {Constants.Constants.Black, Constants.Constants.BlackKing}:
                            legal = True
                            self.removePieceAt(rowFrom - 1, colFrom + 1)
                        else:
                            legal = False
                    else:
                        legal = False
            else:
                legal = False
            if not legal:
                return False

        elif self.piecesMap[(rowFrom, colFrom)].color in {Constants.Constants.Black, Constants.Constants.BlackKing}:
            legal = True
            if (colFrom + 1 == colTo or colFrom - 1 == colTo) and rowFrom == rowTo + 1 and self.piecesMap[(rowFrom, colFrom)].color == Constants.Constants.Black:
                legal = True
            elif (colFrom + 1 == colTo or colFrom - 1 == colTo) and (rowFrom == rowTo + 1 or rowFrom == rowTo - 1) and self.piecesMap[(rowFrom, colFrom)].color == Constants.Constants.BlackKing:
                legal = True
                # ^^ Illegal unless its jump an opponent
            elif abs(colFrom - colTo) == 2 and abs(rowFrom - rowTo) == 2:
                if colFrom > colTo:
                    # left jump
                    if (rowFrom - 1, colFrom - 1) in self.piecesMap:
                        if self.piecesMap[(rowFrom - 1, colFrom - 1)].color in {Constants.Constants.White, Constants.Constants.WhiteKing}:
                            legal = True
                            self.removePieceAt(rowFrom - 1, colFrom - 1)
                        else:
                            legal = False
                    elif (rowFrom + 1, colFrom - 1) in self.piecesMap and self.piecesMap[((rowFrom, colFrom))].color == Constants.Constants.BlackKing:
                        if self.piecesMap[(rowFrom + 1, colFrom - 1)].color in {Constants.Constants.White, Constants.Constants.WhiteKing}:
                            legal = True
                            self.removePieceAt(rowFrom + 1, colFrom - 1)
                        else:
                            legal = False
                    else:
                        legal = False
                else:
                    # right jump
                    if (rowFrom - 1, colFrom + 1) in self.piecesMap:
                        if self.piecesMap[(rowFrom - 1, colFrom + 1)].color in {Constants.Constants.White, Constants.Constants.WhiteKing}:
                            legal = True
                            self.removePieceAt(rowFrom - 1, colFrom + 1)
                        else:
                            legal = False
                    elif (rowFrom + 1, colFrom + 1) in self.piecesMap and self.piecesMap[((rowFrom, colFrom))].color == Constants.Constants.BlackKing:
                        if self.piecesMap[(rowFrom + 1, colFrom + 1)].color in {Constants.Constants.White, Constants.Constants.WhiteKing}:
                            legal = True
                            self.removePieceAt(rowFrom + 1, colFrom + 1)
                        else:
                            legal = False
                    else:
                        legal = False
            else:
                legal = False
            if not legal:
                return False

        return True


    def isValidMoveBlack(self):
        pass


    def isValidMoveWhite(self):
        pass


    def isValidMoveBlackKing(self):
        pass


    def isValidMoveWhiteKing(self):
        pass


    def movePieceFromTo(self, rowFrom, colFrom, rowTo, colTo):
        pieceToMove = self.piecesMap[(rowFrom, colFrom)]
        pieceToMove.row = rowTo
        pieceToMove.col = colTo
        if rowTo == 0 and Constants.Constants.Black:
            pieceToMove.color = Constants.Constants.BlackKing
        elif rowTo == 7 and pieceToMove.color == Constants.Constants.White:
            pieceToMove.color = Constants.Constants.WhiteKing
        self.piecesMap[(rowTo, colTo)] = pieceToMove
        self.removePieceAt(rowFrom, colFrom)


        # to be removed
        self.switchPlayerInTurn()

