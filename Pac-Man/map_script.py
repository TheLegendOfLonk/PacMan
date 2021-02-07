'''
Loads all tile assets, creates a two dimensional array
with all sprites and assigns a sprite to each tile
'''
import os
import pygame as pg
import settings
from vectors import Vector2

def tile_load(img):
    '''
    Loads and scales image

    Paramters:
        img: File name of the tile

    Returns:
        The loaded and scaled image
    '''
    return pg.transform.scale(
        pg.image.load(os.path.join(settings.PATH, "assets", "Tiles", img)),
        (settings.TILEWIDTH, settings.TILEHEIGHT))

#define sprites
BLACK_TILE = tile_load("Black.png")
CLOSED_LEFT = tile_load("Cage_Wall_Closed_Left.png")
CLOSED_RIGHT = tile_load("Cage_Wall_Closed_Right.png")
CAGE_CORNER = tile_load("Cage_Wall_Corner.png")
CAGE_DOUBLE = tile_load("Cage_Wall_Double.png")
PELLET = tile_load("Pellet.png")
POWER_PELLET = tile_load("Power_Pellet.png")
CORNER_DOUBLE = tile_load("Wall_Corner_Double.png")
WIDE_LEFT = tile_load("Wall_Corner_Wide_Left.png")
WIDE_RIGHT = tile_load("Wall_Corner_Wide_Right.png")
CORNER = tile_load("Wall_Corner.png")
BIG_CORNER = tile_load("Corner_Big.png")
WALL_DOUBLE = tile_load("Wall_Double.png")
WALL = tile_load("Wall.png")

class Tile():
    '''
    Each tile has its own sprite, which is rotated upon assignment, as well as
    a x and a y coordinate
    '''
    def __init__(self, sprite, rotation, x, y):
        self.sprite = pg.transform.rotate(sprite, rotation)
        self.x = x
        self.y = y



sprite_assign = {
    ".": BLACK_TILE,
    "C": CORNER_DOUBLE,
    "S": WALL_DOUBLE,
    "L": WIDE_LEFT,
    "R": WIDE_RIGHT,
    #"%": PELLET,
    "c": CORNER,
    "s": WALL,
    "w": BIG_CORNER,
    "K": CAGE_CORNER,
    "k": CAGE_DOUBLE,
    "o": CLOSED_RIGHT,
    "O": CLOSED_LEFT,
    "D": BLACK_TILE
}   

class Node():
    def __init__(self, up, left, down, right):
        self.up = bool(up)
        self.left = bool(left)
        self.down = bool(down)
        self.right = bool(right)
        self.directions = {
            1: {
                0: self.right
            },
            0: {
                1: self.down,
                0: False,
                -1: self.up
            },
            -1: {
                0: self.left
            }
            
        }

    def check_dir(self, direction):
        direction = direction.normalize()
        result = self.directions.get(direction.x, False)
        if result:
            result = result.get(direction.y, False)
        return result

class Map():
    '''
    Class containing all map info
    '''
    def __init__(self):
        self.tiles = []
        self.map_init()
        self.nodes = []
        self.node_types = {
            'TL': Node(1, 1, 0, 0),
            'TR': Node(1, 0, 0, 1),
            'LD': Node(0, 1, 1, 0),
            'DR': Node(0, 0, 1, 1),
            'TLD': Node(1, 1, 1, 0),
            'TLR': Node(1, 1, 0, 1),
            'TDR': Node(1, 0, 1, 1),
            'LDR': Node(0, 1, 1, 1),
            'TLDR': Node(1, 1, 1, 1)
        }
        self.set_nodes()
    
    def map_init(self):
        '''
        Generates all tiles
        '''
        with open(os.path.join(settings.PATH, "assets", "Map", "Sprites.txt"), "r") as s_map, \
            open(os.path.join(settings.PATH, "assets", "Map", "Rotations.txt"), "r") as r_map:
            map_lines = s_map.readlines()
            rotation_lines = r_map.readlines()
            for row in range(settings.GRIDROWS):
                row_list = []
                for col in range(settings.GRIDCOLS):
                    char = map_lines[row][col]
                    rotation = int(rotation_lines[row][col]) * 90
                    row_list.append(Tile(
                        sprite_assign.get(char, BLACK_TILE),
                        rotation,
                        col * settings.TILEWIDTH,
                        row * settings.TILEHEIGHT
                    ))
                self.tiles.append(row_list)
    def set_nodes(self):
        # self.nodes = {
        #     (5, 2): 'DR',
        #     (5, 7): 'LDR',
        #     (5, 13): 'LD',
        #     (5, 16): 'DR',
        #     (5, 22): 'LDR',
        #     (5, 27): 'LD',
        #     (9, 2): 'TDR',
        #     (9, 7): 'TLDR',
        #     (9, 10): 'LDR',
        #     (9, 13): 'TLR',
        #     (9, 16): 'TLR',
        #     (9, 19): 'LDR',
        #     (9, 22): 'TLDR',
        #     (9, 27): 'TLD',
        #     (12, 2): 'TR',
        #     (12, 7): 'TLD',
        #     (12, 10): 'TR',
        #     (12, 13): 'LD',
        #     (12, 16): 'DR',
        #     (12, 19): 'TL',
        #     (12, 22): 'TDR',
        #     (12, 27): 'TL',
        #     (15, 10): 'DR',
        #     (15, 13): 'TLR',
        #     (15, 16): 'TLR',
        #     (15, 19): 'LD',
        #     (18, 7): 'TLDR',
        #     (18, 10): 'TLD',
        #     (18, 19): 'TDR',
        #     (18, 22): 'TLDR',
        #     (21, 10): 'TDR',
        #     (21, 19): 'TLD',
        #     (24, 2): 'DR',
        #     (24, 7): 'TLDR',
        #     (24, 10): 'TLR',
        #     (24, 13): 'LD',
        #     (24, 16): 'DR',
        #     (24, 19): 'TLR',
        #     (24, 22): 'TLDR',
        #     (24, 27): 'LD',
        #     (27, 2): 'TR',
        #     (27, 4): 'LD',
        #     (27, 7): 'TDR',
        #     (27, 10): 'LDR',
        #     (27, 13): 'TLR',
        #     (27, 16): 'TLR',
        #     (27, 19): 'LDR',
        #     (27, 22): 'TLD',
        #     (27, 25): 'DR',
        #     (27, 27): 'TL',
        #     (30, 2): 'DR',
        #     (30, 4): 'TLR',
        #     (30, 7): 'TL',
        #     (30, 10): 'TR',
        #     (30, 13): 'LD',
        #     (30, 16): 'DR',
        #     (30, 19): 'TL',
        #     (30, 22): 'TR',
        #     (30, 25): 'TLR',
        #     (30, 27): 'LD',
        #     (33, 2): 'TR',
        #     (33, 13): 'TLR',
        #     (33, 16): 'TLR',
        #     (33, 27): 'TL'
        # }
        self.nodes = {
            (2, 5): 'DR',
            (7, 5): 'LDR',
            (13, 5): 'LD',
            (16, 5): 'DR',
            (22, 5): 'LDR',
            (27, 5): 'LD',
            (2, 9): 'TDR',
            (7, 9): 'TLDR',
            (10, 9): 'LDR',
            (13, 9): 'TLR',
            (16, 9): 'TLR',
            (19, 9): 'LDR',
            (22, 9): 'TLDR',
            (27, 9): 'TLD',
            (2, 12): 'TR',
            (7, 12): 'TLD',
            (10, 12): 'TR',
            (13, 12): 'LD',
            (16, 12): 'DR',
            (19, 12): 'TL',
            (22, 12): 'TDR',
            (27, 12): 'TL',
            (10, 15): 'DR',
            (13, 15): 'TLR',
            (16, 15): 'TLR',
            (19, 15): 'LD',
            (7, 18): 'TLDR',
            (10, 18): 'TLD',
            (19, 18): 'TDR',
            (22, 18): 'TLDR',
            (10, 21): 'TDR',
            (19, 21): 'TLD',
            (2, 24): 'DR',
            (7, 24): 'TLDR',
            (10, 24): 'TLR',
            (13, 24): 'LD',
            (16, 24): 'DR',
            (19, 24): 'TLR',
            (22, 24): 'TLDR',
            (27, 24): 'LD',
            (2, 27): 'TR',
            (4, 27): 'LD',
            (7, 27): 'TDR',
            (10, 27): 'LDR',
            (13, 27): 'TLR',
            (16, 27): 'TLR',
            (19, 27): 'LDR',
            (22, 27): 'TLD',
            (25, 27): 'DR',
            (27, 27): 'TL',
            (2, 30): 'DR',
            (4, 30): 'TLR',
            (7, 30): 'TL',
            (10, 30): 'TR',
            (13, 30): 'LD',
            (16, 30): 'DR',
            (19, 30): 'TL',
            (22, 30): 'TR',
            (25, 30): 'TLR',
            (27, 30): 'LD',
            (2, 33): 'TR',
            (13, 33): 'TLR',
            (16, 33): 'TLR',
            (27, 33): 'TL'
        }
_map = Map()
