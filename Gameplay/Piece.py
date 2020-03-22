from Gameplay import Constants


# Pieces are only used by the GUI.
class Piece:

    def __init__(self, row, col, color):
        # x and y refers to the index position on the board
        self.row = row
        self.col = col
        self.color = color

    def getPixelPos(self):
        dim = Constants.screen_dimension // 10
        offset = (dim - Constants.piece_dimension) // 2

        pixelX = (self.col + 1) * dim + offset
        pixelY = (self.row + 1) * dim + offset
        return (pixelX, pixelY)


    def getHash(self):
        c = 0
        return str(self.row) + str(self.col) + str(self.color.value)
