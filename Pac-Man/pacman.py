import pygame as pg
from pygame.locals import *
from vectors import Vector2
from settings import *
from map_script import _map

class Pacman(object):
    def __init__(self):
        self.name = "pacman"
        self.color = YELLOW
        self.position = Vector2(14*16, 27*16-8)
        self.direction = STOP
        self.not_moved = True
        self.remember_direction = None
        self.speed = 80
        self.radius = 10
        #self.start_Position()
        self.lives = 5
        #self.startImage = self.spritesheet.getImage()
        self.animation = None
        self.animation_list = {}
        #self.animations()        
        self.deathAnimation = False

     
    def update(self, deltatime):
        self.visible = True
        self.position += self.direction*self.speed*deltatime
        self.update_Animations(deltatime)
        
        tile = self.get_tile()
        node = _map.nodes.get(tile, False)
        on_node = False
        if node:
            dif_x = abs((tile[0] - 1) * 16  - (self.position.x - TILEWIDTH / 2))
            dif_y = abs((tile[1] - 1) * 16  - (self.position.y - TILEHEIGHT / 2))
            if dif_x <= 1 and dif_y <= 1:
                on_node = True

        direction = self.possibleDirs()
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
            #self.autoMove()
            #temp
            #self.direction = STOP

    def node_check(self, node, direction):
        node = _map.node_types.get(node, False)
        if node:
            result = node.check_dir(direction)
            return result
        return False

    def start_Position(self):
        pass

    def possibleDirs(self):
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
        # I KNOW IT'S WRONG!!!
        return (x + 1,y + 1)
