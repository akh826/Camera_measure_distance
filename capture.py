import cv2
import os
import keyboard
import errno
import time

# Logitech C505 HD WEBCAM 
    # Height: 31.91 mm
    # Width: 72.91 mm
    # Depth: 66.64 mm
    # Cable length: 2 m
    # Weight: 75 g
# Technical Specifications
    # Max Resolution: 720p/30fps
    # Camera mega pixel: 1.2
    # Focus type: Fixed
    # Lens type: plastic
    # Built-in mic: mono
    # Mic range: Up to 2.74 m
    # Diagonal field of view (dFoV): 60°
    # Universal mounting clip fits laptops, LCD or monitors

# camera2 > (left) camera1 > (right)
#       c1  c2
#        ^  ^
#       / \/ \
#      /  /\  \
#     /  /  \  \
def main():
    camera1 = 0
    camera2 = 2
    directory = os.getcwd()
    image_floder1 =r'Cap_image_cam1'
    image_floder2 =r'Cap_image_cam2'
    try:
        os.mkdir(image_floder1)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass

    try:
        os.mkdir(image_floder2)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass

    Cap_image_dir1 = os.path.join(directory,image_floder1)
    Cap_image_dir2 = os.path.join(directory,image_floder2)
    count = 0
    # os.chdir(Cap_image_dir)

    cap1 = cv2.VideoCapture(camera1,cv2.CAP_DSHOW)
    cap1.set(cv2.CAP_PROP_BUFFERSIZE, 2)
    cap2 = cv2.VideoCapture(camera2,cv2.CAP_DSHOW)
    cap2.set(cv2.CAP_PROP_BUFFERSIZE, 2)

    print("Start of loop")

    while True:
        print("looping "+str(cap1.isOpened())+" "+str(cap2.isOpened())+" "+str(time.time()))
        ret1, frame1 = cap1.read()
        if ret1:
            cv2.imshow('frame1', frame1)
        ret2, frame2 = cap2.read()
        if ret2:
            cv2.imshow('frame2', frame2)

        if keyboard.is_pressed('c'):
            filename1 = str(count)+'cam1_'+'.png'
            filename2 = str(count)+'cam2_'+'.png'
            os.chdir(Cap_image_dir1)
            cv2.imwrite(filename1, frame1)
            os.chdir(Cap_image_dir2)
            cv2.imwrite(filename2, frame2)
            count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break 

    print("End of loop")

    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
  