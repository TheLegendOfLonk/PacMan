import pygame as pg
from pygame.locals import *
from vectors import Vector2
from settings import *

class Pacman(object):
    def __init__(self):
        self.name = "pacman"
        self.color = YELLOW
        self.position = Vector2(200, 400)
        self.direction = STOP
        self.speed = 100
        self.radius = 10
        #self.start_Position()
        self.lives = 5
        #self.startImage = self.spritesheet.getImage()
        self.animation = None
        self.animations = {}
        #self.animations()        
        self.deathAnimation = False

     
    def update(self, deltatime):
        self.visible = True
        self.position += self.direction*self.speed*deltatime
        self.update_Animations(deltatime)
        direction = self.possibleDirs()
        if direction:
            self.keyMove(direction)
        else:
            self.autoMove()
            #temp
            self.direction = STOP


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
