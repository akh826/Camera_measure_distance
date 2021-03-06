import argparse
import dlib
import cv2
import os
import sys
from GetDistance import GetDistance

def main():
    cam_angle = 60
    cam_width = 7.2 #width between two cameras in cm  closest=7.2

    font                   = cv2.FONT_HERSHEY_SIMPLEX
    locationText2 = (0,30)
    fontScale              = 1
    fontColor              = (0,0,255)
    lineType               = 2
    
    cap1 = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    cap1.set(cv2.CAP_PROP_BUFFERSIZE, 2)
    cap2 = cv2.VideoCapture(1,cv2.CAP_DSHOW)
    cap2.set(cv2.CAP_PROP_BUFFERSIZE, 2)

    getdistance = GetDistance(cam_width,cam_angle, 1280, 720)
    print("Start of loop")

    while True:
        ret1, img1 = cap1.read()
        ret2, img2 = cap2.read()

        if(ret1 and ret2):
            getdistance.next_frame(img1,img2)
            getdistance.process_face_landmarks()
            distance = getdistance.getdistance()

            nose1,nose2 = getdistance.getnose()
            if(nose1 is not None and nose2 is not None):
                cv2.circle(img1, nose1, 3, (0, 0, 255), -1)
                cv2.circle(img2, nose2, 3, (0, 0, 255), -1)

            cv2.putText(img1,"d = "+str(abs(int(distance))), 
                locationText2, 
                font, 
                fontScale,
                fontColor,
                lineType)
            cv2.imshow('frame1', img1)
            cv2.imshow('frame2', img2)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break 

    print("End of loop")

    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
  