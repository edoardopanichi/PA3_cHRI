import numpy as np
import pygame
import random
import sys, serial, glob
from serial.tools import list_ports
import time
from target import Target
from haply_code.pyhapi import Board, Device, Mechanisms
from haply_code.pantograph import Pantograph

''' DESCRIPTION OF SOME VARIABLE OF THE CODE
xh -> x and y coordinates of the haptic device or the mouse otherwise
'''


# VARIABLES OF SIMULATION ON PYGAME
pygame.init() # start pygame
window = pygame.display.set_mode((800, 600)) # create a window (size in pixels)
window.fill((255,255,255)) # white background
pygame.display.set_caption('shooting targets')
image = pygame.image.load('image/terrorist.png')
image = pygame.transform.scale(image, (50, 50))

font = pygame.font.Font('freesansbold.ttf', 15) # printing text font and font size
text = font.render('KILLS: ', True, (0, 0, 0), (255, 255, 255)) # printing text object
textRect = text.get_rect()
textRect.topleft = (10, 10)

window_scale = 3 # conversion from meters to pixels. Not sure if we need it

clock = pygame.time.Clock() # initialise clock

dts = 0.01
FPS = int(1/dts)

# VARIABLES ABOUT ELEMENTS OF THE SIMULATION (targets, forces, CGI elements and so on...)
x_rand = random.randint(50, 750)
y_rand = random.randint(50,300)

radius = 25
count = 0
xc, yc = window.get_rect().center # window center
fe = np.zeros(2)

target_list=[]
for i in range(5):
    target = Target(True)
    target_list.append(target)


##################### Detect and Connect Physical device #####################
# USB serial microcontroller program id data:
def serial_ports():
    """ Lists serial port names """
    ports = list(serial.tools.list_ports.comports())

    result = []
    for p in ports:
        try:
            port = p.device
            s = serial.Serial(port)
            s.close()
            if p.description[0:12] == "Arduino Zero":
                result.append(port)
                print(p.description[0:12])
        except (OSError, serial.SerialException):
            pass
    return result


CW = 0
CCW = 1

haplyBoard = Board
device = Device
SimpleActuatorMech = Mechanisms
pantograph = Pantograph
   

#########Open the connection with the arduino board#########
port = serial_ports()   ##port contains the communication port or False if no device
if port:
    print("Board found on port %s"%port[0])
    haplyBoard = Board("test", port[0], 0)
    device = Device(5, haplyBoard)
    pantograph = Pantograph()
    device.set_mechanism(pantograph)
    
    device.add_actuator(1, CCW, 2)
    device.add_actuator(2, CW, 1)
    
    device.add_encoder(1, CCW, 241, 10752, 2)
    device.add_encoder(2, CW, -61, 10752, 1)
    
    device.device_set_parameters()
else:
    print("No compatible device found. Running virtual environnement...")
    

run = True
while run:
    ##Get endpoint position xh
    if port and haplyBoard.data_available():    ##If Haply is present
        #Waiting for the device to be available
        #########Read the motorangles from the board#########
        device.device_read_data()
        motorAngle = device.get_device_angles()
        
        #########Convert it into position#########
        device_position = device.get_device_position(motorAngle)
        xh = np.array(device_position) * 1e3 * window_scale
        xh[0] = np.round(-xh[0] + 300)
        xh[1] = np.round(xh[1] - 60)
        
         
    else:
        # ##Compute distances and forces between blocks
        # xh = np.clip(np.array(haptic.center),0,599)
        # xh = np.round(xh)
        
        ##Get mouse position
        mouse_pos = pygame.mouse.get_pos()
        xh = np.clip(np.array(mouse_pos), 0, 599)
        
    for event in pygame.event.get(): # interrupt function
        if event.type == pygame.QUIT: # force quit with closing the window
            run = False
        elif event.type == pygame.KEYUP:
            if event.key == ord('q'): # force quit with q button
                run = False
            if event.key == ord('c'): # force quit with q button
                xm,ym = pygame.mouse.get_pos()
                for target in target_list:
                    if np.sqrt((xm-int(target.pos[0]))**2 + (ym -int(target.pos[1]))**2)<radius:
                        target.hit=True

                
    
    
    # real-time plotting
    window.fill((255,255,255)) # clear window
    
    text = font.render('KILLS: '+ str(count), True, (255, 0, 0), (255, 255, 255))
    
    window.blit(text, textRect)
    #pygame.draw.circle(window, (0, 255, 0), (x_rand, y_rand), radius)
    for target in target_list:
        if target.hit == False:
            #pygame.draw.circle(window, (0, 255, 0), np.round(target.pos), radius)
            window.blit(image, (int(target.pos[0])-25, int(target.pos[1])-25))
            target.update_pos()
    
    
    
    pygame.display.flip() # update display
    
    
     ######### Send forces to the device #########
    if port:
        fe[1] = -fe[1]  ##Flips the force on the Y=axis 
        
        ##Update the forces of the device
        device.set_device_torques(fe)
        device.device_write_torques()
        #pause for 1 millisecond
        time.sleep(0.001)
    #else:
        ######### Update the positions according to the forces ########
        ##Compute simulation (here there is no inertia)
        ##If the haply is connected xm=xh and dxh = 0
        #dxh = (k/b*(xm-xh)/window_scale - fe/b)    ####replace with the valid expression that takes all the forces into account
        #dxh = dxh*window_scale
        #xh = np.round(xh+dxh)             ##update new positon of the end effector
        
    
    
    # try to keep it real time with the desired step time
    clock.tick(FPS)
    
    if run == False:
        break
    
pygame.quit() # stop pygame


