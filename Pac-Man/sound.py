import pygame as pg
from settings import *

pg.mixer.init()
pg.mixer.set_num_channels(8)


def load_sound(name):
    return pg.mixer.Sound(os.path.join(PATH, "assets", "sounds", name))

def load_track(name):
    pg.mixer.music.load(os.path.join(PATH, "assets", "sounds", name))


def background_music(name, volume):
    load_track(name)
    pg.mixer.music.set_volume(volume)
    pg.mixer.music.play(-1)

def play_channel(name, volume, loops, index):
    sound = load_sound(name)
    pg.mixer.Sound.set_volume(sound, volume)
    channel = pg.mixer.Channel(index)
    channel.play(sound, loops)

def play_sound(name, volume, loops):
    sound = load_sound(name)
    pg.mixer.Sound.set_volume(sound, volume)   
    sound.play(loops)
