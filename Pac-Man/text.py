import pygame as pg
from vectors import Vector2
from settings import *
import os

#TODO: Cleansing

class Text(object):
    def __init__(self, text, size, color, x, y, show=True):
        self.text = text
        self.size = size
        self.color = color
        self.position = Vector2(x, y)
        self.show = show
        self.font = None
        self.textbox = None
        self.totalTime = 0
        self.display_length = 0
        self.init_text()
        self.create_textbox()

    def init_text(self):
        path = os.path.join(PATH, "assets", "PressStart2P-vaV7.ttf")
        self.font = pg.font.Font(path, self.size)
        
    def create_textbox(self):    
        self.textbox = self.font.render(self.text, 1, self.color)
        
    def update(self, deltatime):
        pass      

    def set_text(self, insert_text_here):
        self.text = insert_text_here
        self.create_textbox()
    
    def render(self, screen):
        if self.show:
            x, y = self.position.as_tuple()
            screen.blit(self.textbox, (x, y))


class AllText():
    def __init__(self):
        self.text_list = {}
        self.all_text()
        self.temp_text = []

    def all_text(self):
        self.text_list["score_str"] = Text("SCORE", TILEHEIGHT-1, WHITE, 0, 0+5)
        self.text_list["score_int"] = Text("0".zfill(2), TILEHEIGHT-1, WHITE, 0, TILEHEIGHT+5)
        self.text_list["highscore_str"] = Text("HIGH SCORE", TILEHEIGHT-1, WHITE, TILEWIDTH*9.8, 0+5)
        self.text_list["highscore_int"] = Text("0".zfill(5), TILEHEIGHT-1, WHITE, TILEWIDTH*11.7, TILEHEIGHT+5)
        self.text_list["ready"] = Text("READY!",12, YELLOW, 12*TILEWIDTH, 20*TILEHEIGHT, True)
        self.text_list["gameover"] = Text("GAME  OVER!",12, RED, 10*TILEWIDTH, 20*TILEHEIGHT, False)

    def update(self, deltatime):
        if len(self.temp_text) > 0:
            temp_text = []
            for text in self.temp_text:
                text.update(deltatime)
                if text.show:
                    temp_text.append(text)
            self.temp_text = temp_text
    
    def update_score(self, score):
        self.text_list["score_int"].set_text(str(score).zfill(2))

    def stop_showing_ready(self):
        self.text_list["ready"].show = False

    def show_gameover(self):
        self.text_list["gameover"].show = True

    def add_temp_text(self, number, position):
        #x, y = position.as_tuple(
        #text = Text(str(number), 10, WHITE, x, y)
        #text.display_length = 1
        #self.temp_text.append(text)
        pass
    
    def render(self, screen):
        for key in self.text_list.keys():
            self.text_list[key].render(screen)
        
        for item in self.temp_text:
            item.render(screen)
