import pygame
from Gameplay import Game, Constants
from GUI import GameGUI
from AI import PvpOpponent, LevelZeroOpponent, LevelOneOpponent, LevelTwoOpponent


class SelectOpponentGUI:

    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 30, True, False)
    fonttitel = pygame.font.SysFont('Comic Sans MS', 50, True, False)

    centerOfScreen = Constants.screen_dimension // 2

    titel = fonttitel.render('Checkers', False, (0, 0, 0))
    titelX = centerOfScreen - titel.get_width() // 2
    titelY = 50

    playas = font.render('Play as:', False, (0, 0, 0))
    playasX = centerOfScreen - 55 - playas.get_width() // 2
    playasY = 150

    pieceX = playasX + 130
    pieceY = playasY + 8

    lvl0 = font.render('Level 0', False, (0, 0, 0))
    lvl0X = centerOfScreen - lvl0.get_width() // 2
    lvl0Y = 225

    lvl1 = font.render('Level 1', False, (0, 0, 0))
    lvl1X = centerOfScreen - lvl1.get_width() // 2
    lvl1Y = 300

    lvl2 = font.render('Level 2', False, (0, 0, 0))
    lvl2X = centerOfScreen - lvl2.get_width() // 2
    lvl2Y = 375


    def __init__(self, window, clock):
        self.window = window
        self.clock = clock
        self.playAsPiece = Constants.Constants.BlackPlayer


    def redrawGameWindow(self):
        #self.window.fill((247, 126, 0))
        self.window.blit(pygame.image.load('GUI/images/bgmenu.png'), (0, 0))

        self.window.blit(self.titel, (self.titelX, self.titelY))

        self.window.blit(self.playas, (self.playasX, self.playasY))

        if self.playAsPiece == Constants.Constants.BlackPlayer:
            self.window.blit(pygame.image.load('GUI/images/blackpiece.png'), (self.pieceX, self.pieceY))
        else:
            self.window.blit(pygame.image.load('GUI/images/whitepiece.png'), (self.pieceX, self.pieceY))

        self.window.blit(self.lvl0, (self.lvl0X, self.lvl0Y))

        self.window.blit(self.lvl1, (self.lvl1X, self.lvl1Y))

        self.window.blit(self.lvl2, (self.lvl2X, self.lvl2Y))

        pygame.display.update()


    def runGame(self):

        # Main loop
        run = True
        while run:
            # fps
            self.clock.tick(Constants.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (xPos, yPos) = pygame.mouse.get_pos()
                    if self.pieceX <= xPos <= self.pieceX + 40 and self.pieceY <= yPos <= self.pieceY + 40:
                        if self.playAsPiece == Constants.Constants.BlackPlayer:
                            self.playAsPiece = Constants.Constants.WhitePlayer
                        else:
                            self.playAsPiece = Constants.Constants.BlackPlayer

                    elif self.lvl0X <= xPos <= self.lvl0X + self.lvl0.get_width() and self.lvl0Y <= yPos <= self.lvl0Y + self.lvl0.get_height():
                        run = False
                        if self.playAsPiece == Constants.Constants.BlackPlayer:
                            # Remember to switch, as you choose what you wanna play
                            opponent = LevelZeroOpponent.LevelZeroOpponent(Constants.Constants.WhitePlayer)
                        elif self.playAsPiece == Constants.Constants.WhitePlayer:
                            opponent = LevelZeroOpponent.LevelZeroOpponent(Constants.Constants.BlackPlayer)
                        game = Game.Game(opponent)
                        gameGUI = GameGUI.GameGUI(self.window, self.clock, game)
                        gameGUI.runGame()

                    elif self.lvl1X <= xPos <= self.lvl1X + self.lvl1.get_width() and self.lvl1Y <= yPos <= self.lvl1Y + self.lvl1.get_height():
                        run = False
                        if self.playAsPiece == Constants.Constants.BlackPlayer:
                            # Remember to switch, as you choose what you wanna play
                            opponent = LevelOneOpponent.LevelOneOpponent(Constants.Constants.WhitePlayer)
                        elif self.playAsPiece == Constants.Constants.WhitePlayer:
                            opponent = LevelOneOpponent.LevelOneOpponent(Constants.Constants.BlackPlayer)
                        game = Game.Game(opponent)
                        gameGUI = GameGUI.GameGUI(self.window, self.clock, game)
                        gameGUI.runGame()
                    elif self.lvl2X <= xPos <= self.lvl2X + self.lvl2.get_width() and self.lvl2Y <= yPos <= self.lvl2Y + self.lvl2.get_height():
                        run = False
                        if self.playAsPiece == Constants.Constants.BlackPlayer:
                            # Remember to switch, as you choose what you wanna play
                            opponent = LevelTwoOpponent.LevelTwoOpponent(Constants.Constants.WhitePlayer)
                        elif self.playAsPiece == Constants.Constants.WhitePlayer:
                            opponent = LevelTwoOpponent.LevelTwoOpponent(Constants.Constants.BlackPlayer)
                        game = Game.Game(opponent)
                        gameGUI = GameGUI.GameGUI(self.window, self.clock, game)
                        gameGUI.runGame()

            if run:
                self.redrawGameWindow()
