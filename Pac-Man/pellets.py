import pygame as pg
from vectors import Vector2
from settings import *
import map_script

class Pellet(object):
    '''
    Creates a Pellet

    Attributes
    ----------
    name : string
        The name of the pellet
    position : Vector2
        Position of the Pellet
    radius : int
        Pellet collision radius
    points : int
        Point value to score of a single pellet
    show : bool
        Indicates wether the pellet should be visible
    
    Methods
    -------
    render(screen)
        Draws pellet and defines its rendering position
    
    '''
    def __init__(self, x, y):
        self.name = 'Pellet'
        self.position = Vector2(x, y)
        self.radius = 2
        self.points = 10
        #self.color = WHITE
        self.show = True

    def render(self, screen):
        '''
        Draws pellet and defines its rendering position

        Parameters
        ----------
        render(screen)
            Draws the powerpellet and defines its rendering position

        Returns
        -------
        pygame.Surface
        '''
        if self.show:
            pos = self.position.as_int()

            #defines position of pellet as the center of its tile
            pos = (int(pos[0] - TILEWIDTH/2), int(pos[1] - TILEWIDTH/2))
            #pg.draw.circle(screen, self.color, pos, self.radius)
            #pos = (int(pos[0]), int(pos[1]))
            screen.blit(map_script.PELLET, pos)

class Powerpellet(object):
    '''
    Creates a powerpellet

    Attributes
    ----------
    name : string
        The name of the pellet
    position : Vector2
        Position of the powerpellet
    radius : int
        Powerpellets collision radius
    points : int
        Point value to score of a single powerpellet
    timer : int
        Timer for when powerpellet is consumed by Pac-Man
    show : bool
        Indicates wether the powerpellet should be visible
    
    Methods
    -------
    render(screen)
        Draws the powerpellet and defines its rendering position
    '''
    def __init__(self, x, y):
        self.name = "PowerPellet"
        self.position = Vector2(x, y)
        self.radius = 4
        self.points = 50
        #self.color = WHITE
        self.timer = 0
        self.show = True

    def render(self, screen):
        '''
        Draws the pellet and defines its rendering position

        Parameters
        ----------
        screen : pygame.Surface
            The game window

        Returns
        -------
        pygame.Surface
        '''
        if self.show:
            
            #splits vector tuple into two integers
            pos = self.position.as_int()

            #defines position of powerpellet as the center of its tile 
            pos = (int(pos[0] - TILEWIDTH/2), int(pos[1] - TILEWIDTH/2))
            
            #pos = (int(pos[0]+TILEWIDTH/2), int(pos[1]+TILEWIDTH/2))
            #pg.draw.circle(screen, self.color, pos, self.radius)
            screen.blit(map_script.POWER_PELLET, pos)

class AllPellets(object):
    '''
    Puts all pellets in one class object, class that gets called from other scripts

    Attributes
    ----------
    pellet_list : list
        list of all(uneaten) pellets(including powerpellets)
    powerpellets : list
        List of all powerpellets
    pellet_symbols : list
        List of symbols used to indicate 'pellet' in map1.txt
    powerpellet_symbols : list
        List of symbols used to indicate 'powerpellet' in map1.txt
    
    Methods
    -------
    create_pellet_list()
        Appends pellets to appropriate lists
    read_mapfile()
        Extracts symbols from map1.txt

    '''
    
    def __init__(self):
        self.pellet_list = []
        self.powerpellets = []
        self.pellet_symbols = ["p", "n"]
        self.powerpellet_symbols = ["P", "N"]
        self.create_pellet_list()

    def create_pellet_list(self):
        '''
        Appends pellets to appropriate lists
        '''
        grid = self.read_mapfile()
        rows = len(grid)
        cols = len(grid[0])
        
        for row in range(rows):
            for col in range(cols):
                
                #if the symbol from the file is in the pellet_symbols list --> create new Pellet and add it to pellet_list
                if (grid[row][col] in self.pellet_symbols):
                    self.pellet_list.append(Pellet(col*TILEWIDTH + TILEWIDTH/2, row*TILEHEIGHT + TILEWIDTH/2))
                
                #if the symbol from the file is in the powerpellet_symbols list --> create new Powerpellet and add it to pellet_list & powerpellets
                if (grid[row][col] in self.powerpellet_symbols):
                    pp = Powerpellet(col*TILEWIDTH + TILEWIDTH/2, row*TILEHEIGHT + TILEWIDTH/2)
                    self.pellet_list.append(pp)
                    self.powerpellets.append(pp)
                    
    def read_mapfile(self):
        '''
        Extracts symbols from map1.txt
        
        Returns
        -------
        list
            Lists symbols (in order) from map1.txt
        '''
        with open(os.path.join(PATH, "assets", "Map", "map1.txt"), "r") as m:
            lines = [line.rstrip('\n') for line in m]
            return [line.split(' ') for line in lines]
    
    def isEmpty(self):
        '''
        Checks if pellet_list is empty

        Returns
        -------
        bool
            Indicates wether the list is empty
        '''
        if len(self.pellet_list) == 0:
            return True
        return False
    
    def render(self, screen):
        '''
        Calls the appropriate render method of Pellet and Powerpellet for each pellet

        Parameters
        ----------
        screen : pygame.Surface
            The game window
        
        Returns
        -------
        pygame.Surface
        '''
        for pellet in self.pellet_list:
            pellet.render(screen)
    def reset(self):
        self.create_pellet_list()
