import os
import settings
import pygame as pg
from pacman import Pacman

def sprite_load(img, scale_x, scale_y, rotate):
    return pg.transform.rotate(pg.transform.scale(
        pg.image.load(os.path.join(settings.PATH, "assets", "Sprites", img)),
        (scale_x, scale_y)), rotate) 

class UI():
    def __init__(self):
        self.life = sprite_load('Life.png', 32, 32, 0)
    
    def draw_lives(self, screen, container):
        for i in range(container.get_lives()):
            x_pos = (2 + 2 * i) * settings.TILEWIDTH
            y_pos = 34 * settings.TILEHEIGHT
            screen.blit(self.life, (x_pos, y_pos))
    def render(self, screen, container):
        self.draw_lives(screen, container)