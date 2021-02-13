import pygame as pg
from settings import *
import os

class Animation():
    def __init__(self, anim_type):
        self.anim_type = anim_type
        self.current_frame = 0
        self.sprites = []
        self.deltatime = 0
        self.complete = False
        self.fps = 0

    def add_frame(self, sprite, rotation, flip):
        if flip:
            self.sprites.append(pg.transform.flip(pg.image.load(
            os.path.join(PATH, "assets", "Sprites", sprite)), flip, False))
        else:
            self.sprites.append(pg.transform.rotate(pg.image.load(
            os.path.join(PATH, "assets", "Sprites", sprite)), rotation))
    
    def update(self, deltatime):
        if self.anim_type == "looping":
            
            self.deltatime += deltatime
            if self.deltatime >= (1.0 / self.fps):
                self.current_frame += 1
                self.deltatime = 0
            
            if self.current_frame == len(self.sprites):
                self.current_frame = 0
        
        elif self.anim_type == "singular":
            if not self.complete:
                self.deltatime += deltatime
                
                if self.deltatime >= (1.0 / self.fps):
                    self.current_frame += 1
                    self.deltatime = 0
                
                if self.current_frame == len(self.sprites) - 1:
                    self.complete = True
            
        elif self.anim_type == "frozen":
            self.current_frame = 0
        
        return self.sprites[self.current_frame]
    
    def reset(self):
        self.current_frame = 0
        self.complete = False

    
        


    
