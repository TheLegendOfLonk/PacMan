import pygame as pg 
from pygame.locals import * # pylint: disable=unused-import
from settings import * # pylint: disable=unused-import
import load_tiles
pg.font.init()

class GameController(object):
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.setBackground()
    
    def setBackground(self):
        self.background = pg.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)
        self.map_tiles = load_tiles.map_init()
        self.drawTiles()

    def startGame(self):
        pass

    def drawTiles(self):
        for row in self.map_tiles:
            for tile in row:
                self.screen.blit(tile.sprite, (tile.x, tile.y))
    #def update(self):
    
    #def renderAll(self):


if __name__ == "__main__":
    game = GameController()
    clock = pg.time.Clock()
    FPS = 60
    #game.startGame()
    while True:
        #game.update()
        clock.tick(FPS)
        pg.display.update()
    