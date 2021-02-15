'''
Runs the game
'''
import pygame as pg
from pygame.locals import *
from settings import *
import sound
from map_script import Map
from pacman import Pacman
from pellets import AllPellets
from variables import Variables
from ghosts import AllGhosts
from text import AllText
from fruit import Fruit


class GameController(object):
    '''
    Manages the game

    Attributes
    ----------
    screen : pygame.Surface
        The game window
    background : pygame.Surface
        A black background
    clock : pygame.time.clock
        A clock used to stabilize FPS
    gameover : bool
        Indicates whether a game over has ocurred
    score : int
        Describes the current score
    pellets_eaten : int
        Indicates the amount of eaten pellets
    run : bool
        Changes to false, to stop game execution when player quits the game, in order to prevent a no response error
    pellets : AllPellets
        Initializes an AllPellets class object
    map : Map
        Initializes a Map class object
    pacman : Pacman
        Initializes a Pacman class object
    level : int
        Defines the current level
    
    Methods
    -------
    set_background()
        Creates a black background window
    update()
        Updates the entire game each frame
    reset()
        Resets the level(Map, Pellets, Pac-Man)
    check_pellet_collision()
        Checks for collisions between Pac-Man and pellets
    check_Events()
        Checks for specific pygame events
    death()
        Handels Pac-Man's death
    set_events()
        Defines pygame events
    render()
        Renders all elements of the game every update cycle
    '''

    def __init__(self):
        
        #Initialise all pygame components
        pg.init()
        sound.start()
        #Set screen and background
        self.screen = pg.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.set_background()
        self.clock = pg.time.Clock()
        self.gameover = False
        self.score = 0
        self.timer = 0.0
        self.waiting = False
        self.death = False
        self.highscore = 0
        self.rend = True
        self.pellets_eaten = 0
        self.run = True
        self.pellets = AllPellets()
        self.map = Map()
        self.text = AllText()
        self.pacman = Pacman(self.map)
        self.ghosts = AllGhosts(self.map, self.pacman)
        self.fruit = Fruit(self.map)
        self.level = 1
        self.PP_over = pg.USEREVENT
        self.release_after_pellets = [0, 30, 60]
        self.pp_sound = None
        self.start_game()
        self.cruising = 60
        
        sound.background_music('siren_1.wav', 0.2)
       
    def load_highscore(self):
        '''
        Load highscore from highscore.text
        '''
        with open(os.path.join(PATH, "highscore.txt"), "r") as f:
            try:
                self.highscore = int(f.read())
                print(self.highscore)
                self.text.update_highscore(self.highscore)
            except:
                self.highscore = 0
                print('text')
    
    def save_highscore(self):
        '''
        Save highscore in highscore.txt
        '''
        path = os.path.join(PATH, "highscore.txt")
        with open(path) as f: 
            lines = f.readlines() #read 
        #modify 
        lines[0] = str(self.highscore)
 
        with open(path, "w") as f: 
            try:
                f.writelines(lines) #write back
            except:
                self.highscore = 0
                print("Couldn't save highscore")   
 
    def set_background(self):
        '''
        Creates a black background

        Returns
        -------
        pygame.Surface
        '''
        self.background = pg.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)   
        
    def start_game(self):
        self.waiting = True
        self.load_highscore()
        self.update()
        sound.play_sound('game_start.wav', 0.3, 0)
        pg.time.wait(5000)
        self.waiting = False
        self.text.stop_showing_ready()
        

    def update(self):
        '''
        Main update loop, updates the entire game each frame
        '''

        #time difference between previous and currently rendered picture to make frame
        #length hardware independent
        
        if not self.waiting:
            deltatime = self.clock.tick(FPS) / 1000
            
            if deltatime > 0.020:
                deltatime = 0.020
        
        else:
           
            if self.rend:
                self.pacman.update_animations(1 / FPS)
                self.render()
                
                if self.pacman.reset:
                    sound.play_sound('death_2.wav', 0.3, 0)
                    pg.time.wait(200)
                    sound.play_sound('death_2.wav', 0.3, 0)
                    pg.time.wait(200)
                    self.pacman.show = False
                    
                    if not self.gameover:
                        self.reset()
                    else:
                        sound.reset()
            return
        
        self.pacman.update(deltatime, self.map)
        self.check_pellet_collision()
        self.check_Events()
        self.check_fruit_events(deltatime)
        self.ghosts.update(deltatime, self.pacman, self.pp_sound)
        self.set_highscore()
        self.text.update_score(self.score, self.highscore)
        ghost_events = self.ghosts.check_events(self.pacman,self.pellets_eaten, self.release_after_pellets, self.pp_sound)
        
        if self.cruising and self.pellets_eaten >= self.cruising:
            self.ghosts.cruising()
            self.cruising = False
        
        if ghost_events == 3:
            self.release_after_pellets.pop(0)
        
        elif ghost_events == 2:
            self.waiting = True
            pg.time.wait(1000)
            self.render()
            self.waiting = False
            self.check_death()
        
        elif ghost_events == 1:
            ghost_points = int(self.ghosts.get_points())
            self.score += ghost_points
            self.text.add_temp_text(ghost_points, self.pacman.position - Vector2(TILEWIDTH,0))
            self.pacman.show = False
            self.waiting = True
            self.render()
            pg.time.wait(1000)
            
            for ghost in self.ghosts:
                ghost.show = True
            
            self.waiting = False
            self.pacman.show = True
        
        self.text.update(deltatime)
        self.render()
        
    def set_highscore(self):
        if self.highscore < self.score:
            self.highscore = self.score

    def reset(self):
        '''
        Resets the level(Map, Pellets, Pac-Man, Ghosts)
        '''
        self.ghosts.rend = False
        sound.reset()
        self.render()
        self.waiting = True
        pg.event.get()
        pg.time.wait(1000)
        self.rend = False
        
        for row in self.map.tiles:
            pg.event.get()
            
            for tile in row:
                self.screen.blit(self.map.tiles[0][0].sprite, (tile.x, tile.y))
                pg.display.update()
                pg.time.wait(1)
        
        pg.display.update()
        pg.time.wait(500)
        self.rend = True
        self.waiting = True
        self.pacman.reset_self()
        self.ghosts.reset()
        
        #Level won
        if self.pellets.isEmpty():
            self.pellets_eaten = 0
            self.pellets.reset()
        
        self.render()
        pg.event.get()
        pg.time.wait(2000)
        self.release_after_pellets = [0 + self.pellets_eaten, 10 + self.pellets_eaten, 20 + self.pellets_eaten]
        
        sound.start()
        sound.background_music('siren_1.wav', 0.2)
        
        self.death = False
        self.cruising = 60 + self.pellets_eaten
        self.waiting = False

    def check_pellet_collision(self):
        '''
        Checks for collisions between Pac-Man and all the pellets on the map

        Attributes
        ----------
        pellet : bool
            when a pellet has been eaten, pacman.py will return pellet as 'True'
        '''
        pellet = self.pacman.eat_pellet(self.pellets.pellet_list)
        if pellet:
            self.pellets_eaten += 1

            #Amount of times, eating animation is played
            self.pacman.pellet_anim = 2
            
            #Play eating sound(wakawakawaka)
            sound.play_channel('pellet_munch_1.wav', 0.2, 0, 1)
            
            #stop Pac-Man's movement for 1 frame or 16,67ms when a pellet is eaten
            self.pacman.stop_frame = True

            #Increases current score by pellet.points or powerpellet.points amount
            self.score += pellet.points

            #removes eaten pellets from the pellet list
            self.pellets.pellet_list.remove(pellet)
            #print(self.score)

            if pellet.name == "PowerPellet":
                pg.mixer.music.pause()
                
                self.pp_sound = sound.play_channel('power_pellet.wav', 0.15, -1, 0)

                self.ghosts.power_pellet()
                pg.time.set_timer(self.PP_over, 8000)

        #checks if the list of all uneaten pellets is empty
        if self.pellets.isEmpty():
            #no longer show Pac-Man's sprite
            self.pacman.show = False
            self.ghosts.rend = False
            self.level += 1
            self.reset()
            #TODO: flash background, reset level, reset Pac-Man(save lives and score)

    def check_Events(self):
        '''
        Checks for pygame events

        Attributes
        ----------
        event : pygame.event
            pygame Event
        '''

        #get all events from pygame.event.get() and loop through them
        for event in pg.event.get():

            #when player tries to close the window, the game is no longer permitted to run
            if event.type == pg.QUIT:
                self.run = False
            
            if event.type == self.PP_over:
                pass
                #self.ghosts.pp_over()
    def check_fruit_events(self, deltatime):
        self.timer += deltatime
        
        if self.timer >= 10 and not self.fruit.delete:
            self.fruit.update(deltatime)
            dist = (self.pacman.position - self.fruit.position).magnitude_squared()
            
            if dist < 16 ** 2:
                self.score += self.fruit.points
                self.fruit.delete = True
                self.text.add_temp_text(self.fruit.points, self.fruit.position)      

    def check_death(self):
        '''
        Handels Pac-Man's death
        '''
        self.ghosts.rend = False
        self.render()
        self.pacman.live_lost()
        
        pg.mixer.stop()
        pg.mixer.music.stop()
        sound.play_channel('death_1.wav', 0.2, 0, 5)
        self.waiting = True


        if self.pacman.lives == 0:
            self.gameover = True
            self.pacman.show = False
            self.save_highscore()
            
            self.text.show_gameover()
            
            #TODO: reset all
            pg.quit()
            

    def set_events(self):
        '''
        Defines specific pygame events
        '''
        self.FRAME_SKIPPED = pg.USEREVENT

    def render(self):
        '''
        Renders all visual elements
6
        Returns
        -------
        pygame.Surface
            Updated screen with all screen elements

        '''
        #renders the map walls
        for row in self.map.tiles:
            for tile in row:
                self.screen.blit(tile.sprite, (tile.x, tile.y))

        self.pellets.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        self.pacman.render_lives(self.screen)
        self.text.render(self.screen)
        if self.timer >= 10 and not self.fruit.delete:
            self.fruit.render(self.screen)
        pg.display.update()


if __name__ == "__main__":

    #Initializes the- GameController class object
    game = GameController()
    while game.run:
        game.update()
