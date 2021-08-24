import cv2
import os
import sys
from GetDistance import GetDistance

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
        img1 = cv2.imread(os.path.join(Cap_image_dir1,cam1_image[no])) 
        img2 = cv2.imread(os.path.join(Cap_image_dir2,cam2_image[no])) 

        getdistance.next_frame(img1,img2)
        getdistance.process_face()
        getdistance.printdata()
        distance = getdistance.getdistance()

        faces1,faces2 = getdistance.getface()
        if(faces1 is not None and faces2 is not None):
            x1,y1,w1,h1=faces1[0]
            cv2.rectangle(img1, (x1, y1), (x1+w1, y1+h1), (0, 255, 0), 2)

            x2,y2,w2,h2=faces2[0]
            cv2.rectangle(img2, (x2, y2), (x2+w2, y2+h2), (255, 0, 0), 2)
            cv2.rectangle(img1, (x2, y2), (x2+w2, y2+h2), (255, 0, 0), 2)

        cv2.putText(img1,"d = "+str(abs(distance)), 
            locationText2, 
            font, 
            fontScale,
            fontColor,
            lineType)


        cv2.imshow("Cam1", img1)
        cv2.imshow("Cam2", img2)
      

        if cv2.waitKey(0) & 0xFF == ord('q'):
            break 

if __name__ == '__main__':
    main()
  
  