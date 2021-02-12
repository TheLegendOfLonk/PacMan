import pygame as pg
from settings import *
from vectors import Vector2
from random import randint
from map_script import sprite_load


class Ghost():
    def __init__(self, _map, position, sprite, direction=UP):
        self.name = "ghost"
        self.position = position
        self.speed = 80
        self.tile = _map
        self.target = Vector2()
        self.mode = 0
        self.mode_timer = 0
        self.modes = {
            0: self.chase,
            1: self.scatter,
            2: self.frightened,
            3: self.eaten
        }
        self.directions = [UP, LEFT, DOWN, RIGHT]
        self.points = 200
        self.direction = direction
        self.banned_nodes = [
            (13, 27),
            (16, 27),
            (13, 15),
            (16, 15)
        ]
        self.map = _map
        self.next_tile = None
        self.sprite = sprite
        #self.animation = None
        #self.animations = {}
    def update(self, deltatime, pacman):
        self.position += self.direction * self.speed * deltatime
        if self.passed_next_tile():
            self.start_decision()
    
    def get_tile(self, pos=None):
        x = pos.x
        y = pos.y
        x = round((x - TILEWIDTH / 2) / TILEWIDTH)
        y = round((y - TILEHEIGHT / 2) / TILEHEIGHT)

        return Vector2(x, y)
        
    def get_current_tile(self,):
        '''
        Returns the tile the ghost is currently located on

        Returns
        -------
        tuple
            A tuple containing the x and y cordinate of the tile
        '''
        x = self.position.x
        y = self.position.y
        x = round((x - TILEWIDTH) / TILEWIDTH)
        y = round((y - TILEHEIGHT) / TILEHEIGHT)

        return Vector2(x, y)

    def determine_path(self, target):
        self.target = target
        results = dict()
        tile = self.get_current_tile()
        node = self.map.nodes.get((tile.x + 1, tile.y + 1), False)
        if node:
            node = self.map.node_types.get(node, False)
            for direction in self.directions:
                allow = not (direction == UP and (tile.x + 1, tile.y + 1) in self.banned_nodes) \
                    and node.check_dir(direction) and ((self.direction * -1).as_int() != direction.as_int())
                if allow:
                    results[direction] = self.determine_distance(direction)
            if len(results) == 0:
                results[self.direction] = 1
            print(e[0] for e in results.items())
            print(e[1] for e in results.items())
            min_distance = min(results.values())
            for key, value in results.items():
                if value <= min_distance:
                    self.direction = key
                    return
    
    def determine_distance(self, direction):
        vector = self.target - (self.get_current_tile() + direction)
        return vector.magnitude()
    
    def start_decision(self):
        func = self.modes.get(self.mode, False)
        func()
        self.get_next_tile()

    def chase(self):
        pass
    
    def scatter(self):
        pass

    def frightened(self):
        pass

    def eaten(self):
        pass

    def get_next_tile(self):
        x, y = (self.get_current_tile() + self.direction).as_int()
        self.next_tile = (x, y)

    def passed_next_tile(self):
        coordinates = Vector2(self.next_tile[0] * TILEWIDTH + TILEWIDTH,
                              self.next_tile[1] * TILEHEIGHT + TILEHEIGHT)
        if self.direction.x < 0 and self.position.x < coordinates.x or \
            self.direction.x > 0 and self.position.x > coordinates.x:
            self.center(coordinates)
            return True
        elif self.direction.y < 0 and self.position.y < coordinates.y or \
            self.direction.y > 0 and self.position.y > coordinates.y:
            self.center(coordinates)
            return True
        return False

    def center(self, position):
        self.position = position
    
    def render(self, screen):
        screen.blit(self.sprite, (self.position.x - 1.5 * TILEWIDTH, self.position.y - 1.5 * TILEWIDTH))
        pg.draw.circle(screen, WHITE, (self.next_tile[0] * TILEWIDTH + TILEWIDTH / 2,self.next_tile[1] * TILEHEIGHT + TILEWIDTH / 2), 10)
    
        
class Blinky(Ghost):
    def __init__(self, _map, pacman):
        sprite = sprite_load('blinky_left1.png', 32, 32, 0)
        super().__init__(_map, Vector2(14.25 * TILEWIDTH, 15 * TILEHEIGHT), sprite, direction=LEFT)
        self.pacman = pacman
        self.get_next_tile()

    def chase(self):
        target = self.get_tile(self.pacman.position)
        self.determine_path(target)

class Pinky(Ghost):
    def __init__(self, _map, pacman):
        super().__init__(_map, Vector2(14.5, 15), direction=DOWN)
        self.pacman = pacman
        self.sprite = self.map.sprite_load('pinky_left1.png') 

class Inky(Ghost):
    def __init__(self, _map, pacman):
        super().__init__(_map, Vector2(14.5, 15), direction=UP)
        self.pacman = pacman
        self.sprite = self.map.sprite_load('inky_left1.png') 

class Clyde(Ghost):
    def __init__(self, _map, pacman):
        super().__init__(_map, Vector2(14.5, 15), direction=UP)
        self.pacman = pacman
        self.sprite = self.map.sprite_load('clyde_left1.png') 

class AllGhosts():
    def __init__(self, _map, pacman):
        self.pacman = pacman
        self.ghosts = [
            Blinky(_map, pacman),
            #Pinky(_map, pacman),
            #Inky(_map, pacman),
            #Clyde(_map, pacman)
        ]
    
    def __iter__(self):
        return iter(self.ghosts)
    
    def update(self, deltatime, pacman):
        for ghost in self:
            ghost.update(deltatime, pacman)
    
    def render(self, screen):
        for ghost in self:
            ghost.render(screen)

