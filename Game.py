import Piece, Constants


class Game:

    def __init__(self):
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

        # Only allow forward movement for normal pieces
        if self.piecesMap[(rowFrom, colFrom)].color == Constants.Constants.White:
            if rowFrom >= rowTo:
                return False
        elif self.piecesMap[(rowFrom, colFrom)].color == Constants.Constants.Black:
            if rowFrom <= rowTo:
                return False

        # Only allow a movement of dist 1 or jump opponent
        if self.piecesMap[(rowFrom, colFrom)].color == Constants.Constants.White:
            legal = True
            if not (((colFrom + 1) == colTo or (colFrom - 1) == colTo) and (rowFrom == rowTo - 1)):
                legal = False
                # ^^ Illegal unless its jump an opponent
                if abs(colFrom - colTo) == 2 and abs(rowFrom - rowTo) == 2:
                    if colFrom > colTo:
                        # left jump
                        if (rowFrom + 1, colFrom - 1) in self.piecesMap:
                            if self.piecesMap[(rowFrom + 1, colFrom - 1)].color == Constants.Constants.Black:
                                legal = True
                                self.removePieceAt(rowFrom + 1, colFrom - 1)
                    else:
                        # right jump
                        if (rowFrom + 1, colFrom + 1) in self.piecesMap:
                            if self.piecesMap[(rowFrom + 1, colFrom + 1)].color == Constants.Constants.Black:
                                legal = True
                                self.removePieceAt(rowFrom + 1, colFrom + 1)
            if not legal:
                return False
        elif self.piecesMap[(rowFrom, colFrom)].color == Constants.Constants.Black:
            legal = True
            if not (((colFrom + 1) == colTo or (colFrom - 1) == colTo) and (rowFrom == rowTo + 1)):
                legal = False
                # ^^ Illegal unless its jump an opponent
                if abs(colFrom - colTo) == 2 and abs(rowFrom - rowTo) == 2:
                    if colFrom > colTo:
                        # left jump
                        if (rowFrom - 1, colFrom - 1) in self.piecesMap:
                            if self.piecesMap[(rowFrom - 1, colFrom - 1)].color == Constants.Constants.White:
                                legal = True
                                self.removePieceAt(rowFrom - 1, colFrom - 1)
                    else:
                        # right jump
                        if (rowFrom - 1, colFrom + 1) in self.piecesMap:
                            if self.piecesMap[(rowFrom - 1, colFrom + 1)].color == Constants.Constants.White:
                                legal = True
                                self.removePieceAt(rowFrom - 1, colFrom + 1)
            if not legal:
                return False

        return True


    def movePieceFromTo(self, rowFrom, colFrom, rowTo, colTo):
        pieceToMove = self.piecesMap[(rowFrom, colFrom)]
        pieceToMove.row = rowTo
        pieceToMove.col = colTo
        self.piecesMap[(rowTo, colTo)] = pieceToMove
        self.removePieceAt(rowFrom, colFrom)
