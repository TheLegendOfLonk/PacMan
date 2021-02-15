import pygame as pg
from settings import *
from map_script import sprite_load
from vectors import Vector2
from map_script import sprite_load
import random
class Fruit():
    def __init__(self, _map, fruit_type="cherry"):
        self.position = Vector2(13.5*TILEWIDTH, 20*TILEHEIGHT)
        self.timer = 0
        self.display_length = random.randint(15,40)
        self.sprite = None
        self.delete = False
        self.set_fruit_type(fruit_type)

    def update(self, deltatime):
        self.timer += deltatime
        if self.timer >= self.display_length:
            self.delete = True

    def set_fruit_type(self, fruit_type):
        if fruit_type == "cherry":
            self.sprite = sprite_load('cherry_fruit.png', 32,32,0)
            self.points = 100
        elif fruit_type == "strawberry":
            self.sprite = sprite_load('strawberry_fruit.png', 32,32,0)
            self.points = 300
        elif fruit_type == "orange":
            self.sprite = sprite_load('orange_fruit.png', 32,32,0)
            self.points = 500
        elif fruit_type == "apple":
            self.sprite = sprite_load('apple_fruit.png', 32,32,0)
            self.points = 700
        elif fruit_type == "melon":
            self.sprite = sprite_load('melon_fruit.png', 32,32,0)
            self.points = 1000
        elif fruit_type == "galaxian":
            self.sprite = sprite_load('galaxian_boss.png', 32,32,0)
            self.points = 2000
        elif fruit_type == "bell":
            self.sprite = sprite_load('bellthingy.png', 32,32,0)
            self.points = 3000
        elif fruit_type == "key":
            self.sprite = sprite_load('key.png', 32,32,0)
            self.points = 5000
    
    def render(self, screen):
        screen.blit(self.sprite, (self.position.x - TILEWIDTH/2, self.position.y - TILEHEIGHT/2))
    
