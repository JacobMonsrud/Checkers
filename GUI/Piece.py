from GUI import MainGUI

class Piece:

    def __init__(self, row, col, color):
        # x and y refers to the index position on the board
        self.row = row
        self.col = col
        self.color = color

    def getPixelPos(self):
        dim = MainGUI.MainGUI.screen_dimension // 10
        offset = (dim - MainGUI.MainGUI.piece_dimension) // 2

        pixelX = (self.row + 1) * dim + offset
        pixelY = (self.col + 1) * dim + offset
        return (pixelX, pixelY)