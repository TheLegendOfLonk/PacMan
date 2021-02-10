import pygame as pg
from vectors import Vector2
import settings

#TODO: Cleansing

class Text(object):
    def __init__(self, text, size, color, x, y, show=True):
        self.text = text
        self.size = size
        self.color = color
        self.position = Vector2(x, y)
        self.show = show
        self.font = None
        self.label = None
        self.initFont("PressStart2P-vaV7.ttf")

    def initFont(self, fontPath):
        self.font = pg.font.Font(fontPath, self.size)
    
    def render(self, screen):
        if self.show:
            x, y = self.position.as_tuple()
    
    def update_Score(self, score):
        pass
            