import pygame
import Game
from GUI import GameGUI
import Constants

class MainMenuGUI:

    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 30, True, False)

    centerOfScreen = Constants.screen_dimension // 2

    pvc = font.render('Player vs Computer', False, (0, 0, 0))
    pvcX = centerOfScreen - pvc.get_width() // 2
    pvcY = 150

    pvp = font.render('Player vs Player', False, (0, 0, 0))
    pvpX = centerOfScreen - pvp.get_width() // 2
    pvpY = 250


    def __init__(self, window, clock):
        self.window = window
        self.clock = clock


    def redrawGameWindow(self):
        # Board
        self.window.fill((247, 126, 0))

        self.window.blit(self.pvc, (self.pvcX, self.pvcY))

        self.window.blit(self.pvp, (self.pvpX, self.pvpY))

        pygame.display.update()


    def runGame(self):

        # Main loop
        stop = False
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
                        pass

                    elif self.pvpX <= xPos <= self.pvpX + self.pvp.get_width() and self.pvpY <= yPos <= self.pvpY + self.pvp.get_height():
                        run = False
                        # GameGUI
                        game = Game.Game()
                        gameGUI = GameGUI.GameGUI(self.window, self.clock, game)
                        gameGUI.runGame()
                        stop = True

            if not stop:
                self.redrawGameWindow()
