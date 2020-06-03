from controller import Robot
import numpy as np
import cv2
from controller import Camera
import imutils
import time

robot = Robot()

timestep = int(robot.getBasicTimeStep())
leftMotor = robot.getMotor('left wheel motor')
rightMotor = robot.getMotor('right wheel motor')

leftMotor.setPosition(float('+inf'))
rightMotor.setPosition(float('+inf'))

maxSpeed = min(rightMotor.getMaxVelocity(), leftMotor.getMaxVelocity())
#maxSpeed=5
cam = robot.getCamera('camera')
cam.enable(1)
aap = 1.5
def Motor_steer (kt, predkosc, sterowanie):
    if sterowanie == 0 :
        leftMotor.setVelocity(predkosc)
        rightMotor.setVelocity(predkosc)
        return
    elif sterowanie > 0:
        sterowanie = 100 - sterowanie
        sterowanie = 100 - sterowanie
        if kt<0:
            kt=kt*-1
        kt=(kt*100)/180
        kt=kt*aap
        kt=100-kt
        leftMotor.setVelocity(predkosc*kt/100)
        rightMotor.setVelocity((predkosc*kt/100)*sterowanie/100)        
        return
    elif sterowanie < 0:
        sterowanie = sterowanie * -1        
        sterowanie = 100 - sterowanie
        if kt<0:
            kt=kt*-1
        kt=(kt*100)/180
        kt=kt*aap 
        kt=100-kt
        x=predkosc*kt/100
        leftMotor.setVelocity((predkosc*kt/100)*sterowanie/100)
        rightMotor.setVelocity(predkosc*kt/100 )     
        return
kp= .8
ap = 1

start_time=time.time()
counter=0
while robot.step(timestep) != -1:
    counter+=1
    obraz = cam.getImageArray()
    obraz2 = np.array(obraz, dtype=np.uint8)    
    obraz2 = imutils.rotate(obraz2,-90)    
    obraz3 = cv2.flip(obraz2, 1)
    obraz3 = obraz3[20:90,0:119]
    
    czarnalinia = cv2.inRange(obraz3, (0,0,0), (110,110,110))
    contours, hierarchy = cv2.findContours(czarnalinia.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(obraz3, contours,-1,(0,255,0), 3)
    
    if len(contours)>0:    
        x,y,w,h = cv2.boundingRect(contours[0])  
        cv2.rectangle(obraz3,(x,y),(x+w,y+h),(255,0,0),2)
        
        k = cv2.minAreaRect(contours[0])
        (x1,y1), (x2,y2), kat = k        
        if kat <-45:
            kat = 90+kat
        if x2 < y2 and kat > 0:
            kat = (90-kat)*-1
        if x2 > y2 and kat < 0:
            kat = 90 + kat          
        srodek = 80  
        blad = int(x1 - srodek)
        kat = int(kat)
        Motor_steer(kat,maxSpeed,(blad*kp)+(kat*ap))        
        box = cv2.boxPoints(k)
        box = np.int0(box)
                
        cv2.drawContours(obraz3, [box],0,(0,0,255),2)
        cv2.putText(obraz3,str(kat),(25,20),cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,0,0), 1)
        
            
        cv2.line(obraz3, (int(x1), 40), (int(x1), 60), (255,0,0), 3) 
        centertext = "blad = "+ str(blad)
        cv2.putText(obraz3, centertext, (5,25), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,0,255), 1)
    
    cv2.imshow('obraz3',obraz3)
    cv2.imshow('black',czarnalinia)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
finish_time=time.time()
fps=counter/(finish_time-start_time)
print("fps: " + str(fps))
