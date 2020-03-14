import pygame
import Piece
import Constants


class GameGUI:

    def __init__(self, window, clock):
        self.window = window
        self.clock = clock

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


    def getCenterPosForBoardSquare(self, xPixelPos, yPixelPos):
        indexX = 0
        indexY = 0

        jump = Constants.screen_dimension // 10

        for i in range(0, 10):
            left = i * jump
            if left <= xPixelPos <= left + jump:
                indexX = i

            if left <= yPixelPos <= left + jump:
                indexY = i

        centerX = (indexX * jump) + (jump // 2)
        centerY = (indexY * jump) + (jump // 2)

        return (centerX, centerY)


    def getPieceIndexAt(self, xPixelPos, yPixelPos):
        indexX = 0
        indexY = 0
        jump = Constants.screen_dimension // 10

        for i in range(0, 10):
            left = i * jump
            if left <= xPixelPos <= left + jump:
                indexX = i

            if left <= yPixelPos <= left + jump:
                indexY = i
        # As x-pos is col and y-pos is row
        return (indexY - 1, indexX - 1)


    def redrawGameWindow(self, exceptIndexX, exceptIndexY, dragX, dragY):
        # Board
        self.window.fill((247, 126, 0))
        self.window.blit(pygame.image.load('GUI/images/board.png'), (55, 55))

        # Draw pieces according to
        for row in range(0, 8):
            for col in range(0, 8):
                if (row, col) in self.piecesMap and (row, col) != (exceptIndexX, exceptIndexY):
                    currentPiece = self.piecesMap[(row, col)]
                    (pixelX, pixelY) = currentPiece.getPixelPos()
                    if currentPiece.color == Constants.Constants.Black:
                        self.window.blit(pygame.image.load('GUI/images/blackpiece.png'), (pixelX, pixelY))
                    elif currentPiece.color == Constants.Constants.White:
                        self.window.blit(pygame.image.load('GUI/images/whitepiece.png'), (pixelX, pixelY))

                elif (row, col) in self.piecesMap and (row, col) == (exceptIndexX, exceptIndexY):
                    movingPiece = self.piecesMap[(row, col)]
                    centerDragX = dragX - (Constants.piece_dimension // 2)
                    centerDragY = dragY - (Constants.piece_dimension // 2)
                    if movingPiece.color == Constants.Constants.Black:
                        self.window.blit(pygame.image.load('GUI/images/blackpiece.png'), (centerDragX, centerDragY))
                    elif movingPiece.color == Constants.Constants.White:
                        self.window.blit(pygame.image.load('GUI/images/whitepiece.png'), (centerDragX, centerDragY))

        pygame.display.update()


    def runGame(self):

        drag = False
        (dragX, dragY) = (0, 0)
        (exceptIndexX, exceptIndexY) = (10, 10)

        # Main loop
        run = True
        while run:
            # fps
            self.clock.tick(Constants.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Find the correct piece
                    (row, col) = self.getPieceIndexAt(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                    if 0 <= row <= 7 and 0 <= col <= 7:
                        if (row, col) in self.piecesMap:
                            drag = True
                            (dragX, dragY) = pygame.mouse.get_pos()
                            (exceptIndexX, exceptIndexY) = (row, col)

                if event.type == pygame.MOUSEMOTION:
                    if drag:
                        (dragX, dragY) = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONUP:
                    (newRow, newCol) = self.getPieceIndexAt(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                    if 0 <= newRow <= 7 and 0 <= newCol <= 7:
                        if (exceptIndexX, exceptIndexY) in self.piecesMap:
                            pieceToMove = self.piecesMap[(exceptIndexX, exceptIndexY)]
                            pieceToMove.row = newRow
                            pieceToMove.col = newCol
                            self.piecesMap[(newRow, newCol)] = pieceToMove
                            self.piecesMap.pop((exceptIndexX, exceptIndexY))

                    drag = False
                    (dragX, dragY) = (0, 0)
                    (exceptIndexX, exceptIndexY) = (10, 10)


            self.redrawGameWindow(exceptIndexX, exceptIndexY, dragX, dragY)

        pygame.quit()

