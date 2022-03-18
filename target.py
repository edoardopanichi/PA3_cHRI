import numpy as np
import random
import pygame

class Target:
    def __init__(self, civilian=True):
        self.civilian = civilian 
        self.moving_direction = np.array([random.choice([-1, 0, 1]), random.choice([-1, 0, 1])])
        self.speed = random.uniform(0.5, 2)
        self.pos = x_rand = np.array([random.uniform(50, 750), random.uniform(50, 300)])
        self.hit = False
    
    def update_pos(self):
        self.pos += self.moving_direction * self.speed
    
    def printamelo(self):
        print(self.pos, self.speed, self.moving_direction)
    
    
    
