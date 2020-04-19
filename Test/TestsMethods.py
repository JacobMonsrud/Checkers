from Gameplay import Constants, Piece

#Some usefull test methods
class TestsMethods:

    def __init__(self):
        pass

    def printBoard(self, board):
        print('   0 1 2 3 4 5 6 7')
        for row in range(0, 8):
            rowString = ''
            rowString += str(row) + '  '
            for col in range(0, 8):
                if (row, col) in board:
                    currentPiece = board[(row, col)]
                    if currentPiece.color == Constants.Constants.BlackMen:
                        rowString += "b "
                    elif currentPiece.color == Constants.Constants.WhiteMen:
                        rowString += "w "
                    elif currentPiece.color == Constants.Constants.BlackKing:
                        rowString += "B "
                    elif currentPiece.color == Constants.Constants.WhiteKing:
                        rowString += "W "
                else:
                    rowString += "_ "
            print(rowString.strip())
        print("")


    def convertStringToBoard(self, boardStr):
        board = dict()

        arr = boardStr.replace(" ", "").split("|")
        row = 0
        for rowStr in arr:
            pieces = list(rowStr)
            col = 0
            for colStr in pieces:
                if colStr == 'w':
                    board[(row, col)] = Piece.Piece(row, col, Constants.Constants.WhiteMen)
                elif colStr == 'b':
                    board[(row, col)] = Piece.Piece(row, col, Constants.Constants.BlackMen)
                elif colStr == 'W':
                    board[(row, col)] = Piece.Piece(row, col, Constants.Constants.WhiteKing)
                elif colStr == 'B':
                    board[(row, col)] = Piece.Piece(row, col, Constants.Constants.BlackKing)
                col += 1
            row += 1
        return board