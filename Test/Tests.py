from Test import TestsMethods
from AI import LevelTwoOpponent
from Gameplay import Constants

def testChildBoards():
    methods = TestsMethods.TestsMethods()
    oppoPlayer = Constants.Constants.BlackPlayer
    lvl2 = LevelTwoOpponent.LevelTwoOpponent(oppoPlayer)

    boardStr = ' _ w _ w _ w _ w |' \
               ' w _ w _ w _ w _ |' \
               ' _ w _ w _ w _ w |' \
               ' _ _ _ _ _ _ _ _ |' \
               ' _ w _ _ _ _ _ b |' \
               ' b _ _ _ b _ b _ |' \
               ' _ _ _ b _ b _ b |' \
               ' b _ b _ _ _ b _ '

    board = methods.convertStringToBoard(boardStr)
    b = list()
    b.append(board)

    print("initial Board:\n")
    print(methods.printBoard(b[0]))
    print("")

    cboards = lvl2.getChildBoards(b, oppoPlayer)
    print("Child board:\n")
    for bor in cboards:
        methods.printBoard(bor[0])
        val = lvl2.calcBoardValue(bor, oppoPlayer)
        print(str(val))
        for moves in bor[1:]:
            print(moves)
        print("")

def runTests():
   testChildBoards()

if __name__ == '__main__':
    runTests()
