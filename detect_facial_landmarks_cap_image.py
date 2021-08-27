import argparse
import dlib
import cv2
import os
import sys
from GetDistance import GetDistance

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# load the input image, resize it, and convert it to grayscale
font = cv2.FONT_HERSHEY_SIMPLEX
locationText2 = (0,30)
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
getdistance = GetDistance(cam_width,cam_angle, 1280, 720)


for no in range(len(cam1_image)):
    img1 = cv2.imread(os.path.join(Cap_image_dir1,cam1_image[no])) 
    img2 = cv2.imread(os.path.join(Cap_image_dir2,cam2_image[no])) 

    getdistance.next_frame(img1,img2)
    getdistance.process_face_landmarks()
    distance = getdistance.getdistance()

    shape1,shape2  = getdistance.getshape()

    for (x, y) in shape1:
        cv2.circle(img1, (x, y), 1, (0, 0, 255), -1)
    for (x, y) in shape2:
        cv2.circle(img2, (x, y), 1, (0, 0, 255), -1)
    
    if(shape1 is not None and shape2 is not None):
        cv2.circle(img1, shape1[30], 3, (0, 255, 0), -1)
        cv2.circle(img2, shape2[30], 3, (0, 255, 0), -1)

    cv2.putText(img1,"d = "+str(abs(int(distance))), 
        locationText2, 
        font, 
        fontScale,
        fontColor,
        lineType)


    cv2.imshow("Cam1", img1)
    cv2.imshow("Cam2", img2)
      
    if cv2.waitKey(0) & 0xFF == ord('q'):
            break 