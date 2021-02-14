'''
Stores all settings
'''
#path
import os

from vectors import Vector2

PATH = os.path.abspath(__file__)[:-12]

#screen settings
TILEWIDTH = 16
TILEHEIGHT = 16
GRIDROWS = 36
GRIDCOLS = 28
SWIDTH = GRIDCOLS*TILEWIDTH
SHEIGHT = GRIDROWS*TILEHEIGHT
SCREENSIZE = (SWIDTH, SHEIGHT)
FPS = 60

#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 100, 150)
TEAL = (100, 255, 255)
ORANGE = (230, 190, 40)
TRANSPARENT = (255, 0, 255)

#vectors
UP = Vector2(0, -1)
DOWN = Vector2(0, 1)
LEFT = Vector2(-1, 0)
RIGHT = Vector2(1, 0)
STOP = Vector2()
