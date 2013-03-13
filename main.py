# ---------------------------------------------------------------------------------------
#  Symmetry Game
#   Ronald Sardarian, Theo Guariello, Ryan Wright
#  A simple proof of concept.
# ---------------------------------------------------------------------------------------

import pygame, math, sys, random, os
# from player import *


# ---------------------------------------------------------------------------------------    
# Game class, used to track essential game values and calls other logic

DEBUG_MODE = False
GAME_WIDTH = 1024
GAME_HEIGHT = 768

class Game(object):
    def __init__(self):
        # self.screen = pygame.display.set_mode((WIDTH,HEIGHT), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.game_screen = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.game_over = False
        self.game_exit = False
        self.clock = pygame.time.Clock()
        
        self.KEYS = {
            'left':  pygame.K_a, 
            'right': pygame.K_d, 
            'up': pygame.K_w, 
            'down':  pygame.K_s, 
            'quit': pygame.K_q,  
            'restart': pygame.K_r, 
            'pause': pygame.K_ESCAPE, 
            'confirm': pygame.K_RETURN, 
            'suicide': pygame.K_v
            }
        
        # this loads the backgournd image of the game
        self.game_bg = pygame.image.load(resource_path('game-bg.png')).convert_alpha()
        
        #loads pause screen image
        self.pause_screen = pygame.image.load(resource_path('pause.png')).convert_alpha()
        
        self.game_time = pygame.time.get_ticks()
        self.paused = False
        self.pause_time = 0

        # Call initializing stuff
        self.start_game()
        
        
        # example on how to import a sound
        #self.sfx_kill = pygame.mixer.Sound(resource_path(os.path.join('Sounds', 'spider kill (freesfx.co.uk).wav')))

        
        # functions to play sounds
        # self.sfx_ambient.set_volume(0.3)
        # self.sfx_ambient.play(-1)
        
        #self.score_made = False
        
        
    def splash_screen(self):
        # Start of game splash screen
        splash = True
        
        splash_background = pygame.image.load(resource_path('instructions-keyboard.png')).convert_alpha()
        
        splash_background_rect = splash_background.get_rect()
        self.screen.blit(splash_background, splash_background_rect)
        pygame.display.flip() #flushes to buffer (draws to screen)
        
            
        while (splash):
            self.pause_time = pygame.time.get_ticks() - self.game_time
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_exit = True
                    splash = False
                if event.type == pygame.KEYDOWN:
                    if event.key in self.KEYS['confirm']:
                        splash = False
                    if event.key in self.KEYS['quit']:
                        self.game_exit = True
                        

    #initialize all the variables we need for the game 
    def start_game(self):
        self.splash_screen()
        self.paused = False
        self.player = man(self.game_time)#initialize player object
        
        #initialize actor lists
        self.enemy_list = [] #example
        
        #for i in range(0,8):
        #   self.egg_list.append(Egg()) #appends 8 actors example
        
        
        self.timer = 20
        self.timer_past_time = self.game_time
        
        self.wave_number = 0    
        
        
        self.score = 0
        self.last_score_time = self.game_time
        
    #process player input
    def process_events(self):
        if not self.paused:
            key = pygame.key.get_pressed() # all keys currently pressed, used for continued actions (movement)
            if key[self.KEYS['left']]:
                self.player.move_left()
                break
                    

            if key[self.KEYS['right']]:
                self.player.move_right()
                break
                    

            if key[self.KEYS['up']]:
                self.player.move_up()
                break
                    

            if key[self.KEYS['down']]:
                self.player.move_down()
                break

            if key[self.KEYS['jump']]:
                self.player.jump()
                self.sfx_jump.play()
                break
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_exit = True
        
            if event.type == pygame.KEYDOWN: 
                if event.key in self.KEYS['quit']:
                    self.game_exit = True
                if event.key in self.KEYS['restart']:
                    if not (self.game_over)
                        self.reset_game()
                if event.key in self.KEYS['pause']:
                    self.paused = not self.paused
                if DEBUG_MODE:
                    if event.key in self.KEYS['suicide']:
                        self.game_over = True
                if not self.paused:
                    
                                    
                # End Game
                #if self.game_over:
                    
                        
    def reset_game(self):
        self.game_over = False
        self.start_game()
        
        
    def update(self):
        if self.paused:
            self.pause_time = pygame.time.get_ticks() - self.game_time
        else:
            self.game_time = pygame.time.get_ticks() - self.pause_time
                    
            if self.game_time - self.timer_past_time > 1000:
                #self.timer_past_time += 1000
                self.timer_past_time = self.game_time
                if self.timer > 0:
                    self.timer -= 1
        
            self.player.update(self.game_time)

        
    def draw(self):
        self.screen.fill((30,30,30))
        self.game_screen.fill((80,80,80))
        self.game_screen.blit( self.game_bg, pygame.Rect(0, 0, self.game_bg.get_width(), self.game_bg.get_height()))
        
        # print after - before, "millis"
        
        
        # redraw actors from lists

        
        # redraw the player object (above all other objects)
        self.player.draw(self.game_screen)
       
        self.screen.blit(self.game_screen, (0, 0))
 
        if self.paused:
            self.screen.blit(self.pause_screen, (0, 0))
 
            

        
        
# ---------------------------------------------------------------------------------------    


# ---------------------------------------------------------------------------------------    
# Overall game logic. Creates a Game object and calls its functions in order, draws to the screen

pygame.init()
pygame.display.set_caption("Symmetry Game Prototype")
g = Game()
pygame.key.set_repeat(500, 200)

# g.splash_screen()

while not g.game_exit:
    g.clock.tick(30)
    g.process_events()
    g.update()
    g.draw()
    pygame.display.flip()

    
sys.exit()
    
    
    
    
    
    
