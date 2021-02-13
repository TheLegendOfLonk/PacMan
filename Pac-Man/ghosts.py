import pygame as pg
from settings import *
from vectors import Vector2
from random import randint
from map_script import sprite_load
import datetime


class Ghost():
    '''
    A class serving as a bluebprint for all ghosts

    Parameters
    ----------
    _map : Map
        The Map class object

    position : Vector2
        The starting position of the ghost

    sprite : pygame.Surface
        The sprite of the ghost

    direction : Vector2
        The starting direction of the ghost

    Attributes
    ----------
    name : string
        The name of the ghost

    position : Vector2
        The current position

    starting_position : Vector2
        The starting position

    speed : float
        The speed in pixels per second

    target : Vector2
        The tile which is the ghosts goal

    mode : int
        Describes the mode the ghost is currently in

    mode : dict
        A dictionary which assigns integers to different mode methods

    directions : list
        a list containing all possible directions

    points : int
        The amount of points the ghost grants upon getting eaten

    direction : Vector2
        The current direction

    banned_nodes : list
        A list containing the coordinates of all nodes, which do not allow the ghost to change
        its direction

    map : Map
        The Map class object

    next_tile : tuple
        A tuple containing the coordinates of the center of the next tile. Each time the ghost
        reaches this tile, it will check whether it's on a node

    sprite : pygame.Surface
        The sprite of the ghost

    dot_countdown : int
        A countdown that releases the ghost upon reaching 0

    waiting : bool
        Indicates whether the ghost is still waiting in the center box

    current_sprite : pygame.Surface
        The current sprite which needs to be rendered

    frightened_sprite : pygame.Surface
        The sprite of a frightened ghost

    radius : int
        Collision radius

    CAGE_ENTRANCE : Vector2
        The entrance of the ghost cage
    
    corner : Vector2
        The tile coordinates of the corner which the ghosts target when in scatter mode

    Methods
    -------
    update(deltatime, pacman)
        Updates location and check if decision must be made

    get_tile(pos)
        Gets the tile of a certain object

    get_current_tile()
        Returns the tile the ghost is currently located on

    determine_path(target)
        Changes the current direction when on a node to which is the best according to the ghost AI

    determine_distance(direction)
        Returns the distance between one possible path and the target

    start_decision()
        Calls a function in dependence of the current mode and gets next tile

    set_next_tile()
        Sets the next tile which the ghost will go to

    passed_next_tile()
        Checks whether next tile was passed, and if yes, calls center

    center(position):
        Changes the position of the ghost to the center of the tile

    render(screen):
        Renders the ghost
    '''
    def __init__(self, _map, position, sprite, direction=UP):
        self.name = "ghost"
        self.position = position
        self.starting_position = position
        self.speed = 80
        self.target = None
        self.mode = 0
        self.modes = {
            0: self.chase, # pylint: disable=no-member
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
        self.dot_countdown = 0
        self.waiting = False
        self.current_sprite = self.sprite
        self.frightened_sprite = sprite_load('blue_ghost1.png', 32, 32, 0)
        self.eaten_sprite = sprite_load('ghosteyes_left.png', 32, 32, 0)
        self.radius = 16
        self.previous_tile = self.get_current_tile().as_tuple()
        self.previous_dir = None
        self.CAGE_ENTRANCE = Vector2(14 * TILEWIDTH, 14.5 * TILEHEIGHT)
        self.releasing = False
        self.corner = None
        #self.animation = None
        #self.animations = {}
    def update(self, deltatime, pacman):
        '''
        Updates location and check if decision must be made

        Parameters
        ----------
        deltatime : float
            Changes with different FPS, so that all movement is independent of FPS
        pacman : Pacman
            A Pacman class object
        '''
        if self.direction != self.previous_dir:
            self.previous_dir = self.direction
            return
        self.position += self.direction * self.speed * deltatime
        self.previous_dir = self.direction
        #Check whether passed a node
        if self.passed_next_tile():
            self.start_decision()
        if self.map.teleport_check(self):
            self.set_next_tile()
        

    def get_tile(self, pos):
        '''
        Gets the tile of a certain object

        Parameter
        ---------
        pos : Vector2
            Position of the object
        
        Retruns
        -------
        Vector2
            A vector containing the tile
        '''
        x = pos.x
        y = pos.y
        x = round((x - TILEWIDTH / 2) / TILEWIDTH)
        y = round((y - TILEHEIGHT / 2) / TILEHEIGHT)

        return Vector2(x, y)
        
    def get_current_tile(self):
        '''
        Returns the tile the ghost is currently located on

        Returns
        -------
        tuple
            A tuple containing the x and y cordinate of the tile
        '''
        x = self.position.x
        y = self.position.y
        x = round((x - TILEWIDTH / 2) / TILEWIDTH)
        y = round((y - TILEHEIGHT / 2) / TILEHEIGHT)

        return Vector2(x, y)

    def determine_path(self, target):
        '''
        Changes the current direction when on a node to which is the best according to the ghost AI

        Parameters
        ----------
        target : Vector2
            The tile the target is located on
        '''
        self.target = target
        results = self.get_directions()
        min_distance = min(results.values())
        for key, value in results.items():
            if value <= min_distance:
                self.direction = key
                return
    
    def get_directions(self):
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
        return results
                
    def determine_distance(self, direction):
        '''
        Returns the distance between one possible path and the target

        Parameters
        ----------
        direction : Vector2
            The direction of the path
        
        Returns
        -------
        float:
            The distance between the target and the path
        '''
        vector = self.target - (self.get_current_tile() + direction)
        return vector.magnitude()
    
    def start_decision(self):
        '''
        Calls a function in dependence of the current mode and gets next tile
        '''
        if self.releasing:
            self.release() # pylint: disable=no-member
            self.set_next_tile()
        elif self.waiting:
            self.reverse()
        else:
            func = self.modes.get(self.mode, False)
            func()
            self.set_next_tile()
    
    def set_next_tile(self):
        '''
        Sets the next tile which the ghost will go to
        '''
        if self.next_tile:
            self.previous_tile = self.next_tile
        else:
            self.previous_tile = self.get_current_tile().as_tuple()
        x, y = (self.get_current_tile() + self.direction).as_tuple()
        self.next_tile = (round(x), round(y))

    def passed_next_tile(self):
        '''
        Checks whether next tile was passed, and if yes, calls center

        Returns
        -------
        bool
            True if next tile was passed
        '''
        coordinates = Vector2(self.next_tile[0] * TILEWIDTH + TILEWIDTH / 2,
                              self.next_tile[1] * TILEHEIGHT + TILEHEIGHT / 2)
        if self.direction.x < 0 and self.position.x < coordinates.x or \
            self.direction.x > 0 and self.position.x > coordinates.x:
            if not self.waiting:
                self.center(coordinates)
            return True
        elif self.direction.y < 0 and self.position.y < coordinates.y or \
            self.direction.y > 0 and self.position.y > coordinates.y:
            if not self.waiting:
                self.center(coordinates)
            return True
        return False

    def center(self, position):
        '''
        Changes the position of the ghost to the center of the tile
        '''
        self.position = position
    
    def render(self, screen):
        '''
        Renders the ghost

        Parameters
        ----------
        screen : pygame.Surface
            The surface on which the ghost should be rendered
        '''
        screen.blit(self.current_sprite, (self.position.x - TILEWIDTH, self.position.y - TILEWIDTH))
        #pg.draw.circle(screen, WHITE, (self.position.x, self.position.y), 15)
    def reverse(self):
        if self.releasing:
            return
        self.direction *= -1
        container = self.previous_tile
        self.previous_tile = self.next_tile
        self.next_tile = container

    def collision_check(self, pacman):
        if (self.position - pacman.position).magnitude() <= self.radius:
            if self.mode == 2:
                self.current_sprite = self.eaten_sprite
                self.mode = 3
            elif self.mode < 2:
                print("Death lul")

    def scatter(self):
        self.determine_path(self.corner)

    def frightened(self):
        results = list(self.get_directions().keys())
        random = randint(0, len(results) - 1)
        self.direction = results[random]

    def eaten(self):
        pass

    def start_release(self):
        self.releasing = True
        self.speed = 40

    def release(self):
        self.direction = self.release_order[0]
        
class Blinky(Ghost):
    def __init__(self, _map, pacman):
        sprite = sprite_load('blinky_left1.png', 32, 32, 0)
        super().__init__(_map, Vector2(14 * TILEWIDTH, 14.5 * TILEHEIGHT), sprite, direction=LEFT)
        self.pacman = pacman
        self.corner = Vector2(25, -1)
        self.set_next_tile()

    def chase(self):
        target = self.get_tile(self.pacman.position)
        self.determine_path(target)

class Pinky(Ghost):
    def __init__(self, _map, pacman):
        sprite = sprite_load('pinky_left1.png', 32, 32, 0)
        super().__init__(_map, Vector2(14 * TILEWIDTH, 16.5 * TILEHEIGHT), sprite, direction=DOWN)
        self.pacman = pacman
        self.corner = Vector2(27, 34)
        self.waiting = True
        self.start_release()
        self.set_next_tile()
        self.release_order = [UP]
        
    def chase(self):
        target = self.get_tile(self.pacman.position) + self.pacman.direction * 4
        if self.pacman.direction == UP:
            target += Vector2(4, 0)
        self.determine_path(target)
    
    def release(self):
        super().release()
        if self.position.y < self.CAGE_ENTRANCE.y:
            self.direction = LEFT
            self.waiting = False
            self.releasing = False
            self.speed = 80


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
            Pinky(_map, pacman),
            #Inky(_map, pacman),
            #Clyde(_map, pacman)
        ]
        self.frightened_timer = None
        self.chase_timer = None
        self.chase_time = None
        self.chase_time_list = [10, 10, 10, 10, 10]
        self.set_chase_timer(self.chase_time_list[0])
        self.chase_time_list.pop(0)
        self.current_mode = 1
        self.chase_only = False
        for ghost in self:
            ghost.mode = self.current_mode
    
    def __iter__(self):
        return iter(self.ghosts)
    
    def update(self, deltatime, pacman):
        if self.frightened_timer and (datetime.datetime.now() - self.frightened_timer).seconds >= 8:
            self.pp_over()
            self.frightened_timer = None
        if not self.frightened_timer and \
            (datetime.datetime.now() - self.chase_timer).seconds >= self.chase_time \
            and (not self.chase_only or self.current_mode == 1):
            self.current_mode = 1 - self.current_mode
            for ghost in self:
                if ghost.mode < 2:
                    ghost.mode = self.current_mode
                    ghost.reverse()
                    print("Activated mode", self.current_mode)
            if len(self.chase_time_list) > 0:
                self.set_chase_timer(self.chase_time_list[0])
                self.chase_time_list.pop(0)
            else:
                self.chase_only = True

        for ghost in self:
            ghost.update(deltatime, pacman)
    def render(self, screen):
        for ghost in self:
            ghost.render(screen)
    def check_events(self, pacman):
        for ghost in self:
            ghost.collision_check(pacman)
    def power_pellet(self):
        if self.chase_timer and not self.frightened_timer:
            self.chase_time -= (datetime.datetime.now() - self.chase_timer).seconds
            print("Remaining:", self.chase_time)
        self.frightened_timer = datetime.datetime.now()
        for ghost in self:
            if ghost.mode < 2:
                ghost.reverse()
                ghost.mode = 2
                ghost.speed = 60
                ghost.current_sprite = ghost.frightened_sprite
    def pp_over(self):
        self.set_chase_timer(self.chase_time)
        for ghost in self:
            if ghost.mode < 3:
                ghost.mode = self.current_mode
                ghost.speed = 80
                ghost.current_sprite = ghost.sprite
    def set_chase_timer(self, time):
        self.chase_timer = datetime.datetime.now()
        self.chase_time = time

#TODO: Cruising Elroy