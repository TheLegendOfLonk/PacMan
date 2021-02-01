import pygame as pg
from pygame.locals import *
from settings import *


class GameController(object):
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.setBackground()
    
    def setBackground(self):
        self.background = pg.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)
    #def startGame(self):
    

    #def update(self):
    
    #def renderAll(self):


if __name__ == "__main__":
    game = GameController()
    #game.startGame()
    while True:
        game.update()
    