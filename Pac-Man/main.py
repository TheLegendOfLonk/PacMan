'''
Runs the game
'''
import pygame as pg
from pygame.locals import *
import settings
from map_script import Map
from pacman import Pacman
from pellets import AllPellets
from variables import Variables


class GameController(object):
    '''
    Manages the game

    Attributes
    ----------
    screen : pygame.Surface
        The game window
    background : pygame.Surface
        A black background
    clock : pygame.time.clock
        A clock used to stabilize FPS
    gameover : bool
        Indicates whether a game over has ocurred
    score : int
        Describes the current score
    pellets_eaten : int
        Indicates the amount of eaten pellets
    run : bool
        Changes to false, to stop game execution when player quits the game, in order to prevent a no response error
    pellets : AllPellets
        Initializes an AllPellets class object
    map : Map
        Initializes a Map class object
    pacman : Pacman
        Initializes a Pacman class object
    FRAME_SKIPPED : pygame.USEREVENT
        Defines a skipped frame as a pygame Userevent
    '''

    def __init__(self):
        
        #Initialise all pygame components
        pg.init()
        
        #Set screen and background
        self.screen = pg.display.set_mode(settings.SCREENSIZE, 0, 32)
        self.background = None
        self.set_background()
        self.clock = pg.time.Clock()
        self.gameover = False
        self.score = 0
        self.pellets_eaten = 0
        self.run = True
        self.pellets = AllPellets()
        self.map = Map()
        self.pacman = Pacman(self.map)
        self.set_events()
        
    def set_background(self):
        '''
        Creates a black background

        Attributes
        ----------
        background : pygame.Surface
            creates black brackground with SCREENSIZE dimensions
        
        Returns
        -------
        pygame.Surface
        '''
        self.background = pg.surface.Surface(settings.SCREENSIZE).convert()
        self.background.fill(settings.BLACK)

    def update(self):
        '''
        Main update loop, updates the entire game each frame
        '''
        if not self.gameover:
    
            #time difference between previous and currently rendered picture to make frame
            #length hardware independent
            deltatime = self.clock.tick(settings.FPS) / 1000
            self.pacman.update(deltatime, self.map)
            self.check_pellet_collision()
            self.check_Events()
            self.render()
        else:

            #TODO:end level, background flashes, game over
            pass

    def restart(self):
        pass

    def check_pellet_collision(self):
        '''
        Checks for collisions between Pac-Man and all the pellets on the map

        Attributes
        ----------
        pellet : bool
            when a pellet has been eaten, pacman.py will return pellet as 'True'
        pellet_list : list
            list of all uneaten pellets(including powerpellets)
        '''
        pellet = self.pacman.eat_pellet(self.pellets.pellet_list)
        if pellet:
            self.pellets_eaten += 1

            #stop Pac-Man's movement for 1 frame or 16,67ms when a pellet is eaten
            self.pacman.stop_frame = True
            pg.time.set_timer(self.FRAME_SKIPPED, int(1000 / settings.FPS), True)

            #Increases current score by pellet.points or powerpellet.points amount
            self.score += pellet.points
            self.pellets.pellet_list.remove(pellet)
            print(self.score)

        #checks if the list of all pellets is empty
        if self.pellets.isEmpty():
            self.pacman.show = False
            print("No more pellets")
            #TODO: flash background, reset level, reset Pac-Man(save lives and score)

    def check_Events(self):
        '''
        Checks for pygame events
        '''
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.run = False

            #checks if frame has been skipped and resets the stop_frame boolean if this is the case
            if event.type == self.FRAME_SKIPPED:
                self.pacman.stop_frame = False

    def render(self):
        '''
        Renders all visual elements
        '''

        #renders the map walls
        for row in self.map.tiles:
            for tile in row:
                self.screen.blit(tile.sprite, (tile.x, tile.y))

        self.pellets.render(self.screen)
        #self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        #self.ghosts.render(self.screen)
        #self.text.render(self.screen)
        self.pacman.render_lives(self.screen)
        pg.display.update()

    def death(self):
        '''
        Pac-Man dies
        '''
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
    