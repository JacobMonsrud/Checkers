import pygame
from Gameplay import Game, Constants
from GUI import GameGUI, SelectOpponentGUI
from AI import PvpOpponent, LevelZeroOpponent


class MainMenuGUI:

    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 30, True, False)
    fonttitel = pygame.font.SysFont('Comic Sans MS', 50, True, False)

    centerOfScreen = Constants.screen_dimension // 2

    titel = fonttitel.render('Checkers', False, (0, 0, 0))
    titelX = centerOfScreen - titel.get_width() // 2
    titelY = 50

    pvc = font.render('Player vs Computer', False, (0, 0, 0))
    pvcX = centerOfScreen - pvc.get_width() // 2
    pvcY = 200

    pvp = font.render('Player vs Player', False, (0, 0, 0))
    pvpX = centerOfScreen - pvp.get_width() // 2
    pvpY = 300



    def __init__(self, window, clock):
        self.window = window
        self.clock = clock


    def redrawGameWindow(self):
        #self.window.fill((247, 126, 0))
        self.window.blit(pygame.image.load('GUI/images/bgmenu.png'), (0, 0))

        self.window.blit(self.titel, (self.titelX, self.titelY))

        self.window.blit(self.pvc, (self.pvcX, self.pvcY))

        self.window.blit(self.pvp, (self.pvpX, self.pvpY))

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

                    if self.pvcX <= xPos <= self.pvcX + self.pvc.get_width() and self.pvcY <= yPos <= self.pvcY + self.pvc.get_height():
                        run = False
                        selectGUI = SelectOpponentGUI.SelectOpponentGUI(self.window, self.clock)
                        selectGUI.runGame()

                    elif self.pvpX <= xPos <= self.pvpX + self.pvp.get_width() and self.pvpY <= yPos <= self.pvpY + self.pvp.get_height():
                        run = False
                        # GameGUI
                        opponent = PvpOpponent.PvpOpponent(Constants.Constants.WhitePlayer)
                        game = Game.Game(opponent)
                        gameGUI = GameGUI.GameGUI(self.window, self.clock, game)
                        gameGUI.runGame()

            if run:
                self.redrawGameWindow()
