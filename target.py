import numpy as np
import random
import pygame

class Target:
    def __init__(self, target=True):
        self.target = target
        if not target: 
            self.moving_direction = np.array([random.choice([-1, 1]), random.choice([-1, 1])])
        else:
            self.moving_direction = np.array([random.choice([-1, 0, 1]), random.choice([-1, 0, 1])])
        self.speed = random.uniform(0.5, 1.5)
        self.pos = np.array([random.uniform(50, 750), random.uniform(50, 450)])
    
    def update_pos(self):
        self.pos += self.moving_direction * self.speed
    
    def bounce_tb(self):
        self.moving_direction[1]=-self.moving_direction[1]
    
    def bounce_lr(self):
        self.moving_direction[0]=-self.moving_direction[0]
    
    def hit(self):
        self.moving_direction = np.array([random.choice([-1, 0, 1]), random.choice([-1, 0, 1])])
        self.speed = random.uniform(0.5, 1.5)
        self.pos = np.array([random.uniform(50, 750), random.uniform(50, 300)])
    
    
    
    
    
