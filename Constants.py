import enum

fps = 30
screen_dimension = 600
piece_dimension = 40

class Constants(enum.Enum):
    White = 0
    Black = 1
    WhiteKing = 2
    BlackKing = 3

    WhitePlayerTurn = 4
    BlackPlayerTurn = 5