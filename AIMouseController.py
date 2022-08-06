from enum import auto
import time
import numpy as np
import cv2
import handTrackingModule as htm
import autopy

cap = cv2.VideoCapture(0)

width_cam,height_cam = 640 ,480
cap.set(3, width_cam)
cap.set(4, height_cam)
frameReduction = 100
width_screen , height_screen = autopy.screen.size()
smooth_vlaue = 5
previous_locationX , previous_locationY = 0 , 0
current_locationX , currrent_locationY = 0 , 0

previous_time = 0 
detector = htm.HandDetector(detConfidence= 0.75 ,maxHands= 1)
while True:
    success,img =  cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw= False)
    if len(lmList) !=0 :
        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]

        fingers = detector.fingerUp()
        cv2.rectangle(img , (frameReduction ,frameReduction) , (width_cam - frameReduction , height_cam -frameReduction) , (255,0,255) , 3   )
        # Mouse Move
        if fingers[1]  == 1  and fingers[2] == 0:
            x3  = np.interp(x1 , (frameReduction,width_cam -frameReduction) , (0 , width_screen) )   
            y3  = np.interp(y1 , (frameReduction,height_cam - frameReduction) , (0 , height_cam) )    
            # smooth values
            current_locationX = previous_locationX + (x3 -previous_locationX) / smooth_vlaue
            current_locationY = previous_locationY + (y3 -previous_locationY) / smooth_vlaue
            cv2.circle(img,(x1 , y1) , 15 , (255,0,255) , cv2.FILLED)
            previous_locationX ,previous_locationY  = current_locationX ,current_locationY
            autopy.mouse.move(width_screen- current_locationX , current_locationY)   
        # Mouse Click
        if fingers[1]  == 1  and fingers[2] == 1:
            line_length , img, line_info = detector.find_distance(img,8 ,12 )
            if(line_length <25):
                cv2.circle(img,(line_info[4] , line_info[5]) , 15 , (0,255,0) , cv2.FILLED)
                autopy.mouse.click()
    current_time = time.time()
    fbs = 1 / (current_time - previous_time)
    previous_time = current_time

    img = cv2.flip(img,1)
    cv2.putText(img, f' FBS: {int(fbs) }' , (20 , 80) , cv2.FONT_HERSHEY_PLAIN , 3 , (0,255,0) , 3)
    cv2.imshow("Image" , img)
    cv2.waitKey(1)