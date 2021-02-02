'''
Stores all settings
'''
#path
import os
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
