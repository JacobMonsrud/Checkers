import pygame
from GUI import GameGUI, MainMenuGUI
import Constants, Game


class MainGUI:

    def __init__(self):
        # Initializy pygame stuff
        pygame.init()
        pygame.display.set_caption("Checkers")
        self.window = pygame.display.set_mode((Constants.screen_dimension, Constants.screen_dimension))
        self.clock = pygame.time.Clock()


    def runGame(self):

        mainmenu = MainMenuGUI.MainMenuGUI(self.window, self.clock)
        mainmenu.runGame()

