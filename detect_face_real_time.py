import cv2
import os
import keyboard
import errno
import time
import sys
import math
import numpy as np

def main():
    cam_angle = 60
    cam_width = 7.2 #width between two cameras in cm  closest=7.2

    font                   = cv2.FONT_HERSHEY_SIMPLEX
    locationText1 = (0,20)
    locationText2 = (0,60)
    locationText3 = (0,100)
    fontScale              = 1
    fontColor              = (0,0,255)
    lineType               = 2
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_alt.xml')

    cap1 = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    cap1.set(cv2.CAP_PROP_BUFFERSIZE, 2)
    cap2 = cv2.VideoCapture(1,cv2.CAP_DSHOW)
    cap2.set(cv2.CAP_PROP_BUFFERSIZE, 2)

    print("Start of loop")

    while True:
        ret1, img1 = cap1.read()
        ret2, img2 = cap2.read()

        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        faces1 = face_cascade.detectMultiScale(gray1, 1.1, 4)
        faces2 = face_cascade.detectMultiScale(gray2, 1.1, 4)

        if len(faces1) and len(faces2):
            x1,y1,w1,h1=faces1[0]
            cv2.rectangle(img1, (x1, y1), (x1+w1, y1+h1), (0, 255, 0), 2)

            x2,y2,w2,h2=faces2[0]
            cv2.rectangle(img2, (x2, y2), (x2+w2, y2+h2), (255, 0, 0), 2)
            cv2.rectangle(img1, (x2, y2), (x2+w2, y2+h2), (255, 0, 0), 2)

            height1, width1 = img1.shape[:2]
            height2, width2 = img2.shape[:2]

            # cam1_left_angle = 180-cam_angle-x1/width1*cam_angle
            # cam2_left_angle = (180-cam_angle)/2+x2/width2*cam_angle
            cam2_left_angle = (180-cam_angle)/2+x2/width2*cam_angle
            cam1_left_angle = (180-cam_angle)/2+x1/width1*cam_angle
            cam2_right_angle = (180-cam_angle)/2+(x2+w2)/width2*cam_angle
            cam1_right_angle = (180-cam_angle)/2+(x1+w1)/width1*cam_angle
            cam2_mid_angle = (180-cam_angle)/2+(x2+w2/2)/width2*cam_angle
            cam1_mid_angle = (180-cam_angle)/2+(x1+w1/2)/width1*cam_angle

            if(cam1_left_angle >= 90):
                cam1_left_angle = -(cam1_left_angle - 90)
            else:
                cam1_left_angle = 90 - cam1_left_angle

            if(cam2_left_angle >= 90):
                cam2_left_angle = -(cam2_left_angle - 90)
            else:
                cam2_left_angle = 90 - cam2_left_angle

            if(cam1_right_angle >= 90):
                cam1_right_angle = -(cam1_right_angle - 90)
            else:
                cam1_right_angle = 90 - cam1_right_angle

            if(cam2_right_angle >= 90):
                cam2_right_angle = -(cam2_right_angle - 90)
            else:
                cam2_right_angle = 90 - cam2_right_angle

            if(cam1_mid_angle >= 90):
                cam1_mid_angle = -(cam1_mid_angle - 90)
            else:
                cam1_mid_angle = 90 - cam1_mid_angle

            if(cam2_mid_angle >= 90):
                cam2_mid_angle = -(cam2_mid_angle - 90)
            else:
                cam2_mid_angle = 90 - cam2_mid_angle

            try:
                distance1 = cam_width / (math.tan(cam2_left_angle*math.pi/180)-math.tan(cam1_left_angle*math.pi/180))
                distance2 = cam_width / (math.tan(cam2_right_angle*math.pi/180)-math.tan(cam1_right_angle*math.pi/180))
                distance_mid = cam_width / (math.tan(cam2_mid_angle*math.pi/180)-math.tan(cam1_mid_angle*math.pi/180))
            except ZeroDivisionError:
                print("ZeroDivisionError")

            print("cam1_left_angle = "+str(cam1_left_angle)+" cam1_right_angle = "+str(cam1_right_angle)+"cam2_left_angle = "+str(cam2_left_angle)+" cam2_right_angle = "+str(cam2_right_angle))
            # print("distance1 = "+str(abs(distance1))+" distance2 = "+str(abs(distance2)))
            cv2.putText(img1,"d1 = "+str(abs(distance1)), 
            locationText1, 
            font, 
            fontScale,
            fontColor,
            lineType)
            cv2.putText(img1,"d2 = "+str(abs(distance2)), 
            locationText3, 
            font, 
            fontScale,
            fontColor,
            lineType)
            cv2.putText(img1,"d2 = "+str(abs(distance_mid)), 
            locationText2, 
            font, 
            fontScale,
            fontColor,
            lineType)


        if ret1:
            cv2.imshow('frame1', img1)
        if ret2:
            cv2.imshow('frame2', img2)

        
        

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break 

    print("End of loop")

    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
  