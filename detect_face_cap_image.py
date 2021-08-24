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
    cam_width = 7.2 #width between two cameras in cm

    directory = os.getcwd()
    image_floder1 =r'Cap_image_cam1'
    image_floder2 =r'Cap_image_cam2'

    Cap_image_dir1 = os.path.join(directory,image_floder1)
    Cap_image_dir2 = os.path.join(directory,image_floder2)
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_alt.xml')

    if not (os.path.exists(image_floder1) and os.path.exists(image_floder2)):
        sys.exit()

    cam1_image = os.listdir(Cap_image_dir1)
    cam2_image = os.listdir(Cap_image_dir2)

    for no in range(len(cam1_image)):
        print(cam1_image[no]+" "+cam2_image[no])
        img1 = cv2.imread(os.path.join(Cap_image_dir1,cam1_image[no])) 
        img2 = cv2.imread(os.path.join(Cap_image_dir2,cam2_image[no])) 

        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        faces1 = face_cascade.detectMultiScale(gray1, 1.1, 4)
        faces2 = face_cascade.detectMultiScale(gray2, 1.1, 4)

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

        try:
            distance1 = cam_width / (math.tan(cam2_left_angle*math.pi/180)-math.tan(cam1_left_angle*math.pi/180))
            distance2 = cam_width / (math.tan(cam2_right_angle*math.pi/180)-math.tan(cam1_right_angle*math.pi/180))
        except ZeroDivisionError:
            print("ZeroDivisionError")


        # d1 = width2/2*math.tan(cam1_left_angle)/math.tan(cam_angle/2)
        # d2 = -width2/2*math.tan(cam2_left_angle)/math.tan(cam_angle/2)

        # distance = cam_width*math.sin(cam2_left_angle)/math.sin(cam2_left_angle-cam1_left_angle)
        # print("image width = "+str(width1)+" "+str(x2)+" "+str(x1))
        print("cam1_left_angle = "+str(cam1_left_angle)+" cam1_right_angle = "+str(cam1_right_angle)+"\n"+
        "cam2_left_angle = "+str(cam2_left_angle)+" cam2_right_angle = "+str(cam2_right_angle))
        print("distance1 = "+str(abs(distance1))+" distance2 = "+str(abs(distance2)))

        # print(str(d1)+" "+str(d2))


        cv2.imshow("Cam1", img1)
        cv2.imshow("Cam2", img2)
      

        if cv2.waitKey(0) & 0xFF == ord('q'):
            break 

    # cap1 = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    # cap1.set(cv2.CAP_PROP_BUFFERSIZE, 2)
    # cap2 = cv2.VideoCapture(1,cv2.CAP_DSHOW)
    # cap2.set(cv2.CAP_PROP_BUFFERSIZE, 2)

    # print("Start of loop")

    # while True:
    #     print("looping "+str(cap1.isOpened())+" "+str(cap2.isOpened())+" "+str(time.time()))
    #     ret1, frame1 = cap1.read()
    #     if ret1:
    #         cv2.imshow('frame1', frame1)
    #     ret2, frame2 = cap2.read()
    #     if ret2:
    #         cv2.imshow('frame2', frame2)

    #     if keyboard.is_pressed('c'):
    #         print("Before saving image:")  
    #         print(os.listdir(Cap_image_dir))  
    #         filename1 = 'cam1_'+str(count)+'.png'
    #         filename2 = 'cam2_'+str(count)+'.png'
    #         cv2.imwrite(filename1, frame1)
    #         cv2.imwrite(filename2, frame2)
    #         count += 1

    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break 

    # print("End of loop")

    # cap1.release()
    # cap2.release()
    # cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
  