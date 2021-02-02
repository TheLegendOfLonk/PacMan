'''
Runs the games
'''
import pygame as pg
import settings
import load_tiles
pg.font.init()

class GameController(object):
    '''
    Manages the game
    '''
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(settings.SCREENSIZE, 0, 32)
        self.background = None
        self.set_background()
        self.map_tiles = load_tiles.map_init()
        self.draw_tiles()

    def set_background(self):
        '''
        Creates a black background
        '''
        self.background = pg.surface.Surface(settings.SCREENSIZE).convert()
        self.background.fill(settings.BLACK)

    #def start_game(self):

    def draw_tiles(self):
        '''
        Draw all tiles in map_tiles
        '''
        for row in self.map_tiles:
            for tile in row:
                self.screen.blit(tile.sprite, (tile.x, tile.y))

    #def update(self):

    #def renderAll(self):

def main():
    '''
    Runs the game
    '''
    game = GameController()

    #define clock which stabilizes FPS
    clock = pg.time.Clock()

    run = True
    #game.startGame()
    while run:
        #game.update()

        #stabilize FPS
        clock.tick(settings.FPS)

        #adopt display changes
        pg.display.update()

        #quit if game closed
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

if __name__ == "__main__":
    main()
    