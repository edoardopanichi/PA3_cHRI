import numpy as np
import random
import pygame

class Target:
    def __init__(self, civilian=True):
        self.civilian = civilian 
        self.moving_direction = np.array([random.choice([-1, 0, 1]), random.choice([-1, 0, 1])])
        self.speed = random.uniform(0.5, 1.5)
        self.pos = x_rand = np.array([random.uniform(50, 750), random.uniform(50, 300)])
        self.hit = False
    
    def update_pos(self):
        self.pos += self.moving_direction * self.speed
    
    def bounce_tb(self):
        self.moving_direction[1]=-self.moving_direction[1]
    
    def bounce_lr(self):
        self.moving_direction[0]=-self.moving_direction[0]
    
    def printamelo(self):
        print(self.pos, self.speed, self.moving_direction)
    
    
    
