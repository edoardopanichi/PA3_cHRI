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
xc, yc = window.get_rect().center # window center
target_radius = 25

# Images 
pygame.display.set_caption('shooting targets')
imageTerrorist = pygame.image.load('image/terrorist.png')
imageTerrorist = pygame.transform.scale(imageTerrorist, (2*target_radius, 2*target_radius))

imageTarget = pygame.image.load('image/target.png')
imageTarget = pygame.transform.scale(imageTarget, (2*target_radius, 2*target_radius))

crossSize = 90  # int
imageCross = pygame.image.load('image/cross2.png')
imageCross = pygame.transform.scale(imageCross, (crossSize, crossSize))

factor = 0.7  # factor to scale image
imageSniper = pygame.image.load('image/sniper1.png')
imageSniper = pygame.transform.scale(imageSniper, (220, 60))
imageSniperSmall = pygame.transform.scale(imageSniper, (int(factor*220), int(factor*60)))
imageSniperRect = imageSniper.get_rect ()
imageSniperRect.center = (xc-250, yc+50)

imageRifle = pygame.image.load('image/rifle1.png')
imageRifle = pygame.transform.scale(imageRifle, (180, 90))
imageRifleSmall = pygame.transform.scale(imageRifle, (int(factor*180), int(factor*90)))
imageRifleRect = imageRifle.get_rect ()
imageRifleRect.center = (xc, yc+50)

imagePistol = pygame.image.load('image/pistol1.png')
imagePistol = pygame.transform.scale(imagePistol, (110, 65))
imagePistolSmall = pygame.transform.scale(imagePistol, (int(factor*110), int(factor*65)))
imagePistolRect = imagePistol.get_rect ()
imagePistolRect.center = (xc+250, yc+50)

# Text
font = pygame.font.Font('freesansbold.ttf', 15) # printing text font and font size
textHits = font.render('Hits: ', True, (0, 0, 0), (255, 255, 255)) # printing text object
textHitsRect = textHits.get_rect()
textHitsRect.topleft = (10, 30) 

textTime = font.render('Time: ', True, (0, 0, 0), (255, 255, 255)) # printing text object
textTimeRect = textTime.get_rect()
textTimeRect.topleft = (10, 10) 

fontTitle = pygame.font.Font('freesansbold.ttf', 50) # printing text font and font size
title = fontTitle.render('Gun simulation', True, (0, 0, 0), (255, 255, 255)) # printing text object
titleRect = title.get_rect()
titleRect.center = (xc, yc-200) 

fontChoice = pygame.font.Font('freesansbold.ttf', 25) # printing text font and font size
textChoice = fontChoice.render('Choose a weapon:', True, (0, 0, 0), (255, 255, 255)) # printing text object
textChoiceRect = textChoice.get_rect()
textChoiceRect.center = (xc, yc-80) 

fontGun = pygame.font.Font('freesansbold.ttf', 20) # printing text font and font size
textSniper1 = fontGun.render('Sniper', True, (0, 0, 0), (255, 255, 255)) # printing text object
textSniper1Rect = textSniper1.get_rect()
textSniper1Rect.center = (xc-250, yc) 
textSniper2 = fontGun.render('Press \'s\'', True, (0, 0, 0), (255, 255, 255)) # printing text object
textSniper2Rect = textSniper2.get_rect()
textSniper2Rect.center = (xc-250, yc+100) 

textRifle1 = fontGun.render('Rifle', True, (0, 0, 0), (255, 255, 255)) # printing text object
textRifle1Rect = textRifle1.get_rect()
textRifle1Rect.center = (xc, yc)
textRifle2 = fontGun.render('Press \'r\'', True, (0, 0, 0), (255, 255, 255)) # printing text object
textRifle2Rect = textRifle2.get_rect()
textRifle2Rect.center = (xc, yc+100)

textPistol1 = fontGun.render('Pistol', True, (0, 0, 0), (255, 255, 255)) # printing text object
textPistol1Rect = textPistol1.get_rect()
textPistol1Rect.center = (xc+250, yc)
textPistol2 = fontGun.render('Press \'p\'', True, (0, 0, 0), (255, 255, 255)) # printing text object
textPistol2Rect = textPistol2.get_rect()
textPistol2Rect.center = (xc+250, yc+100)

textScore = fontTitle.render('Score', True, (0, 0, 0), (255, 255, 255)) # printing text object
textScoreRect = textScore.get_rect()
textScoreRect.center = (xc, yc-175) 

fontTable = pygame.font.Font('freesansbold.ttf', 20) # printing text font and font size
textKPM = fontTable.render('Kills per minute:', True, (0, 0, 0), (255, 255, 255)) # printing text object
textKPMRect = textKPM.get_rect()
textKPMRect.center = (xc, yc-50) 

textBPM = fontTable.render('Bullets per minute:', True, (0, 0, 0), (255, 255, 255)) # printing text object
textBPMRect = textBPM.get_rect()
textBPMRect.center = (xc, yc)  

textSME = fontTable.render('SME from target center:', True, (0, 0, 0), (255, 255, 255)) # printing text object
textSMERect = textSME.get_rect()
textSMERect.center = (xc, yc+50) 

textRestart = fontTable.render('Press \'z\' for restart', True, (0, 0, 0), (255, 255, 255)) # printing text object
textRestartRect = textRestart.get_rect()
textRestartRect.center = (xc, yc+150)

window_scale = 3 # conversion from meters to pixels. Not sure if we need it

clock = pygame.time.Clock() # initialise clock

dts = 0.01
FPS = int(1 / dts)

# VARIABLES ABOUT ELEMENTS OF THE SIMULATION (targets, forces, CGI elements and so on...)
x_rand = random.randint(50, 750)
y_rand = random.randint(50, 300)

radius = 25
count = 0

xc, yc = window.get_rect().center # window center

k = 1
b = 1
killCount = 0
bulletCount = 0
gun = "empty"
timeCountdown = 15

# some variables needed to define the forces
fe = np.zeros(2)
xh_old = np.zeros(2)
velocity_device = np.zeros(2)
v = np.random.rand(2) # random vector
v_hat = v / np.linalg.norm(v) # random unit vector to choose the direction of the wind

target_num = 2
target_list=[]
for i in range(target_num):
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
startscreen = True
endscreen = False
setTimer = 0
while run:
    '''*********** STARTSCREEN ***********'''
    while startscreen:  
        for event in pygame.event.get(): # interrupt function
            if event.type == pygame.QUIT: # force quit with closing the window
                startscreen = False
                setTimer = 1
                run = False
            elif event.type == pygame.KEYUP:
                if event.key == ord('q'): # force quit with q button
                    startscreen = False
                    setTimer = 1
                    run = False
                if event.key == ord('s'): # select sniper
                    setTimer = 1
                    gun = "sniper"
                    startscreen = False
                if event.key == ord('r'): # select rifle
                    setTimer = 1
                    gun = "rifle"
                    startscreen = False
                if event.key == ord('p'): # select pistol
                    setTimer = 1
                    gun = "pistol"
                    startscreen = False
        
        # real-time plotting
        window.fill((255,255,255)) # clear window
    
        # plot text to screen
        window.blit(title, titleRect)
        window.blit(textChoice, textChoiceRect)
        window.blit(textSniper1, textSniper1Rect)
        window.blit(textSniper2, textSniper2Rect)
        window.blit(textRifle1, textRifle1Rect)
        window.blit(textRifle2, textRifle2Rect)
        window.blit(textPistol1, textPistol1Rect)
        window.blit(textPistol2, textPistol2Rect)
        
        # plot images
        window.blit(imageSniper, imageSniperRect)
        window.blit(imageRifle, imageRifleRect)
        window.blit(imagePistol, imagePistolRect)
        #window.blit(image, (xc-25, yc-150))
        pygame.display.flip() # update display
    '''*********** !STARTSCREEN ***********'''    
    
    '''ACQUIRING THE POSITION FROM THE HAPLY IF CONNECTED, FROM THE MOUSE OTHERWISE'''
    ##Get endpoint/mouse position xh
    if port and haplyBoard.data_available():    ##If Haply is present
        #Waiting for the device to be available
        #########Read the motorangles from the board#########
        device.device_read_data()
        motorAngle = device.get_device_angles()
        
        #########Convert it into position#########
        device_position = device.get_device_position(motorAngle)
        xh = np.array(device_position) * 1e3 * window_scale
        xh[0] = np.round(-xh[0] + 210) * 1.9 # we shift and multiply the position read to obtain a situation in which every point of
        # the window in the game is reachable through a position in the workspace with the haply
        xh[1] = np.round(xh[1] - 65) * 1.9 # we shift and multiply the position read to obtain a situation in which every point of
        # the window in the game is reachable through a position in the workspace with the haply
         
    else:
        ##Get mouse position
        mouse_pos = pygame.mouse.get_pos()
        xh = np.clip(np.array(mouse_pos), 0, pygame.display.get_surface().get_width()-1)
        
    print("\nposition of mouse or haply:", xh)
    
    '''************* TASK *************'''
    for event in pygame.event.get(): # interrupt function
        if event.type == pygame.QUIT: # force quit with closing the window
            run = False
        elif event.type == pygame.KEYUP:
            if event.key == ord('q'): # force quit with q button
                run = False
            if event.key == pygame.K_SPACE: # force quit with q button
                bulletCount += 1
                for target in target_list:
                    if np.sqrt((xh[0]-int(target.pos[0]))**2 + (xh[1] -int(target.pos[1]))**2)<radius:
                        target.hit()
                        killCount += 1
                    
    # start timer
    if setTimer == 1:
        timerStart = time.perf_counter()
        timerEnd = timerStart + timeCountdown  # define time of timer
        setTimer = 0
        killCount = 0
        bulletCount = 0
    
    # end timer
    if  time.perf_counter() >= timerEnd:
        endscreen = True
    
    countdown = round(timerEnd-time.perf_counter(), 1)
    
    
    if gun == 'sniper':
        # define the features of the gun
        f_viscosity = 4*b*velocity_device
        f_gravity = np.array([0, -10])
        # ...
        # change gun image
        imageGun = imageSniperSmall
        imageGunRect = imageSniperSmall.get_rect()
        imageGunRect.topright = (795, 5)
    
    if gun == 'rifle':
        # define the features of the gun
        f_viscosity = 1*velocity_device
        f_gravity = np.array([0, -2.5])
        # ...
        # change gun image
        imageGun = imageRifleSmall
        imageGunRect = imageRifleSmall.get_rect()
        imageGunRect.topright = (795, 5)
    
    if gun == 'pistol':
        # define the features of the gun
        f_viscosity = np.zeros(2)
        f_gravity = np.zeros(2)
        # ...
        # change gun image
        imageGun = imagePistolSmall
        imageGunRect = imagePistolSmall.get_rect()
        imageGunRect.topright = (795, 5)
    
    
    # real-time plotting
    window.fill((255,255,255)) # clear window
    
    # plot time
    textTime = font.render('Time: '+ str(countdown), True, (0, 0, 0), (255, 255, 255))
    window.blit(textTime, textTimeRect)
    
    # plot kill count
    textHits = font.render('HITS: '+ str(killCount), True, (255, 0, 0), (255, 255, 255))
    window.blit(textHits, textHitsRect)
    
    # plot target
    #pygame.draw.circle(window, (0, 255, 0), (x_rand, y_rand), radius)
    for target in target_list:
        x_pos = int(target.pos[0])
        y_pos = int(target.pos[1])
        if 800-x_pos<1+target_radius  or x_pos<1+target_radius:
            target.bounce_lr()
        if 600-y_pos<1+target_radius or y_pos<1+target_radius:
            target.bounce_tb()
        #pygame.draw.circle(window, (0, 255, 0), np.round(target.pos), radius)
        window.blit(imageTarget, (x_pos-25, y_pos-25))
        target.update_pos()
    
    
    window.blit(imageCross, (xh[0]-2-crossSize/2, xh[1]-2-crossSize/2))
    pygame.draw.circle(window, (0, 255, 0), (xh[0], xh[1]), 3) # draw a green point for aiming
    window.blit(imageGun, imageGunRect)
    pygame.display.flip() # update display
    
    # COMPUTING FEEDBACK FORCES AND PERTURBATIONS
    f_perturbance = np.multiply(np.array([2*np.sin(1.5*countdown), 1.5*np.sin(5*countdown)]), v_hat) # perturbation caused by multiple possible external 
    # factors: wind, hand shaking, etc.
    print("f_perturbance", f_perturbance)
    
    velocity_device = ((xh - xh_old)/dts)/(window_scale*1e3) # used for the f_viscosity
    f_viscosity = f_viscosity # the actual calculation of this force is done above where we check which weapon has been chosen.
    # this equivalence is useless, it is here just as a reminder of the force
    f_gravity = f_gravity # check comment of f_viscosity
    
    # f_height_map =
    # fe = f_height_map + f_perturbance + f_viscosity
    fe = f_gravity + f_viscosity + f_perturbance
    
    xh_old = xh # Update xh_old to compute the velocity
    
     ######### Send forces to the device #########
    if port:
        fe[1] = -fe[1]  ##Flips the force on the Y=axis 
        
        ##Update the forces of the device
        device.set_device_torques(fe)
        device.device_write_torques()
        #pause for 1 millisecond
        time.sleep(0.001)
        
    # else:
    #     ######### Update the positions according to the forces ########
    #     ##Compute simulation (here there is no inertia)
    #     ##If the haply is connected xm=xh and dxh = 0
    #     dxh = (k/b*(xm-xh)/window_scale - fe/b)    ####replace with the valid expression that takes all the forces into account
    #     dxh = dxh*window_scale
    #     xh = np.round(xh+dxh)             ##update new position of the end effector
    
    
    '''************* !TASK *************'''
    
    
    '''*********** ENDSCRREEN ***********'''
    while endscreen:  
        for event in pygame.event.get(): # interrupt function
            if event.type == pygame.QUIT: # force quit with closing the window
                endscreen = False
                run = False
            elif event.type == pygame.KEYUP:
                if event.key == ord('q'): # force quit with q button
                    endscreen = False
                    run = False
                if event.key == ord('z'): # restart button
                    endscreen = False
                    startscreen = True
                    target_list=[]
                    for i in range(target_num):
                        target = Target(True)
                        target_list.append(target)
        
        # real-time plotting
        window.fill((255,255,255)) # clear window
    
        # plot text to screen
        window.blit(textScore, textScoreRect)
        textKPM = fontTable.render('Kills per minute: ' + str(killCount), True, (0, 0, 0), (255, 255, 255)) # printing text object
        window.blit(textKPM, textKPMRect)
        textBPM = fontTable.render('Bullets per minute: ' + str(bulletCount), True, (0, 0, 0), (255, 255, 255)) # printing text object
        window.blit(textBPM, textBPMRect)
        window.blit(textSME, textSMERect)
        window.blit(textRestart, textRestartRect)
        
        # plot images
        
        pygame.display.flip() # update display
    '''*********** !ENDSCREEN ***********'''
    
    
    # try to keep it real time with the desired step time
    clock.tick(FPS)
    
    if run == False:
        break
    
pygame.quit() # stop pygame


