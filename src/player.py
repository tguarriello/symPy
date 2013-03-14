
import pygame, math, sys, random, os
from utilities import *

MOVE_SPEED = 3.75
ACC_SPEED = 0.5
SPEED_DAMPENING = 0.97 # 0.55
# JUMP_SPEED = 120
# GRAVITY_SPEED = 5.00
MASK_ALPHA_THRESHOLD = 80
COLLISION_INCREMENTS = 5

class Player(object):
    
    def __init__( self, initial_x, initial_y, game_time ):
        

        self.img = pygame.image.load( resource_path( 'test_rect.png' ) ).convert_alpha()
        self.img_rect = self.img.get_rect()
        
        self.collision_mask = None
        
        self.w = self.img_rect.width
        self.h = self.img_rect.height
        
        
        # self.pos = Vector2D( initial_x, initial_y ) # top left
        self.pos = Vector2D( initial_x, initial_y ) # center
        self.vel = Vector2D()
        self.acc = Vector2D()
        
        self.on_the_ground = True
        
        # can be "tall" "short" or "normal"
        
        self.alive = True
        
        # self.update_speed = 75
        # self.frame = 0
        # self.frame_start_time = game_time
        
        # self.direction = 0
        # self.pose = 0
        # self.pose_height = 356              # 356 px height for each pose
        # self.w = self.img_rect.width / 4    # 4 Col
        # self.h = self.img_rect.height / 8   # 8 Row
        # self.source = pygame.Rect(self.frame*self.w,self.direction*self.h + self.pose * self.pose_height ,self.w,self.h)
    
       
    def move_right( self ):
        if  self.vel.x < MOVE_SPEED:
            self.vel.x += ACC_SPEED
        else:
            self.vel.x = MOVE_SPEED
    
    def move_left( self ): 
        if self.vel.x < MOVE_SPEED:
            self.vel.x -= ACC_SPEED
        else:
            self.vel.x = MOVE_SPEED
        
    def move_up( self ):
        # self.vel.y -= MOVE_SPEED
        self.acc.y = -ACC_SPEED
        
    def move_down( self ):
        # self.vel.y += MOVE_SPEED
        self.acc.y = ACC_SPEED
        
    def accelerate_to( self, x, y ):
        diff = Vector2D( x - self.pos.x, y - self.pos.y )
        diff.normalize()
        diff.mult(ACC_SPEED)
        self.acc = diff
        
    # def jump( self ):
        # if self.on_the_ground:
            # self.vel.y -= JUMP_SPEED
        
    def update( self, game_time, scene_collision_mask, scroll_speed ):
        self.pos.x -= scroll_speed
        
        if not on_the_ground:        
            self.vel.y += GRAVITY_SPEED
        
        #updates state for transformation, changes self.img
        self.collision_mask = pygame.mask.from_surface( self.img, MASK_ALPHA_THRESHOLD )
        
        # self.img may have changed, recalculate collision mask
        # self.collision_mask = pygame.mask.from_surface( self.img, MASK_ALPHA_THRESHOLD )
        
        # --------------------------------------------------------------
        # check if current velocity collides
        # check if slightly smaller velocity collides
        # etc. until 0.1 * current velocity
        # either use current (no collisions) or the largest that collided, after applying collision interaction
        
        original_vel = Vector2D( self.vel.x, self.vel.y )
        # self.vel.mult( 0.1 )
        self.vel.mult( 1.0 / COLLISION_INCREMENTS )
        smaller_vel = Vector2D( self.vel.x, self.vel.y )
        
        flag = False
        
        # for i in range( 1, 11 ):
        # for i in range( 10, 0, -1 ):
        for i in range( COLLISION_INCREMENTS, 0, -1 ):
            self.vel = Vector2D( smaller_vel.x, smaller_vel.y )
            self.vel.mult( i )
            pre_collision_vel = Vector2D( self.vel.x, self.vel.y )
        
            self.collision_interaction( scene_collision_mask )
            
            diff = pre_collision_vel.subtract( self.vel )
            
            if diff.magnitude() > 0:
                # print "i:", i, ", diff magnitude:", diff.magnitude()
                flag = True
                break
            
        if not flag:
            self.vel = Vector2D( original_vel.x, original_vel.y )
            
        self.pos.add( self.vel )
        
        self.vel = Vector2D( original_vel.x, original_vel.y )
        
        # self.collision_interaction( scene_collision_mask )
            
        # self.pos.add( self.vel )
        
        # --------------------------------------------------------------
        
        '''
        self.collision_interaction( scene_collision_mask )
            
        self.pos.add( self.vel )
        '''
        
        self.vel.add( self.acc )
        self.acc.clear()
        self.vel.mult( SPEED_DAMPENING )
        self.vel.limit_x( MAXIMUM_HORIZONTAL_SPEED )
        self.vel.limit_y( MAXIMUM_VERTICAL_SPEED )

        self.keep_on_screen()
        
        # self.pos.limit_x_range( 0, WIDTH - self.w )
        # self.pos.limit_y_range( 0 , HEIGHT - self.h )
        
        self.img_rect = pygame.Rect( self.pos.x - self.w / 2.0, self.pos.y - self.h / 2.0, self.w, self.h )
        # self.img_rect = pygame.Rect( self.pos.x, self.pos.y , self.w, self.h )
    
    def keep_on_screen( self ):
        # self.pos.limit_x_range( 0 + self.w / 2, WIDTH - self.w / 2 )
        # self.pos.limit_y_range( 0 + self.h / 2, HEIGHT - self.h / 2 )
        self.pos.limit_x_range( 0, WIDTH  )
        self.pos.limit_y_range( 0, HEIGHT )
        
    
    def collision_interaction( self, scene_collision_mask ):
        # self.on_the_ground = False
    
        x = int( self.pos.x + self.vel.x - self.w / 2.0 )
        y = int( self.pos.y + self.vel.y - self.h / 2.0 )
        
        dx = scene_collision_mask.overlap_area( self.collision_mask, ( x + 1, y ) ) - scene_collision_mask.overlap_area( self.collision_mask, ( x - 1, y ) )
        dy = scene_collision_mask.overlap_area( self.collision_mask, ( x, y + 1 ) ) - scene_collision_mask.overlap_area( self.collision_mask, ( x, y - 1 ) )
        
        # if dy > 0:
            # self.on_the_ground = True
            
        if dx > 0 and self.pos.x <= 0.5:
            self.alive = False
        
        change = Vector2D(-dx, -dy)
        change.normalize()
        
        # print "change x:", change.x, ", y:", change.y
        
        # count = 0
        
        if change.magnitude() >= 0.8:
            while scene_collision_mask.overlap_area(self.collision_mask, (int(self.pos.x + self.vel.x - self.w / 2.0), int(self.pos.y + self.vel.y - self.h / 2.0))) != 0:
                # if count > 200:
                    # print "change.x:", change.x, ", change.y:", change.y, ", change.magnitude():", change.magnitude()
                # count += 1
                self.vel.add( change )
            
        # if self.vel.magnitude() > 10:
            # print self.vel.magnitude()
            
        # Check if something went very wrong in the algorithm
        # (as in... the algorithm decided that flinging this object very, very far away was the best solution to solve a collision)
        # If that happens, stop this object (radical but better than shooting off screen)
        if math.fabs(self.vel.x) > MAXIMUM_HORIZONTAL_SPEED * 3 or math.fabs(self.vel.y) > MAXIMUM_VERTICAL_SPEED * 3:
            self.vel.clear()
        
        
    def draw( self, screen ):
        # screen.blit(self.img, self.img_rect, pygame.Rect(self.frame*32,32*self.move_state,32,32))
        # screen.blit(self.img, self.img_rect, self.source)
        screen.blit( self.img, self.img_rect )
        

            
