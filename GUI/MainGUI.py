import pygame
import numpy
from GUI import Constants, Piece

class MainGUI:

    fps = 30
    screen_dimension = 600
    piece_dimension = 40

    def __init__(self):
        # Initializy pygame stuff
        pygame.init()
        pygame.display.set_caption("Checkers")
        self.window = pygame.display.set_mode((MainGUI.screen_dimension, MainGUI.screen_dimension))
        self.clock = pygame.time.Clock()

        # Setup the board. 2-d array of Pieces (class). (0,0) is top-left. 0 represents empty.
        self.piecesMap = [[0] * 8 for i in range(8)]
        self.setupPieces();


    def setupPieces(self):
        # Setup the white pieces
        for row in range(0, 3):
            if (row % 2 == 0):
                for col in range(1, 8, 2):
                    self.piecesMap[row][col] = Piece.Piece(row, col, Constants.Constants.Black)
            else:
                for col in range(0, 8, 2):
                    self.piecesMap[row][col] = Piece.Piece(row, col, Constants.Constants.Black)

        # Setup white
        for row in range(5, 8):
            if (row % 2 == 0):
                for col in range(1, 8, 2):
                    self.piecesMap[row][col] = Piece.Piece(row, col, Constants.Constants.White)
            else:
                for col in range(0, 8, 2):
                    self.piecesMap[row][col] = Piece.Piece(row, col, Constants.Constants.White)

    def getCenterPosForBoardSquare(self, xpos: int, ypos: int):
        indexX = 0
        indexY = 0

        jumpX = screen_width // 10
        jumpY = screen_height // 10

        for i in range(0, 10):
            xleft = i * jumpX
            if xleft <= xpos <= xleft + jumpX:
                indexX = i

            yleft = i * jumpY
            if yleft <= ypos <= yleft + jumpY:
                indexY = i

        centerX = (indexX * jumpX) + (jumpX // 2)
        centerY = (indexY * jumpY) + (jumpY // 2)

        return (centerX, centerY)

    def redrawGameWindow(self):
        # Board
        self.window.fill((247, 126, 0))
        self.window.blit(pygame.image.load('GUI/images/board.png'), (55, 55))

        for row in range(0, 8):
            for col in range(0, 8):
                if isinstance(self.piecesMap[row][col], Piece.Piece):
                    currentPiece = self.piecesMap[row][col]
                    (pixelX, pixelY) = currentPiece.getPixelPos()
                    if currentPiece.color == Constants.Constants.Black:
                        self.window.blit(pygame.image.load('GUI/images/blackpiece.png'), (pixelX, pixelY))
                    elif currentPiece.color == Constants.Constants.White:
                        self.window.blit(pygame.image.load('GUI/images/whitepiece.png'), (pixelX, pixelY))


        pygame.display.update()

    def runGame(self):
        drag = False
        run = True
        # Main loop
        while run:
            # fps
            self.clock.tick(MainGUI.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Man skal faktisk trække i tingen
                    if abs(x - pygame.mouse.get_pos()[0]) < 25 and abs(y - pygame.mouse.get_pos()[1]) < 25:
                        drag = True
                if event.type == pygame.MOUSEBUTTONUP:
                    (x, y) = getCenterPosForBoardSquare(x, y)
                    drag = False
                if event.type == pygame.MOUSEMOTION:
                    if drag:
                        (x, y) = pygame.mouse.get_pos()

            self.redrawGameWindow()
        pygame.quit()

