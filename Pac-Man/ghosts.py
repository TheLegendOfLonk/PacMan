import pygame as pg
from settings import *
from vectors import Vector2
from random import randint
from map_script import sprite_load
import datetime
from animation import Animation


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

    pellet_countdown : int
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
        self.pellet_countdown = 0
        self.waiting = False
        self.current_sprite = self.sprite
        #self.frightened_sprite = sprite_load('blue_ghost1.png', 32, 32, 0)
        #self.eaten_sprite = sprite_load('ghosteyes_left.png', 32, 32, 0)
        self.radius = 16
        self.previous_tile = self.get_current_tile().as_tuple()
        self.previous_dir = None
        self.CAGE_ENTRANCE = Vector2(14 * TILEWIDTH, 14.5 * TILEHEIGHT)
        self.releasing = False
        self.corner = None
        self.leaving = False
        self.entering = False
        self.animation = None
        self.previous_anim = None
        self.animations = {}
        self.define_animations()
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

        self.update_animations(deltatime)
        

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
        if self.entering:
            self.enter()
        elif self.releasing:
            self.release() # pylint: disable=no-member
        elif self.waiting:
            if self.direction == DOWN:
                self.direction = UP
                self.next_tile = (self.get_current_tile().x, 16.5)
                self.previous_tile = (self.get_current_tile().x, 17.5)
            else:
                self.direction = DOWN
                self.next_tile = (self.get_current_tile().x, 17.5)
                self.previous_tile = (self.get_current_tile().x, 15.5)
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
            if not self.waiting and not self.releasing:
                self.center(coordinates)
            return True
        elif self.direction.y < 0 and self.position.y < coordinates.y or \
            self.direction.y > 0 and self.position.y > coordinates.y:
            if not self.waiting and not self.releasing:
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
        self.test = self.current_sprite
        
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
                #self.current_sprite = self.eaten_sprite
                self.mode = 3
                self.speed = 160
                return self.mode
            elif self.mode < 2:
                print("Death lul")

    def scatter(self):
        self.determine_path(self.corner)

    def frightened(self):
        self.target = self.get_current_tile()
        results = list(self.get_directions().keys())
        random = randint(0, len(results) - 1)
        self.direction = results[random]

    def start_release(self):
        self.releasing = True
        self.waiting = False
        self.speed = 40

    def release(self):
        pass
    
    def eaten(self):
        target = Vector2(14, 14.5)
        self.determine_path(target)

    def enter(self):
        pass

    def define_animations(self):
        directions = ['up', 'left', 'down', 'right']
        for _dir in directions:
            anim = Animation('looping', _dir)
            anim.fps = 10
            if _dir == 'right':
                anim.add_frame(f"{self.name}_left1.png", 0, True)
                anim.add_frame(f"{self.name}_left2.png", 0, True)
            else:
                anim.add_frame(f"{self.name}_{_dir}1.png", 0, False)
                anim.add_frame(f"{self.name}_{_dir}2.png", 0, False)

            self.animations[anim.name] = anim

            anim.fps = 10
            anim = Animation('frozen', 'eyes_' + _dir)
            anim.add_frame('ghost_eyes_' + _dir + '.png', 0, False)

            self.animations[anim.name] = anim

        anim = Animation('looping', 'frightened')
        anim.fps = 10
        anim.add_frame('blue_ghost1.png', 0, False)
        anim.add_frame('ghost_frightened2.png', 0, False)
        self.animations[anim.name] = anim

        anim = Animation('looping', 'frightened_flash')
        anim.fps = 10
        anim.add_frame('ghost_frightened_flash1.png', 0, False)
        anim.add_frame('ghost_frightened_flash2.png', 0 , False)
        self.animations[anim.name] = anim
    
    def update_animations(self, deltatime):
        if self.mode < 2:
            if self.direction >= LEFT:
                self.animation = self.animations["left"]
            elif self.direction >= RIGHT:
                self.animation = self.animations["right"]
            elif self.direction >= UP:
                self.animation = self.animations["up"]
            elif self.direction >= DOWN:
                self.animation = self.animations["down"]

        elif self.mode == 2:
            self.animation = self.animations['frightened']
        
        elif self.mode == 3:
            if self.direction >= LEFT:
                self.animation = self.animations["eyes_left"]
            elif self.direction >= RIGHT:
                self.animation = self.animations["eyes_right"]
            elif self.direction >= UP:
                self.animation = self.animations["eyes_up"]
            elif self.direction >= DOWN:
                self.animation = self.animations["eyes_down"]
        if not self.previous_anim:
            self.previous_anim = self.animation
        if self.animation.name != self.previous_anim.name:
            for direction, anim in self.animations.items():
                anim.reset()
        self.previous_anim = self.animation
        self.current_sprite = self.animation.update(deltatime, next_frame=True)


class Blinky(Ghost):
    def __init__(self, _map, pacman, all_ghosts):
        self.ghosts = all_ghosts
        self.name = 'blinky'
        sprite = sprite_load('blinky_left1.png', 32, 32, 0)
        super().__init__(_map, Vector2(14 * TILEWIDTH, 14.5 * TILEHEIGHT), sprite, direction=LEFT)
        self.pacman = pacman
        self.corner = Vector2(25, -1)
        self.set_next_tile()
        self.release_order = [UP]

    def chase(self):
        target = self.get_tile(self.pacman.position)
        self.determine_path(target)
    
    def eaten(self):
        if (self.position - self.CAGE_ENTRANCE).magnitude() - 8 > 0.2:
            super().eaten()
        else:
            self.entering = True
            self.releasing = True
            self.position = self.CAGE_ENTRANCE
            self.enter()
    
    def enter(self):
        self.direction = DOWN#self.release_order[-1] * -1
        if self.position.y > 17.5 * TILEHEIGHT:
            self.entering = False
            self.mode = self.ghosts.current_mode
            self.speed = 40
    
    def release(self):
        self.direction = self.release_order[0]
        if self.position.y < self.CAGE_ENTRANCE.y:
            self.direction = LEFT
            self.waiting = False
            self.releasing = False
            if self.mode < 2:
                self.speed = 80
            else:
                self.speed = 60
        self.set_next_tile()



class Pinky(Ghost):
    def __init__(self, _map, pacman, all_ghosts):
        self.ghosts = all_ghosts
        self.name = 'pinky'
        sprite = sprite_load('pinky_left1.png', 32, 32, 0)
        super().__init__(_map, Vector2(14 * TILEWIDTH, 17.5 * TILEHEIGHT), sprite, direction=DOWN)
        self.pacman = pacman
        self.corner = Vector2(3, -1)
        self.waiting = True
        self.release_order = [UP]
        self.next_tile = (self.get_current_tile().x, 17.5)
        
    def chase(self):
        target = self.get_tile(self.pacman.position) + self.pacman.direction * 4
        if self.pacman.direction == UP:
            target += Vector2(4, 0)
        self.determine_path(target)
    
    def release(self):
        self.direction = self.release_order[0]
        if self.position.y < self.CAGE_ENTRANCE.y:
            self.direction = LEFT
            self.waiting = False
            self.releasing = False
            if self.mode < 2:
                self.speed = 80
            else:
                self.speed = 60
        self.set_next_tile()
    
    def eaten(self):
        if (self.position - self.CAGE_ENTRANCE).magnitude() - 8 > 0.2:
            super().eaten()
        else:
            self.entering = True
            self.releasing = True
            self.position = self.CAGE_ENTRANCE
            self.enter()
    
    def enter(self):
        self.direction = DOWN#self.release_order[-1] * -1
        if self.position.y > 17.5 * TILEHEIGHT:
            self.entering = False
            self.mode = self.ghosts.current_mode
            self.speed = 40


class Inky(Ghost):
    def __init__(self, _map, pacman, blinky, all_ghosts):
        self.ghosts = all_ghosts
        self.name = 'inky'
        sprite = sprite_load('inky_left1.png', 32, 32, 0)
        super().__init__(_map, Vector2(12 * TILEWIDTH, 17.5 * TILEHEIGHT), sprite, direction=UP)
        self.pacman = pacman
        self.waiting = True
        self.corner = Vector2(27, 34)
        self.blinky = blinky
        self.next_tile = (self.get_current_tile().x, 16.5)
        self.leaving = False
        self.release_order = [RIGHT, UP]
        self.RELEASE_ORDER = [RIGHT, UP]
        

    def release(self):
        if (self.starting_position - self.position).magnitude() <= 1 or self.leaving:
            if not self.leaving:
                self.position = self.starting_position
                self.next_tile = (13.5, self.get_current_tile().y)
                self.leaving = True
                self.direction = self.release_order[0]
            else:
                self.direction = self.release_order[0]
                self.set_next_tile()

            if len(self.release_order) > 1:
                self.release_order.pop(0)
        else:
            if self.direction == DOWN:
                self.direction = UP
                self.next_tile = (self.get_current_tile().x, 16.5)
                self.previous_tile = (self.get_current_tile().x, 17.5)
            else:
                self.direction = DOWN
                self.next_tile = (self.get_current_tile().x, 17.5)
                self.previous_tile = (self.get_current_tile().x, 15.5)
            self.set_next_tile()

        if self.position.y < self.CAGE_ENTRANCE.y:
            self.direction = LEFT
            self.waiting = False
            self.releasing = False
            if self.mode < 2:
                self.speed = 80
            else:
                self.speed = 60
            self.leaving = False
            self.position = self.CAGE_ENTRANCE
            self.release_order = self.RELEASE_ORDER
            self.set_next_tile()
        
    
    def chase(self):
        blinky_pos = self.blinky.get_current_tile()
        vec1 = self.get_tile(self.pacman.position) + self.pacman.direction *  2
        vec2 = (vec1 - blinky_pos) * 2
        target = blinky_pos + vec2

        if self.pacman.direction == UP:
            target += Vector2(2, 0)
        self.determine_path(target)
    
    def eaten(self):
        if (self.position - self.CAGE_ENTRANCE).magnitude() - 8 > 0.2:
            super().eaten()
        else:
            self.entering = True
            self.releasing = True
            self.position = self.CAGE_ENTRANCE
            self.enter()
    
    def enter(self):
        self.direction = DOWN#self.release_order[-1] * -1
        if self.position.y > 17.5 * TILEHEIGHT:
            self.direction = RIGHT#self.release_order[-2] * -1
            if self.position.x < self.starting_position.x:
                self.position = self.starting_position
                self.next_tile = (13.5, self.get_current_tile().y)
                self.leaving = True
                self.direction = self.release_order[0]
                self.release_order.pop(0)
                self.entering = False
                self.mode = self.ghosts.current_mode
                self.speed = 40

class Clyde(Ghost):
    def __init__(self, _map, pacman, all_ghosts):
        self.ghosts = all_ghosts
        self.name = 'clyde'
        sprite = sprite_load('clyde_left1.png', 32, 32, 0)
        super().__init__(_map, Vector2(16 * TILEWIDTH, 17.5 * TILEHEIGHT), sprite, direction=UP)
        self.pacman = pacman
        self.leaving = False
        self.waiting = True
        self.corner = Vector2(0, 34)
        self.next_tile = (self.get_current_tile().x, 16.5)
        self.release_order = [LEFT, UP]
        self.RELEASE_ORDER = [LEFT, UP]

    def chase(self):
        target = self.get_tile(self.pacman.position)
        if (target - self.get_current_tile()).magnitude() < 8:
            target = self.corner
        self.determine_path(target)

    def release(self):
        if (self.starting_position - self.position).magnitude() <= 1 or self.leaving:
            if not self.leaving:
                self.position = self.starting_position
                self.next_tile = (13.5, self.get_current_tile().y)
                self.leaving = True
                self.direction = self.release_order[0]
            else:
                self.direction = self.release_order[0]
                self.set_next_tile()

            if len(self.release_order) > 1:
                self.release_order.pop(0)
        else:
            if self.direction == DOWN:
                self.direction = UP
                self.next_tile = (self.get_current_tile().x, 16.5)
                self.previous_tile = (self.get_current_tile().x, 17.5)
            else:
                self.direction = DOWN
                self.next_tile = (self.get_current_tile().x, 17.5)
                self.previous_tile = (self.get_current_tile().x, 15.5)
            self.set_next_tile()

        if self.position.y < self.CAGE_ENTRANCE.y:
            self.direction = LEFT
            self.waiting = False
            self.releasing = False
            if self.mode < 2:
                self.speed = 80
            else:
                self.speed = 60
            self.leaving = False
            self.position = self.CAGE_ENTRANCE
            self.release_order = self.RELEASE_ORDER
            self.set_next_tile()

    def eaten(self):
        if (self.position - self.CAGE_ENTRANCE).magnitude() - 8 > 0.2:
            super().eaten()
        else:
            self.entering = True
            self.releasing = True
            self.position = self.CAGE_ENTRANCE
            self.enter()
    
    def enter(self):
        self.direction = DOWN #self.release_order[-1] * -1
        if self.position.y > 17.5 * TILEHEIGHT:
            self.direction = RIGHT#self.release_order[-2] * -1
            if self.position.x > self.starting_position.x:
                self.position = self.starting_position
                self.next_tile = (13.5, self.get_current_tile().y)
                self.leaving = True
                self.direction = self.release_order[0]
                self.release_order.pop(0)
                self.entering = False
                self.mode = self.ghosts.current_mode
                self.speed = 40

class AllGhosts():
    def __init__(self, _map, pacman):
        self.pacman = pacman
        self.blinky = Blinky(_map, pacman, self)
        self.pinky = Pinky(_map, pacman, self)
        self.inky = Inky(_map, pacman, self.blinky, self)
        self.clyde = Clyde(_map, pacman, self)
        self.ghosts = [
            self.blinky,
            self.pinky,
            self.inky,
            self.clyde
        ]
        
        self.frightened_timer = None
        self.chase_timer = None
        self.chase_time = None
        self.chase_time_list = [10, 10, 10, 10, 10]
        self.set_chase_timer(self.chase_time_list[0]) # --------------------------------------
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
                    if not ghost.waiting:
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

    def check_events(self, pacman, pellets_eaten, release_after_pellets):
        ret = False
        if len(release_after_pellets) > 0 and release_after_pellets[0] <= pellets_eaten:
            self.release_next()
            ret = True
        for ghost in self:
            if ghost.collision_check(pacman) == 3:
                if all(ghost.mode == 3 for ghost in self):
                    self.pp_over()
                    self.frightened_timer = None

        return ret
    
    def power_pellet(self):
        if self.chase_timer and not self.frightened_timer:
            self.chase_time -= (datetime.datetime.now() - self.chase_timer).seconds
            print("Remaining:", self.chase_time)
        self.frightened_timer = datetime.datetime.now()
        for ghost in self:
            if ghost.mode < 2 and not ghost.releasing:
                ghost.reverse()
                ghost.mode = 2
                ghost.speed = 60
                #ghost.current_sprite = ghost.frightened_sprite
            elif ghost.releasing:
                ghost.mode = 2
                #ghost.current_sprite = ghost.frightened_sprite
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
    
    def release_next(self):
        for ghost in self:
            if ghost.waiting and not ghost.releasing:
                ghost.start_release()
                return

#TODO: Cruising Elroy
