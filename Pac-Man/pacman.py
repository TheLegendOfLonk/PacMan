'''
Contains the Pacman class
'''
import pygame as pg
from pygame.locals import *
from vectors import Vector2
from settings import *
from animation import Animation

class Pacman():
    '''
    Pacman himself

    Parameters
    ----------
    _map : Map
        The Map class object of the game manager

    Attributes
    ----------
    name : string
        Name of the object
    color : tuple
        Tuple of the RGB-value
    position : Vector2
        Pac-Man's position on the board
    direction : Vector2
        Current direction
    not_moved : bool
        True if pacman has not moved yet
    gameover : bool
        Indicates whether a game over has ocurred
    remember_direction : Vector2
        Saved value for when on next node
    speed : int
        Movement speed in pixels per second
    radius : float
        Size of pacman radius
    collision_radius : float
        Pellet eating range
    lives : int
        Amount of remaining lives
    life_sprite : pygame.Surface
        The sprite of pacman's lives
    stop_frame : bool
        True when pacman rests for a frame when eating a pellet
    show : bool
        Indicates whether pacman is visible

    Methods
    -------
    update(deltatime, _map)
        Updates the position of pacman, checks whether he is on a node and manage direction changes
    move_on_node(node, direction, _map)
        Checks if node accepts a certain direction and assign it
    node_check(node, direction, _map)
        Checks if it allows a certain direction
    possible_dirs()
        Checks whether key was pressed and returns appropriate Vector2
    assign_direction(direction)
        Changes the direction to the desired direction
    render(screen)
        TEMPORARY: Draws a circle on pacman's position
    get_tile()
        Returns the tile pacman is currently located on
    eat_pellet(pellet_list)
        Calculate distance to all pellets and return if within eating radius
    position_check(node, tile, _map)
        Fixes unwanted behaviour
    set_to_center(pos_x, pos_y)
        Sets position to center of tile and stops pacman
    center(tile)
        Adjusts the pacman location
    live_lost(screen)
        Decreases amount of lives by one and returns the current number to detect a Game Over
    render_lives(screen)
        Renders pacman's lives
    '''

    # pylint: disable=too-many-instance-attributes

    def __init__(self, _map):
        self.name = "pacman"
        self.color = YELLOW
        self.position = Vector2(14*16, 27*16-8)
        self.direction = STOP
        self.not_moved = True
        self.remember_direction = None
        self.speed = 80
        self.radius = 10
        self.collision_radius = 3
        #TODO: self.start_Position()
        self.lives = 5
        self.life_sprite = _map.sprites.get('life')
        #self.startImage = self.spritesheet.getImage()
        self.sprite = _map.sprites.get('pacman_closed')
        self.animation = None
        self.animation_list = {}
        self.define_animations()
        self.death_animation = False
        self.stop_frame = False
        self.show = True

    def update(self, deltatime, _map):
        '''
        Updates the position of pacman, checks whether he is on a node and manage direction changes

        Parameters
        ----------
        deltatime : float
            Changes with different FPS, so that all movement is independent of FPS
        _map : Map
            The Map object for sprites and tiles
        '''
        if self.stop_frame:
            return

        #Move to the faced direction
        self.position += self.direction*self.speed*deltatime
        #TODO: self.update_animations(deltatime)

        #Get the current tile pacman is on
        tile = self.get_tile()

        #TODO: change so that nodes are read from file
        node = _map.nodes.get((tile.x + 1, tile.y + 1), False)

        #Center the position of pacman to prevent errors
        self.center(tile)

        #Check if pacman is at the center of a node tile, to allow changing directions
        on_node_center = False
        if node:
            dif_x = abs((tile.x) * 16  - (self.position.x - TILEWIDTH / 2))
            dif_y = abs((tile.y) * 16  - (self.position.y - TILEHEIGHT / 2))
            if dif_x <= 1 and dif_y <= 1:
                on_node_center = True
            else:
                #Prevent pacman from going through walls which happens when pacman moved too fast
                self.position_check(node, tile, _map)

        #Determine next direction
        direction = self.possible_dirs()

        #Reset remember_direction if the vector is parallel to direction vector, in order to
        #prevent 'jumping back' when hitting a wall
        if self.remember_direction and self.direction.is_parallel(self.remember_direction):
            self.remember_direction = None

        #Execute if a new direction is defined
        if direction:

            #Execute if pacman stands still or the desired direction is parallel to current
            #This allows to reverse direction
            if self.direction == STOP or self.direction.is_parallel(direction):

                #Allow change of direction if on the center of a node tile
                if on_node_center:

                    #Check if node allows movement to desired direction
                    self.move_on_node(node, direction, _map)

                #Else check if pacman moves for first time
                elif self.not_moved:

                    #Allow only movements to the left or right
                    if direction in (RIGHT, LEFT):
                        self.not_moved = False
                        self.assign_direction(direction)

                #Otherwise, allow movement, as going to the reverse direction is always allowed when
                #not on the center of a node
                else:
                    self.assign_direction(direction)

            #As the desired action is not reversing, change direction only if on the
            #center of a node and if the node allows the direction
            elif on_node_center:
                self.move_on_node(node, direction, _map)

            #Otherwise, remember the desired direction, in order to change direction when
            #pacman reaches a node
            else:
                self.remember_direction = direction

        #Execute if on center of a node, but no desired direction given
        elif on_node_center:

            #Determine whether previous input was given and is suitable
            if self.remember_direction and self.node_check(node, self.remember_direction, _map):
                self.assign_direction(self.remember_direction)
                self.remember_direction = None

            #Otherwise, continue with same direction, if possible
            else:
                direction = self.direction
                if not self.move_on_node(node, direction, _map):
                    self.direction = STOP
        
        _map.teleport_check(self)

    def move_on_node(self, node, direction, _map):
        '''
        Calls the node_check function to check,
        whether the node accepts the desired direction, and if yes,
        calls the assign_direction function, which sets the new direction

        Parameters
        ----------
        node : string
            A string containing all possible directions
        direction : Vector2
            The desired direction
        _map : Map
            The Map class object which contains all nodes and all node types

        Returns
        -------
        bool
            Indicates, whether direction was changed
        '''
        check = self.node_check(node, direction, _map)
        if check:
            self.assign_direction(direction)
        return check

    def node_check(self, node, direction, _map):
        '''
        Converts the node string to a Node class object and checks if it allows a certain direction

        Parameters
        ----------
        node : string
            A string containing all possible directions
        direction : Vector2
            The desired direction
        _map : Map
            The Map class object which contains all nodes and all node types

        Returns
        -------
        bool
            Indicates, whether direction was changed
        '''
        node = _map.node_types.get(node, False)
        if node:
            result = node.check_dir(direction)
            return result
        return False

    def possible_dirs(self):
        '''
        Checks whether key was pressed and returns appropriate Vector2

        Return
        ------
        Vector2
            A Vector2 object representing the desired direction
        '''
        key_pressed = pg.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        return None

    def assign_direction(self, direction):
        '''
        Changes the direction to the desired direction

        Parameters
        ----------
        direction : Vector2
            The desired direction
        '''
        self.direction = direction

    def render(self, screen):
        '''
        TEMPORARY: Draws a circle on pacman's position
        '''
        pos = self.position.as_int()
        pg.draw.circle(screen, self.color, pos, self.radius)
        #TODO: add Pacman animation and sprite

    def get_tile(self):
        '''
        Returns the tile pacman is currently located on

        Returns
        -------
        tuple
            A tuple containing the x and y cordinate of the tile
        '''
        x = round((self.position.x - TILEWIDTH / 2) / TILEWIDTH)
        y = round((self.position.y - TILEHEIGHT / 2) / TILEHEIGHT)

        return Vector2(x, y)

    def eat_pellet(self, pellet_list):
        '''
        Calculate distance to all pellets and return if within eating radius

        Parameters
        ----------
        pellet_list : list
            A list containing all pellets

        Returns
        -------
        Pellet
            The Pellet which is in eating range, returns none if there are no pellets in range
        '''
        for pellet in pellet_list:
            d = self.position - pellet.position
            d_squared = d.magnitude_squared()
            r_squared = (self.radius + self.collision_radius)**2

            if d_squared <= r_squared:
                return pellet
        return None

    def position_check(self, node, tile, _map):
        '''
        Checks for unwanted pacman behaviour. Sometimes nodes are not detected properly.
        Each time moves out of the predestined grid, the set_to_center gets called and
        sets pacman back to the center of the tile

        Parameters
        ----------
        node : string
            A string containing all possible directions
        tile : Vector2
            The tile on which pacman currently stands
        _map : Map
            The Map class object which contains all nodes and all node types
        '''
        mid_x = tile.x * TILEWIDTH + TILEWIDTH / 2
        mid_y = tile.y * TILEHEIGHT + TILEHEIGHT / 2
        node = _map.node_types.get(node, False)
        if not node:
            raise Exception("Node not working!")
        if (int(self.position.x) < int(mid_x) and not node.left) or \
           (int(self.position.x) > int(mid_x) and not node.right):
            self.set_to_center(mid_x, mid_y)
        elif (int(self.position.y) < int(mid_y) and not node.up) or \
             (int(self.position.y) > (mid_y) and not node.down):
            self.set_to_center(mid_x, mid_y)

    def set_to_center(self, pos_x, pos_y):
        '''
        Sets position to center of tile and stops pacman. Used when pacman leaves his boundries

        Parameters
        ----------
        pos_x : float
            The x-position of tile center
        pos_y : float
            The y-position of tile center
        '''
        self.position = Vector2(pos_x, pos_y)
        self.direction = STOP

    def center(self, tile):
        '''
        Adjusts the pacman location. When moving horizontally, adjusts vertical position to
        fit in the grid, and vice versa

        Parameters
        ----------
        tile : Vector2
            The current tile position
        '''
        if self.direction:
            if self.direction.x != 0:
                self.position.y = int(tile.y * TILEHEIGHT + TILEHEIGHT / 2)
            if self.direction.y != 0:
                self.position.x = int(tile.x * TILEWIDTH + TILEWIDTH / 2)

    def define_animations(self):
        anim = Animation("looping")
        anim.fps = 30
        anim.add_frame('pacman_closed.png', 0, False)
        anim.add_frame('pacman_open1.png', 0, False)
        anim.add_frame('pacman_open2.png', 0, False)
        anim.add_frame('pacman_open1.png', 0, False)
        self.animation_list["right"] = anim


        anim = Animation("looping")
        anim.fps = 30
        anim.add_frame('pacman_open1.png', 0, True)

    def update_animations(self, deltatime):
        if self.direction == LEFT:
            self.animation = self.animation_list["left"]
        elif self.direction == RIGHT:
            self.animation = self.animation_list["right"]
        self.sprite = self.animation.update(deltatime)

    def live_lost(self, screen):
        '''
        Decreases amount of lives by one and returns the current number to detect a Game Over

        Parameters
        ----------
        screen : pygame.Surface
            The game window
        '''
        self.lives -= 1
        self.animation = self.animation_list["death"]
        self.death_animation = True

        #TODO:call death animation

    def render_lives(self, screen):
        '''
        Renders Pac-Man player lives at the bottom left of the screen

        Parameters
        ----------
        screen : pygame.Surface
            The game window
        '''
        for i in range(self.lives - 1):
            x = (2 + 2 * i) * TILEWIDTH
            y = 34 * TILEHEIGHT
            screen.blit(self.life_sprite, (x, y))
