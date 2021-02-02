import pygame as pg
from pygame.locals import *
from vectors import Vector2
from settings import *

class Pacman(object):
    def __init__(self):
        self.name = "pacman"
        self.color = YELLOW
        self.position = Vector2(14*16, 27*16-8)
        self.direction = STOP
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
        on_grid = True if (round(self.position.x) - 8) % 16 == 0 and \
        (round(self.position.y) - 8) % 16 == 0 else False
        direction = self.possibleDirs()
        if direction:
            if self.direction == STOP or self.direction.is_parallel(direction) or on_grid:
                self.direction = direction
                self.keyMove(self.direction)
            else:
                self.remember_direction = direction
        elif on_grid and self.remember_direction:
            self.direction = self.remember_direction
            self.remember_direction = None
            self.keyMove(self.direction)

        else:
            pass
            #self.autoMove()
            #temp
            #self.direction = STOP


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
