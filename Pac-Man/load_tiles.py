'''
Loads all tile assets, creates a two dimensional array
with all sprites and assigns a sprite to each tile
'''
import os
import pygame as pg
import settings

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
CORNER_DOUBLE = tile_load("Wall_Corner_Double.png")
WIDE_LEFT = tile_load("Wall_Corner_Wide_Left.png")
WIDE_RIGHT = tile_load("Wall_Corner_Wide_Right.png")
CORNER = tile_load("Wall_Corner.png")
BIG_CORNER = tile_load("Corner_Big.png")
WALL_DOUBLE = tile_load("Wall_Double.png")
WALL = tile_load("Wall.png")

class Tile():
    '''
    Each tile has an own sprite, which is rotated upon assignment,
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
    "%": PELLET,
    "c": CORNER,
    "s": WALL,
    "w": BIG_CORNER,
    "K": CAGE_CORNER,
    "k": CAGE_DOUBLE,
    "o": CLOSED_RIGHT,
    "O": CLOSED_LEFT,
    "D": BLACK_TILE
}

def map_init():
    '''
    Generates all tiles
    '''
    map_tiles = []
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
            map_tiles.append(row_list)
    return map_tiles
