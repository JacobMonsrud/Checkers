import enum

fps = 30
screen_dimension = 600
piece_dimension = 40


class Constants(enum.Enum):
    WhiteMen = 0
    BlackMen = 1
    WhiteKing = 2
    BlackKing = 3

    WhitePlayer = 4
    BlackPlayer = 5

    Draw = 6
    NoWinner = 7

    PvpOpo = 8
    LevelZeroOpo = 9
    LevelOneOpo = 10
    LevelTwoOpo = 11
