'''
Runs the games
'''
import pygame as pg
from pygame.locals import *
import settings
from map_script import _map
from pacman import Pacman
from pellets import AllPellets
from variables import Variables
from UI import UI


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
        self.pellets_eaten = 0
        self.run = True
        self.pellets = AllPellets()
        self.pacman = Pacman()
        self.container = Variables()
        self.interface = UI()
        self.map = _map
        self.set_events()
    
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
            self.check_pellet_collision()
            self.check_Events()
            self.render()
        else:
            #end level, background flashes, game over
            pass
        
    def restart(self):
        pass
    
    def check_pellet_collision(self):
        pellet = self.pacman.eat_pellet(self.pellets.pellet_list)
        if pellet:
            self.pellets_eaten += 1
            self.score += pellet.points
            self.pacman.stop_frame = True
            pg.time.set_timer(self.FRAME_SKIPPED, int(1000 / settings.FPS), True)
            print(self.score)
            self.pellets.pellet_list.remove(pellet)
        if self.pellets.isEmpty():
            self.pacman.show = False
            print("No more pellets")
            

    def check_Events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.run = False
            if event.type == self.FRAME_SKIPPED:
                self.pacman.stop_frame = False
    '''
    Draw all tiles in map_tiles
    '''
    def render(self):
        for row in self.map.tiles:
            for tile in row:
                self.screen.blit(tile.sprite, (tile.x, tile.y))

        self.interface.render(self.screen, self.container)
        self.pellets.render(self.screen)
        #self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        #self.ghosts.render(self.screen)
        #self.text.render(self.screen)
        pg.display.update()

    '''
    Pac-Man dies
    '''
    def death(self):
        if self.pacman.lives == 0:
            self.gameover = True
            self.pacman.show = False
        else:
            self.restart()

    def set_events(self):
        self.FRAME_SKIPPED = pg.USEREVENT

if __name__ == "__main__":
    game = GameController()
    while game.run:
        game.update()
    