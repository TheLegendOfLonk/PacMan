'''
Runs the games
'''
import pygame as pg
from pygame.locals import *
import settings
from map_script import _map
from pacman import Pacman


class GameController(object):
    '''
    Manages the game
    '''
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(settings.SCREENSIZE, 0, 32)
        self.background = None
        self.set_background()
        self.clock = pg.time.Clock()
        self.gameover = False
        self.score = 0
        self.run = True

        self.pacman = Pacman()
        self.map = _map

        

    def set_background(self):
        '''
        Creates a black background
        '''
        self.background = pg.surface.Surface(settings.SCREENSIZE).convert()
        self.background.fill(settings.BLACK)

    def update(self):
        if not self.gameover:
            deltatime = self.clock.tick(settings.FPS) / 1000
            self.pacman.update(deltatime)
            self.check_Events()
            self.render()
    
    def check_Events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.run = False
    '''
    Draw all tiles in map_tiles
    '''
    def render(self):
        for row in self.map.tiles:
            for tile in row:
                self.screen.blit(tile.sprite, (tile.x, tile.y))
        
        #self.pellets.render(self.screen)
        #self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        #self.ghosts.render(self.screen)
        #self.text.render(self.screen)
        pg.display.update()
        

    #for event in pg.event.get():
       # if event.type == pg.QUIT:
            #run = False

if __name__ == "__main__":
    game = GameController()
    while game.run:
        game.update()
    