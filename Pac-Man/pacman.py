import pygame as pg
from pygame.locals import *
from vectors import Vector2
from settings import *
from map_script import _map
import datetime

class Pacman(object):
    def __init__(self):
        self.name = "pacman"
        self.color = YELLOW
        self.position = Vector2(14*16, 27*16-8)
        self.direction = STOP
        self.not_moved = True
        self.remember_direction = None
        self.speed = 100
        self.radius = 10
        self.collision_radius = 3
        #self.start_Position()
        self.lives = 5
        #self.startImage = self.spritesheet.getImage()
        self.animation = None
        self.animation_list = {}
        #self.animations()        
        self.death_animation = False
        self.stop_frame = False
    '''
    Updates Pac-Man player
    '''
    def update(self, deltatime):
        if self.stop_frame:
            return

        self.show = True
        self.position += self.direction*self.speed*deltatime
        self.update_Animations(deltatime)
        
        tile = self.get_tile()
        node = _map.nodes.get((tile[0] + 1, tile[1] + 1), False)
        self.center(tile)
        on_node = False
        if node:
            dif_x = abs((tile[0]) * 16  - (self.position.x - TILEWIDTH / 2))
            dif_y = abs((tile[1]) * 16  - (self.position.y - TILEHEIGHT / 2))
            if dif_x <= 1 and dif_y <= 1:
                on_node = True
            else:
                self.position_check(node, tile)

        direction = self.possible_dirs()
        if self.remember_direction and self.direction.is_parallel(self.remember_direction):
            self.remember_direction = None
        if direction:
            if self.direction == STOP or self.direction.is_parallel(direction):
                if on_node:
                    check = self.node_check(node, direction)
                    if check:
                        self.direction = direction
                        self.keyMove(self.direction)
                elif self.not_moved:
                    if direction == LEFT or direction == RIGHT:
                        self.not_moved = False
                        self.direction = direction
                        self.keyMove(self.direction)
                else:
                    self.direction = direction
                    self.keyMove(self.direction)
            elif on_node:
                check = self.node_check(node, direction)
                if check:
                    self.direction = direction
                    self.keyMove(self.direction)
            elif not self.direction.is_parallel(direction):
                self.remember_direction = direction
        elif on_node:
            if self.remember_direction and self.node_check(node, self.remember_direction):
                direction = self.remember_direction
                self.remember_direction = None
            else:
                direction = self.direction
            check = self.node_check(node, direction)
            if check:
                self.direction = direction
                self.keyMove(self.direction)
            else:
                self.direction = STOP

        else:
            pass

    def node_check(self, node, direction):
        node = _map.node_types.get(node, False)
        if node:
            result = node.check_dir(direction)
            return result
        return False

    def start_Position(self):
        pass
    '''
    Defines all possible movement directions
    '''
    def possible_dirs(self):
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

    def keyMove(self, direction):
        self.direction = direction

    def autoMove(self):
        pass

    def render(self, screen):
        pos = self.position.asInt()
        pg.draw.circle(screen, self.color, pos, self.radius)

    def animations(self):
        pass

    def update_Animations(self, deltatime):
        pass
    
    def get_tile(self):
        x = round((self.position.x - TILEWIDTH / 2) / TILEWIDTH)
        y = round((self.position.y - TILEHEIGHT / 2) / TILEHEIGHT)

        return (x, y)
        
    def eat_pellet(self, pellet_list):
        for pellet in pellet_list:
            d = self.position - pellet.position
            d_squared = d.magnitude_squared()
            r_squared = (self.radius + self.collision_radius)**2
            
            if d_squared <= r_squared:
                return pellet
        return None
    
    def position_check(self, node, tile):
        mid_x, mid_y = tile[0] * TILEWIDTH + TILEWIDTH / 2, tile[1] * TILEHEIGHT + TILEHEIGHT / 2
        node = _map.node_types.get(node, False)
        if not node:
            raise(Exception("Not working node!"))
        if (int(self.position.x) < int(mid_x) and not node.left) or (int(self.position.x) > int(mid_x) and not node.right):
            self.set_to_center(mid_x, mid_y)
        elif (int(self.position.y) < int(mid_y) and not node.up) or (int(self.position.y) > int(mid_y) and not node.down):
            self.set_to_center(mid_x, mid_y)
    
    def set_to_center(self, pos_x, pos_y):
        print("Triggered")
        self.position = Vector2(pos_x, pos_y)
        self.direction = STOP
    
    def center(self, tile):
        if self.direction:
            if self.direction.x != 0:
                self.position.y = int(tile[1] * TILEHEIGHT + TILEHEIGHT / 2)
            if self.direction.y != 0:
                self.position.x = int(tile[0] * TILEWIDTH + TILEWIDTH / 2)
