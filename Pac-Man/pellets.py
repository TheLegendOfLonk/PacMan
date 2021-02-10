import pygame as pg
from vectors import Vector2
from settings import *
import map_script

class Pellet(object):
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.radius = 2
        self.points = 10
        self.color = WHITE
        self.show = True

    def render(self, screen):
        pos = self.position.as_int()
        pos = (int(pos[0] - TILEWIDTH/2), int(pos[1] - TILEWIDTH/2))
        #pg.draw.circle(screen, self.color, pos, self.radius)
        #pos = (int(pos[0]), int(pos[1]))
        screen.blit(map_script.PELLET, pos)

class Powerpellet(object):
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.radius = 4
        self.points = 50
        self.show = True
        self.color = WHITE
        self.timer = 0
        self.show = True

    def render(self, screen):
        if self.show:
            pos = self.position.as_int()
            pos = (int(pos[0] - TILEWIDTH/2), int(pos[1] - TILEWIDTH/2))
            #pos = (int(pos[0]+TILEWIDTH/2), int(pos[1]+TILEWIDTH/2))
            #pg.draw.circle(screen, self.color, pos, self.radius)
            screen.blit(map_script.POWER_PELLET, pos)

class AllPellets(object):
    def __init__(self):
        self.pellet_list = []
        self.powerpellets = []
        self.pellet_symbols = ["p", "n"]
        self.powerpellet_symbols = ["P", "N"]
        self.create_pellet_list()

    def create_pellet_list(self):
        grid = self.read_mazefile()
        rows = len(grid)
        cols = len(grid[0])
        for row in range(rows):
            for col in range(cols):
                if (grid[row][col] in self.pellet_symbols):
                    self.pellet_list.append(Pellet(col*TILEWIDTH + TILEWIDTH/2, row*TILEHEIGHT+ TILEWIDTH/2))
                if (grid[row][col] in self.powerpellet_symbols):
                    pp = Powerpellet(col*TILEWIDTH + TILEWIDTH/2, row*TILEHEIGHT + TILEWIDTH/2)
                    self.pellet_list.append(pp)
                    self.powerpellets.append(pp)
                    
    def read_mazefile(self):
        with open(os.path.join(PATH, "assets", "Map", "map1.txt"), "r") as m:
            lines = [line.rstrip('\n') for line in m]
            return [line.split(' ') for line in lines]
    
    def isEmpty(self):
        if len(self.pellet_list) == 0:
            return True
        return False
    
    def render(self, screen):
        for pellet in self.pellet_list:
            pellet.render(screen)

