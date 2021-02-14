import pygame as pg
from settings import *


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
    return channel


def play_sound(name, volume, loops):
    sound = load_sound(name)
    pg.mixer.Sound.set_volume(sound, volume)   
    sound.play(loops)

def stop(channel):
    channel.stop()

def reset():
    pg.mixer.quit()

def start():
    pg.mixer.init()
    pg.mixer.set_num_channels(8)


