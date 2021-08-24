import cv2
import os
import sys
import math
import numpy as np

class GetDistance():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_alt.xml')
    
    def __init__(self, cam_width,cam_angle):
        self.cam_width = cam_width
        self.cam_angle = cam_angle

        self.distance = 0
        self.cam1_angle = 0
        self.cam2_angle = 0

        self.circles1_result = None
        self.circles2_result = None
        self.faces1 = None
        self.faces2 = None
        

    def process_circle(self):
        gray1 = cv2.cvtColor(self.img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(self.img2, cv2.COLOR_BGR2GRAY)
        circles1 = cv2.HoughCircles(gray1, cv2.HOUGH_GRADIENT, 1.2, 100)
        circles2 = cv2.HoughCircles(gray2, cv2.HOUGH_GRADIENT, 1.2, 100)
        if(circles1 is not None and circles2 is not None):
            self.circles1_result = np.round(circles1[0, :]).astype("int")
            self.circles2_result = np.round(circles2[0, :]).astype("int")
            x1 = self.circles1_result[0][0]  #circle centre x
            # y1 = self.circles1_result[0][1]  #circle centre y
            x2 = self.circles2_result[0][0]  #circle centre x
            # y2 = self.circles2_result[0][1]  #circle centre y
            self.cam2_angle = (180-self.cam_angle)/2+x2/self.width2*self.cam_angle
            self.cam1_angle = (180-self.cam_angle)/2+x1/self.width1*self.cam_angle

            if(self.cam1_angle >= 90):
                self.cam1_angle = -(self.cam1_angle - 90)
            else:
                self.cam1_angle = 90 - self.cam1_angle

            if(self.cam2_angle >= 90):
                self.cam2_angle = -(self.cam2_angle - 90)
            else:
                self.cam2_angle = 90 - self.cam2_angle

            try:
                self.distance = self.cam_width / (math.tan(self.cam2_angle*math.pi/180)-math.tan(self.cam1_angle*math.pi/180))
            except ZeroDivisionError:
                print("ZeroDivisionError")
        else:
            self.circles1_result = None
            self.circles2_result = None
            self.distance = 0
            self.cam1_angle = 0
            self.cam2_angle = 0

    def process_face(self):
        
        gray1 = cv2.cvtColor(self.img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(self.img2, cv2.COLOR_BGR2GRAY)

        self.faces1 = self.face_cascade.detectMultiScale(gray1, 1.1, 4)
        self.faces2 = self.face_cascade.detectMultiScale(gray2, 1.1, 4)

        if(len(self.faces1) and len(self.faces2)):
        # if(self.faces1 is not None and self.faces2 is not None):
            self.cam2_angle = (180-self.cam_angle)/2+(self.faces2[0][0]+self.faces2[0][3]/2)/self.width2*self.cam_angle
            self.cam1_angle = (180-self.cam_angle)/2+(self.faces1[0][0]+self.faces1[0][3]/2)/self.width1*self.cam_angle

            if(self.cam2_angle >= 90):
                self.cam2_angle = -(self.cam2_angle - 90)
            else:
                self.cam2_angle = 90 - self.cam2_angle

            if(self.cam1_angle >= 90):
                self.cam1_angle = -(self.cam1_angle - 90)
            else:
                self.cam1_angle = 90 - self.cam1_angle

            try:
                self.distance = self.cam_width / (math.tan(self.cam2_angle*math.pi/180)-math.tan(self.cam1_angle*math.pi/180))
            except ZeroDivisionError:
                print("ZeroDivisionError")
        else:
            self.faces1 = None
            self.faces2 = None
            self.distance = 0
            self.cam1_angle = 0
            self.cam2_angle = 0

    def next_frame(self,img1,img2):
        self.img1 = img1
        self.img2 = img2
        self.height1, self.width1 = self.img1.shape[:2]
        self.height2, self.width2 = self.img2.shape[:2]

    def getface(self):
        if(self.faces1 is not None and self.faces2 is not None):
            return self.faces1,self.faces2
        return None,None

    def getcircle(self):
        if(self.circles1_result is not None and self.circles2_result is not None):
            return self.circles1_result,self.circles2_result
        return None,None

    def getcamangle(self):
        return self.cam1_angle,self.cam2_angle

    def getdistance(self):
        return self.distance
    
    def printdata(self):
        if(self.cam1_angle is not None and self.cam2_angle is not None and self.distance is not None):
            print("cam1_angle = "+str(self.cam1_angle)+"cam2_angle = "+str(self.cam2_angle))
            print (f"d = {self.distance}")
    


def main():
    font = cv2.FONT_HERSHEY_SIMPLEX
    locationText2 = (0,60)
    fontScale              = 1
    fontColor              = (0,0,255)
    lineType               = 2

    cam_angle = 60
    cam_width = 7.2 #width between two cameras in cm

    directory = os.getcwd()
    image_floder1 =r'Cap_image_cam1'
    image_floder2 =r'Cap_image_cam2'

    Cap_image_dir1 = os.path.join(directory,image_floder1)
    Cap_image_dir2 = os.path.join(directory,image_floder2)

    if not (os.path.exists(image_floder1) and os.path.exists(image_floder2)):
        sys.exit()

    cam1_image = os.listdir(Cap_image_dir1)
    cam2_image = os.listdir(Cap_image_dir2)
    getdistance = GetDistance(cam_width,cam_angle)

    for no in range(len(cam1_image)):
        print(cam1_image[no]+" "+cam2_image[no])
        img1 = cv2.imread(os.path.join(Cap_image_dir1,cam1_image[no])) 
        img2 = cv2.imread(os.path.join(Cap_image_dir2,cam2_image[no])) 

        getdistance.next_frame(img1,img2)
        # getdistance.process_face()
        getdistance.process_circle()
        getdistance.printdata()
        distance = getdistance.getdistance()

        cv2.putText(img1,"d = "+str(abs(distance)), 
            locationText2, 
            font, 
            fontScale,
            fontColor,
            lineType)

        # print(str(d1)+" "+str(d2))


        cv2.imshow("Cam1", img1)
        cv2.imshow("Cam2", img2)
      

        if cv2.waitKey(0) & 0xFF == ord('q'):
            break 

if __name__ == '__main__':
    main()
  