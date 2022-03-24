import numpy as np
import pygame
import random
import sys, serial, glob
from serial.tools import list_ports
import time
import math
from target import Target
from haply_code.pyhapi import Board, Device, Mechanisms
from haply_code.pantograph import Pantograph
from height_map import create_targets, create_civilians
from save_scores import save_score
import matplotlib.pyplot as plt

''' DESCRIPTION OF SOME VARIABLE OF THE CODE
xh -> x and y coordinates of the haptic device or the mouse otherwise
'''


# VARIABLES OF SIMULATION ON PYGAME
pygame.init() # start pygame
window_dimension = (800, 600)
window = pygame.display.set_mode(window_dimension) # create a window (size in pixels)
window.fill((255,255,255)) # white background
xc, yc = window.get_rect().center # window center
target_radius = 25


# Images 
pygame.display.set_caption('shooting targets')

imageTarget = pygame.image.load('image/target.png') 
imageTarget = pygame.transform.scale(imageTarget, (2*target_radius, 2*target_radius))

imageCivilian = pygame.image.load('image/civilian1.png') 
imageCivilian = pygame.transform.scale(imageCivilian, (2*target_radius, 2*target_radius))

imageBgd1 = pygame.image.load('image/background1.jpg')
imageBgd1 = pygame.transform.scale(imageBgd1, (800, 600))

crossSize = 65  # int
imageCross = pygame.image.load('image/cross1.png')
imageCross = pygame.transform.scale(imageCross, (crossSize, crossSize))

factor = 0.7  # factor to scale image
imageSniper = pygame.image.load('image/sniper1.png')
imageSniper = pygame.transform.scale(imageSniper, (220, 60))
imageSniperSmall = pygame.transform.scale(imageSniper, (int(factor*220), int(factor*60)))
imageSniperRect = imageSniper.get_rect ()
imageSniperRect.center = (xc-250, yc+30)

imageRifle = pygame.image.load('image/rifle1.png')
imageRifle = pygame.transform.scale(imageRifle, (180, 90))
imageRifleSmall = pygame.transform.scale(imageRifle, (int(factor*180), int(factor*90)))
imageRifleRect = imageRifle.get_rect ()
imageRifleRect.center = (xc, yc+30)

imagePistol = pygame.image.load('image/pistol1.png')
imagePistol = pygame.transform.scale(imagePistol, (110, 65))
imagePistolSmall = pygame.transform.scale(imagePistol, (int(factor*110), int(factor*65)))
imagePistolRect = imagePistol.get_rect ()
imagePistolRect.center = (xc+250, yc+30)


# Text
font = pygame.font.Font('freesansbold.ttf', 18) # printing text font and font size
textTime = font.render('Time: ', True, (255, 0, 0)) # printing text object
textTimeRect = textTime.get_rect()
textTimeRect.topleft = (10, 10) 

textHits = font.render('Hits: ', True, (255, 0, 0)) # printing text object
textHitsRect = textHits.get_rect()
textHitsRect.topleft = (10, 30)

textShoot = font.render('Press \'SPACE\' to shoot', True, (0, 0, 0)) # printing text object
textShootRect = textShoot.get_rect()
textShootRect.center = (xc, 580)

fontCurrScore = pygame.font.Font('freesansbold.ttf', 25) # printing text font and font size
textCurrScore = font.render('SCORE:     ', True, (0, 0, 0), (255, 255, 255)) # printing text object
textCurrScoreRect = textCurrScore.get_rect()
textCurrScoreRect.center = (xc, 15)  

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
textSniper1Rect.center = (xc-250, yc-20) 
textSniper2 = fontGun.render('Press \'s\'', True, (0, 0, 0), (255, 255, 255)) # printing text object
textSniper2Rect = textSniper2.get_rect()
textSniper2Rect.center = (xc-250, yc+80) 

textRifle1 = fontGun.render('Rifle', True, (0, 0, 0), (255, 255, 255)) # printing text object
textRifle1Rect = textRifle1.get_rect()
textRifle1Rect.center = (xc, yc-20)
textRifle2 = fontGun.render('Press \'r\'', True, (0, 0, 0), (255, 255, 255)) # printing text object
textRifle2Rect = textRifle2.get_rect()
textRifle2Rect.center = (xc, yc+80)

textPistol1 = fontGun.render('Pistol', True, (0, 0, 0), (255, 255, 255)) # printing text object
textPistol1Rect = textPistol1.get_rect()
textPistol1Rect.center = (xc+250, yc-20)
textPistol2 = fontGun.render('Press \'p\'', True, (0, 0, 0), (255, 255, 255)) # printing text object
textPistol2Rect = textPistol2.get_rect()
textPistol2Rect.center = (xc+250, yc+80)

textRecoil = fontGun.render('Press \'1\' to activate/de-activate recoil', True, (0, 0, 0), (255, 255, 255)) # printing text object
textRecoilRect = textRecoil.get_rect()
textRecoilRect.center = (xc, yc+200)
textActivateGreen = fontGun.render('activate', True, (0, 255, 0), (255, 255, 255)) # printing text object
textActivateGreenRect = textActivateGreen.get_rect()
textActivateGreenRect.center = (xc-32, yc+200)
textDeactivateGreen = fontGun.render('de-activate', True, (0, 255, 0), (255, 255, 255)) # printing text object
textDeactivateGreenRect = textDeactivateGreen.get_rect()
textDeactivateGreenRect.center = (xc+69, yc+200)

textScore = fontTitle.render('Score', True, (0, 0, 0), (255, 255, 255)) # printing text object
textScoreRect = textScore.get_rect()
textScoreRect.center = (xc, yc-200) 

fontTable = pygame.font.Font('freesansbold.ttf', 20) # printing text font and font size
textKPM = fontTable.render('Kills per minute:', True, (0, 0, 0), (255, 255, 255)) # printing text object
textKPMRect = textKPM.get_rect()
textKPMRect.center = (xc, yc-100) 

textCPM = fontTable.render('Kills of civilians per minute:', True, (0, 0, 0), (255, 255, 255)) # printing text object
textCPMRect = textCPM.get_rect()
textCPMRect.center = (xc, yc-50) 

textBPM = fontTable.render('Bullets per minute:', True, (0, 0, 0), (255, 255, 255)) # printing text object
textBPMRect = textBPM.get_rect()
textBPMRect.center = (xc, yc)  

textMAE = fontTable.render('MAE from target center:', True, (0, 0, 0), (255, 255, 255)) # printing text object
textMAERect = textMAE.get_rect()
textMAERect.center = (xc, yc+50) 

textRestart = fontTable.render('Press \'z\' for restart', True, (0, 0, 0), (255, 255, 255)) # printing text object
textRestartRect = textRestart.get_rect()
textRestartRect.center = (xc, yc+150)

textSave = fontTable.render('Press \'s\' to save score', True, (0, 0, 0), (255, 255, 255)) # printing text object
textSaveRect = textSave.get_rect()
textSaveRect.center = (xc, yc+200)


window_scale = 3 # conversion from meters to pixels. Not sure if we need it

clock = pygame.time.Clock() # initialise clock

dts = 0.01
FPS = int(1 / dts)

# VARIABLES ABOUT ELEMENTS OF THE SIMULATION (targets, forces, CGI elements and so on...)
x_rand = random.randint(50, 750)
y_rand = random.randint(50, 300)

k = 1
b = 1
radius = 25
killCount = 0
bulletCount = 0
civilianCount = 0

shooting = False # variable for the recoil, if true a recoil force is implemented
recoil_duration = 0 # variable used later to select the duration of the force pulse
recoil_on = 0 # variable to activate or de-active recoil

gun = "empty"
timeCountdown = 30

# some variables needed to define the forces
fe = np.zeros(2)
xh_old = np.zeros(2)
velocity_device = np.zeros(2)
v = np.random.rand(2) # random vector
v_hat = v / np.linalg.norm(v) # random unit vector to choose the direction of the wind

target_num = 1
target_list=[]
for i in range(target_num):
    target = Target(True)
    target_list.append(target)

civilian_num = 4
civilian_list=[]
for i in range(civilian_num):
    civilian = Target(False)
    civilian_list.append(civilian)


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
                if event.key == ord('1'): # activate/de-activate recoil
                    if recoil_on == 1:
                        recoil_on = 0
                    else:
                        recoil_on = 1  
                if event.key == ord('s'): # select sniper
                    setTimer = 1
                    gun = "sniper"
                    startscreen = False
                    score = 0
                    minDistanceList = []  # create empty minDistanceList
                if event.key == ord('r'): # select rifle
                    setTimer = 1
                    gun = "rifle"
                    startscreen = False
                    score = 0
                    minDistanceList = []  # create empty minDistanceList
                if event.key == ord('p'): # select pistol
                    setTimer = 1
                    gun = "pistol"
                    startscreen = False
                    score = 0
                    minDistanceList = []  # create empty minDistanceList
        
        # real-time plotting
        window.fill((255, 255, 255)) # clear window
        
        # plot text to screen
        window.blit(title, titleRect)
        window.blit(textChoice, textChoiceRect)
        window.blit(textSniper1, textSniper1Rect)
        window.blit(textSniper2, textSniper2Rect)
        window.blit(textRifle1, textRifle1Rect)
        window.blit(textRifle2, textRifle2Rect)
        window.blit(textPistol1, textPistol1Rect)
        window.blit(textPistol2, textPistol2Rect)
        window.blit(textRecoil, textRecoilRect)
        if recoil_on == 1:  #recoil is activated
            window.blit(textActivateGreen, textActivateGreenRect)
        else:  #recoil is de-activated
            window.blit(textDeactivateGreen, textDeactivateGreenRect)
        
        # plot images
        window.blit(imageSniper, imageSniperRect)
        window.blit(imageRifle, imageRifleRect)
        window.blit(imagePistol, imagePistolRect)
        
        pygame.display.flip() # update display
    '''*********** !STARTSCREEN ***********'''    
    
    # quit loop if window has been closed
    if run == False:  
        break
    
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
        
    
    '''************* TASK *************'''
    for event in pygame.event.get(): # interrupt function
        if event.type == pygame.QUIT: # force quit with closing the window
            run = False
        elif event.type == pygame.KEYUP:
            if event.key == ord('q'): # force quit with q button
                run = False
            if event.key == pygame.K_SPACE: # shoot with 'space' button
                bulletCount += 1
                hit_smth= False
                shooting = True
                recoil_duration = 12
                
                distanceList = []  # create empty distance list
                for target in target_list:
                    distance = math.sqrt(((target.pos[0]-xh[0])**2)+((target.pos[1]-xh[1])**2))
                    distanceList.append(distance)
                    if np.sqrt((xh[0]-int(target.pos[0]))**2 + (xh[1] -int(target.pos[1]))**2)<radius:
                        target.hit()
                        killCount += 1
                        score += 50
                        hit_smth= True
                        
                minDistance = min(distanceList)
                minDistanceList.append(minDistance)
                        
                for civ in civilian_list:
                    if np.sqrt((xh[0]-int(civ.pos[0]))**2 + (xh[1] -int(civ.pos[1]))**2)<radius:
                        civ.hit()
                        civilianCount += 1
                        score -= 100
                        hit_smth= True
                
                if not hit_smth:
                    score -= 20
           
    # start timer
    if setTimer == 1:
        timerStart = time.perf_counter()
        timerEnd = timerStart + timeCountdown  # define time of timer
        setTimer = 0
        killCount = 0
        bulletCount = 0
        civilianCount = 0
    
    # end timer
    if  time.perf_counter() >= timerEnd:
        endscreen = True
    
    countdown = round(timerEnd-time.perf_counter(), 1)
    
    if gun == 'sniper':
        # define the features of the gun
        f_viscosity = 4*b*velocity_device
        f_gravity = np.array([0, -5])
        
        if shooting or (recoil_duration > 0):
            f_recoil = np.array([0, 100])
            recoil_duration -= 1
            shooting = False
        else:
            f_recoil = np.zeros(2)
        # ...
        # change gun image
        imageGun = imageSniperSmall
        imageGunRect = imageSniperSmall.get_rect()
        imageGunRect.topright = (795, 5)
        weapon_n = 2
    
    if gun == 'rifle':
        # define the features of the gun
        f_viscosity = 1*velocity_device
        f_gravity = np.array([0, -2.5])
        
        if shooting or (recoil_duration > 0):
            f_recoil = np.array([0, 5])
            recoil_duration -= 1
            shooting = False
        else:
            f_recoil = np.zeros(2)
        # ...
        # change gun image
        imageGun = imageRifleSmall
        imageGunRect = imageRifleSmall.get_rect()
        imageGunRect.topright = (795, 5)
        weapon_n = 1
    
    if gun == 'pistol':
        # define the features of the gun
        f_viscosity = np.zeros(2)
        f_gravity = np.zeros(2)
        
        if shooting or (recoil_duration > 0):
            f_recoil = np.array([0, 0])
            recoil_duration -= 1
            shooting = False
        else:
            f_recoil = np.zeros(2)
        # ...
        # change gun image
        imageGun = imagePistolSmall
        imageGunRect = imagePistolSmall.get_rect()
        imageGunRect.topright = (795, 5)
        weapon_n = 0
    
    # real-time plotting
    window.fill((255,255,255)) # clear window
    window.blit(imageBgd1, (0, 0))
    
    # plot time
    textTime = font.render('Time: '+ str(countdown), True, (255, 0, 0))
    window.blit(textTime, textTimeRect)
    
    # plot kill count
    textHits = font.render('HITS: '+ str(killCount), True, (255, 0, 0))
    window.blit(textHits, textHitsRect)
    
    #plot current score
    textCurrScore = fontCurrScore.render('Score: '+ str(score), True, (255, 0, 0))
    window.blit(textCurrScore, textCurrScoreRect)
    
    window.blit(textShoot, textShootRect)
    
    # plot target
    target_pos=[]
    for target in target_list:
        x_pos = int(target.pos[0])
        y_pos = int(target.pos[1])
        if 800-x_pos<1+target_radius  or x_pos<1+target_radius:
            target.bounce_lr()
        if 600-y_pos<1+target_radius or y_pos<1+target_radius:
            target.bounce_tb()
        target.update_pos()
        target_pos.append(target.pos)
        window.blit(imageTarget, (x_pos-target_radius, y_pos-target_radius))

    civilian_pos=[]
    for civilian in civilian_list:
        x_pos = int(civilian.pos[0])
        y_pos = int(civilian.pos[1])
        if 800 - x_pos < 1 + target_radius or x_pos < 1 + target_radius:
            civilian.bounce_lr()
        if 600 - y_pos < 1 + target_radius or y_pos < 1 + target_radius:
            civilian.bounce_tb()
        civilian.update_pos()
        civilian_pos.append(civilian.pos)
        window.blit(imageCivilian, (x_pos - target_radius, y_pos - target_radius))
          
    window.blit(imageCross, (xh[0]-crossSize/2, xh[1]-crossSize/2))
    pygame.draw.circle(window, (0, 255, 0), (xh[0], xh[1]), 5) # draw a green point for aiming
    window.blit(imageGun, imageGunRect)
    pygame.display.flip() # update display
    
    # COMPUTING FEEDBACK FORCES AND PERTURBATIONS
    f_perturbance = np.multiply(np.array([np.sin(5*countdown) + 1.5, np.sin(5*countdown) + 1.5]), v_hat) # perturbation caused by multiple possible external 
    # factors: wind, hand shaking, etc.
    
    velocity_device = ((xh - xh_old)/dts)/(window_scale*1e3) # used for the f_viscosity
    f_viscosity = f_viscosity # the actual calculation of this force is done above where we check which weapon has been chosen.
    # this equivalence is useless, it is here just as a reminder of the force
    f_gravity = f_gravity # check comment of f_viscosity
    
    target_array = np.array(target_pos)
    civilian_array = np.array(civilian_pos)
    x_hm, y_hm, z_hm_targets = create_targets(window_dimension, target_array, weapon_n)
    x_hm, y_hm, z_hm_civilians = create_civilians(window_dimension, civilian_array)
    z_hm = z_hm_targets + z_hm_civilians
    
    gradient = np.array(np.gradient(z_hm))
    if weapon_n != 0:
        f_height_map = gradient[:, int(xh[0]/5), int(xh[1]/5)] * 1.1 * 1e4 * 13**(weapon_n - 1)
    else:
        f_height_map = np.zeros(2)
    #print(f_height_map)
    
    fe = f_viscosity + (f_recoil * recoil_on) + f_gravity + f_perturbance + f_height_map
    #print("f_perturbance:", f_perturbance)
    
    xh_old = xh # Update xh_old to compute the velocity
    
    ######### Send forces to the device #########
    if port:
        fe[1] = -fe[1]  ##Flips the force on the Y=axis 
        
        ##Update the forces of the device
        device.set_device_torques(fe)
        device.device_write_torques()
        #pause for 1 millisecond
        time.sleep(0.001)
    '''************* !TASK *************'''
    
    if endscreen:  # calculate metrics
        score_saved = False
        kills_per_minute = killCount*(60/timeCountdown)
        bullets_per_minute = bulletCount*(60/timeCountdown)
        civilians_per_minute = civilianCount*(60/timeCountdown)
        if bulletCount == 0: # to avoid errors due to the division by zero
            ResultMAE = 100000000
        else:
            ResultMAE =  round(sum(minDistanceList)/bulletCount, 2)
            
        score = score + int(3*1e4/ResultMAE)
        
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
                    civilian_list=[]
                    for i in range(civilian_num):
                        civilian = Target(False)
                        civilian_list.append(civilian)
                        
                if event.key == ord('s') and score_saved==False:
                    save_score(gun,kills_per_minute,bullets_per_minute,ResultMAE,score)
                    score_saved = True
        
        # real-time plotting
        window.fill((255,255,255)) # clear window
    
        # plot text to screen
        textScore = fontTitle.render('Score:  ' + str(score), True, (0, 0, 0), (255, 255, 255))
        textScoreRect = textScore.get_rect()
        textScoreRect.center = (xc, yc-200)
        window.blit(textScore, textScoreRect)
        
        textKPM = fontTable.render('Kills per minute: ' + str(kills_per_minute), True, (0, 0, 0), (255, 255, 255)) # printing text object
        textKPMRect = textKPM.get_rect()
        textKPMRect.center = (xc, yc-100) 
        window.blit(textKPM, textKPMRect)
        
        textCPM = fontTable.render('Kills of civilians per minute: ' + str(civilians_per_minute), True, (0, 0, 0), (255, 255, 255)) # printing text object
        textCPMRect = textCPM.get_rect()
        textCPMRect.center = (xc, yc-50) 
        window.blit(textCPM, textCPMRect)
        
        textBPM = fontTable.render('Bullets per minute: ' + str(bullets_per_minute), True, (0, 0, 0), (255, 255, 255)) # printing text object
        textBPMRect = textBPM.get_rect()
        textBPMRect.center = (xc, yc)  
        window.blit(textBPM, textBPMRect)
        
        textMAE = fontTable.render('MAE from target center: ' + str(ResultMAE) + ' [in pixel]', True, (0, 0, 0), (255, 255, 255)) # printing text object
        textMAERect = textMAE.get_rect()
        textMAERect.center = (xc, yc+50)
        window.blit(textMAE, textMAERect)
        
        window.blit(textRestart, textRestartRect)
        window.blit(textSave, textSaveRect)
        
        pygame.display.flip() # update display
    '''*********** !ENDSCREEN ***********'''
    
    # try to keep it real time with the desired step time
    clock.tick(FPS)
    
    if run == False:
        break
    
pygame.quit() # stop pygame


