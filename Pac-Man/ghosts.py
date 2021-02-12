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
        
    def get_current_tile(self, pos=None):
        '''
        Returns the tile the ghost is currently located on

        Returns
        -------
        tuple
            A tuple containing the x and y cordinate of the tile
        '''
        if pos:
            x = pos.x
            y = pos.y
        else:
            x = self.position.x
            y = self.position.y
        x = round((x - TILEWIDTH / 2) / TILEWIDTH)
        y = round((y - TILEHEIGHT / 2) / TILEHEIGHT)

        return Vector2(x, y)

    def determine_path(self, target):
        self.target = target
        results = dict()
        tile = self.get_current_tile()
        node = self.map.nodes.get(tile, False)
        if node:
            node = self.map.node_types.get(node, False)
            for direction in self.directions:
                allow = (direction == UP and tile in self.banned_nodes) \
                    and node.check_dir(direction) and (self.direction)
                results[direction] = self.determine_distance(direction) if allow else -1
            new_results = dict(filter(lambda elem: elem[0] >= 0, results.items()))
            min_distance = min(new_results.values())
            for key, value in new_results.items():
                if value <= min_distance:
                    self.direction = key
                    return
    
    def determine_distance(self, direction):
        vector = self.target - (self.position + direction)
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
        if self.direction.x != 0:
            x = round(self.position.x - TILEWIDTH / 2) // TILEWIDTH
            x = x + 1 if self.direction.x > 0 else x
            y = round(self.position.y - TILEHEIGHT / 2) // TILEHEIGHT
        else:
            x = round(self.position.x - TILEWIDTH / 2) // TILEWIDTH
            y = round(self.position.y - TILEHEIGHT / 2) // TILEHEIGHT
            y = y + 1 if self.direction.y > 0 else y
        self.next_tile = (x, y)

    def passed_next_tile(self):
        coordinates = Vector2(self.next_tile[0] * TILEWIDTH + TILEWIDTH / 2,
                              self.next_tile[1] * TILEHEIGHT + TILEHEIGHT / 2)
        if self.direction.x - (self.position - coordinates).normalize().x < 0.01:
            self.center(coordinates)
            return True
        elif self.direction.y - (self.position - coordinates).normalize().y < 0.01:
            self.center(coordinates)
            return True
        return False

    def center(self, position):
        self.position = position
    
    def render(self, screen):
        screen.blit(self.sprite, (self.position.x - TILEWIDTH, self.position.y - TILEWIDTH))
        pg.draw.circle(screen, WHITE, self.next_tile, 3)
    
        
class Blinky(Ghost):
    def __init__(self, _map, pacman):
        sprite = sprite_load('blinky_left1.png', 32, 32, 0)
        super().__init__(_map, Vector2(14 * TILEWIDTH, 14.5 * TILEHEIGHT), sprite, direction=LEFT)
        self.pacman = pacman
        self.get_next_tile()

    def chase(self):
        target = self.get_current_tile(self.pacman.position)
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

