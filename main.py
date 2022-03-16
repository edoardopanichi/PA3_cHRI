import numpy as np
import pygame
import random

pygame.init() # start pygame
window = pygame.display.set_mode((800, 600)) # create a window (size in pixels)
window.fill((255,255,255)) # white background
xc, yc = window.get_rect().center # window center
pygame.display.set_caption('robot arm')
image = pygame.image.load('danger.jpeg')
image = pygame.transform.scale(image, (50, 50))

font = pygame.font.Font('freesansbold.ttf', 15) # printing text font and font size
text = font.render('KILLS: ', True, (0, 0, 0), (255, 255, 255)) # printing text object
textRect = text.get_rect()
textRect.topleft = (10, 10) 

clock = pygame.time.Clock() # initialise clock

dts = 0.01
FPS = int(1/dts)

x_rand = random.randint(50, 750)
y_rand = random.randint(50,300)

radius = 25
count = 0

run = True
while run:
    for event in pygame.event.get(): # interrupt function
        if event.type == pygame.QUIT: # force quit with closing the window
            run = False
        elif event.type == pygame.KEYUP:
            if event.key == ord('q'): # force quit with q button
                run = False
            if event.key == ord('c'): # force quit with q button
                xm,ym = pygame.mouse.get_pos()
                if np.sqrt((xm-x_rand)**2 + (ym - y_rand)**2)<radius:
                    x_rand = random.randint(50, 750)
                    y_rand = random.randint(50,300)
                    count+=1

                
    
    
    # real-time plotting
    window.fill((255,255,255)) # clear window
    
    text = font.render('KILLS: '+ str(count), True, (255, 0, 0), (255, 255, 255))
    
    window.blit(text, textRect)
    #pygame.draw.circle(window, (0, 255, 0), (x_rand, y_rand), radius)
    window.blit(image, (x_rand-25, y_rand-25))
    pygame.display.flip() # update display
    
    
    
    # try to keep it real time with the desired step time
    clock.tick(FPS)
    
    if run == False:
        break
    
pygame.quit() # stop pygame


