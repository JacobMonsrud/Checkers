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
        pieceFrom = self.piecesMap[(rowFrom, colFrom)]
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
        if pieceFrom.color in {Constants.Constants.White, Constants.Constants.WhiteKing}:
            if not self.playerInTurn == Constants.Constants.WhitePlayerTurn:
                return False
        elif pieceFrom.color in {Constants.Constants.Black, Constants.Constants.BlackKing}:
            if not self.playerInTurn == Constants.Constants.BlackPlayerTurn:
                return False

        # DELEGATE FROM HERE
        if pieceFrom.color in {Constants.Constants.White, Constants.Constants.Black}:
            return self.isValidMoveMen(rowFrom, colFrom, rowTo, colTo)
        elif pieceFrom.color in {Constants.Constants.WhiteKing, Constants.Constants.BlackKing}:
            return self.isValidMoveKing(rowFrom, colFrom, rowTo, colTo)
        else:
            # should never be reached
            return False


    # Precondition: Piece at from. No piece at to. Move to black square. Is players turn.
    # This only checks, does NOT change the board
    def isValidMoveMen(self, rowFrom, colFrom, rowTo, colTo):
        fromPiece = self.piecesMap[(rowFrom, colFrom)]
        colMovement = abs(colFrom - colTo)

        # Simple white move. No capture
        if colMovement == 1 and rowFrom + 1 == rowTo and fromPiece.color == Constants.Constants.White:
            return True
        # Simple black move. No capture
        elif colMovement == 1 and rowFrom - 1 == rowTo and fromPiece.color == Constants.Constants.Black:
            return True
        # White capture move
        elif colMovement == 2 and rowFrom + 2 == rowTo and fromPiece.color == Constants.Constants.White:
            if colFrom > colTo:
                # left jump | is jumping an enemy
                if (rowFrom + 1, colFrom - 1) in self.piecesMap:
                    return self.piecesMap[(rowFrom + 1, colFrom - 1)].color in {Constants.Constants.Black, Constants.Constants.BlackKing}
                else:
                    return False

            else:
                #right jump
                if (rowFrom + 1, colFrom + 1) in self.piecesMap:
                    return self.piecesMap[(rowFrom + 1, colFrom + 1)].color in {Constants.Constants.Black, Constants.Constants.BlackKing}
                else:
                    return False
        # Black capture move
        elif colMovement == 2 and rowFrom - 2 == rowTo and fromPiece.color == Constants.Constants.Black:
            if colFrom > colTo:
                # left jump | is jumping an enemy
                if (rowFrom - 1, colFrom - 1) in self.piecesMap:
                    return self.piecesMap[(rowFrom - 1, colFrom - 1)].color in {Constants.Constants.White, Constants.Constants.WhiteKing}
                else:
                    return False

            else:
                #right jump
                if (rowFrom - 1, colFrom + 1) in self.piecesMap:
                    return self.piecesMap[(rowFrom - 1, colFrom + 1)].color in {Constants.Constants.White, Constants.Constants.WhiteKing}
                else:
                    return False
        else:
            return False


    # Precondition: Piece at from. No piece at to. Move to black-square. Is players turn.
    # This only checks, does NOT change the board
    def isValidMoveKing(self, rowFrom, colFrom, rowTo, colTo):
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
                    return self.piecesMap[(checkRow, checkCol)].color in {Constants.Constants.Black, Constants.Constants.BlackKing}
                elif fromPiece.color == Constants.Constants.BlackKing:
                    return self.piecesMap[(checkRow, checkCol)].color in {Constants.Constants.White, Constants.Constants.WhiteKing}
            else:
                return False

        else:
            return False



    #Precondition: The move is checked valid.
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

        # Capture move
        if abs(rowFrom - rowTo) == 2:
            rowDel = (max(rowFrom, rowTo) + min(rowFrom, rowTo)) // 2
            colDel = (max(colFrom, colTo) + min(colFrom, colTo)) // 2
            self.removePieceAt(rowDel, colDel)
        # to be removed
        self.switchPlayerInTurn()

