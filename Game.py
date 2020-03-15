import Piece, Constants


class Game:

    def __init__(self):


        # Setup the board. Map form (row, col) to Pieces (class). (0,0) is top-left. 0 represents empty.
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


    def isValidMove(self, rowFrom, colFrom, rowTo, colTo):
        pass


    def movePieceFromTo(self, rowFrom, colFrom, rowTo, colTo):
        pieceToMove = self.piecesMap[(rowFrom, colFrom)]
        pieceToMove.row = rowTo
        pieceToMove.col = colTo
        self.piecesMap[(rowTo, colTo)] = pieceToMove
        del self.piecesMap[(rowFrom, colFrom)]
