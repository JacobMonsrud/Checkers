from Gameplay import Constants, Piece

class ValidMoveAlgo:

    def __init__(self):
        pass

    # This only checks, does NOT change the board
    def isValidMoveCalc(self, rowFrom, colFrom, rowTo, colTo, board) -> bool:
        pieceFrom = board[(rowFrom, colFrom)]
        # Must be a piece at from pos
        if (rowFrom, colFrom) not in board:
            return False

        # No piece at to pos
        if (rowTo, colTo) in board:
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
            return self.__isValidMoveMen(rowFrom, colFrom, rowTo, colTo, board)
        elif pieceFrom.color in {Constants.Constants.WhiteKing, Constants.Constants.BlackKing}:
            return self.__isValidMoveKing(rowFrom, colFrom, rowTo, colTo, board)
        else:
            # should never be reached
            return False


    # Precondition: Piece at from. No piece at to. Move to black square. Within the board
    # This only checks, does NOT change the board
    def __isValidMoveMen(self, rowFrom, colFrom, rowTo, colTo, board) -> bool:
        fromPiece = board[(rowFrom, colFrom)]
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
                if (rowFrom + 1, colFrom - 1) in board:
                    return board[(rowFrom + 1, colFrom - 1)].color in {Constants.Constants.BlackMen, Constants.Constants.BlackKing}
                else:
                    return False

            else:
                #right jump
                if (rowFrom + 1, colFrom + 1) in board:
                    return board[(rowFrom + 1, colFrom + 1)].color in {Constants.Constants.BlackMen, Constants.Constants.BlackKing}
                else:
                    return False
        # Black capture move
        elif colMovement == 2 and rowFrom - 2 == rowTo and fromPiece.color == Constants.Constants.BlackMen:
            if colFrom > colTo:
                # left jump | is jumping an enemy
                if (rowFrom - 1, colFrom - 1) in board:
                    return board[(rowFrom - 1, colFrom - 1)].color in {Constants.Constants.WhiteMen, Constants.Constants.WhiteKing}
                else:
                    return False

            else:
                #right jump
                if (rowFrom - 1, colFrom + 1) in board:
                    return board[(rowFrom - 1, colFrom + 1)].color in {Constants.Constants.WhiteMen, Constants.Constants.WhiteKing}
                else:
                    return False
        else:
            return False


    # Precondition: Piece at from. No piece at to. Move to black-square. Within the board
    # This only checks, does NOT change the board
    def __isValidMoveKing(self, rowFrom, colFrom, rowTo, colTo, board) -> bool:
        fromPiece = board[(rowFrom, colFrom)]
        colMovement = abs(colFrom - colTo)
        rowMovement = abs(rowFrom - rowTo)

        # Simple white or black move. No capture
        if colMovement == 1 and rowMovement == 1:
            return True
        # Capture
        elif colMovement == 2 and rowMovement == 2:
            checkRow = (max(rowFrom, rowTo) + min(rowFrom, rowTo)) / 2
            checkCol = (max(colFrom, colTo) + min(colFrom, colTo)) / 2
            if (checkRow, checkCol) in board:
                if fromPiece.color == Constants.Constants.WhiteKing:
                    return board[(checkRow, checkCol)].color in {Constants.Constants.BlackMen, Constants.Constants.BlackKing}
                elif fromPiece.color == Constants.Constants.BlackKing:
                    return board[(checkRow, checkCol)].color in {Constants.Constants.WhiteMen, Constants.Constants.WhiteKing}
            else:
                return False
        else:
            return False


    def getValidMovesForPlayer(self, player, board) -> set:
        # Map from start pos to end pos.
        legalMoves = set()
        piecesList = list()
        # Get pos of all players pieces
        if player == Constants.Constants.WhitePlayer:
            piecesList = [(r, c) for (r, c) in board if board[(r, c)].color in {Constants.Constants.WhiteMen, Constants.Constants.WhiteKing}]
        else:
            piecesList = [(r, c) for (r, c) in board if board[(r, c)].color in {Constants.Constants.BlackMen, Constants.Constants.BlackKing}]

        for piecePos in piecesList:
            # Search first for capture moves, as these MUST be done if avaliable before normal moves.
            row = piecePos[0]
            col = piecePos[1]
            for move in {(row - 2, col - 2), (row - 2, col + 2), (row + 2, col - 2), (row + 2, col + 2)}:
                 if self.isValidMoveCalc(row, col, move[0], move[1], board):
                    legalMoves.add((row, col, move[0], move[1]))

        if len(legalMoves) > 0:
            return legalMoves
        else:
            for piecePos in piecesList:
                row = piecePos[0]
                col = piecePos[1]
                for moveOne in {(row - 1, col - 1), (row - 1, col + 1), (row + 1, col - 1), (row + 1, col + 1)}:
                    if self.isValidMoveCalc(row, col, moveOne[0], moveOne[1], board):
                        legalMoves.add((row, col, moveOne[0], moveOne[1]))
            return legalMoves