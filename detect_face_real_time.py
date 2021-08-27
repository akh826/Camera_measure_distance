import cv2
from GetDistance import GetDistance

def main():
    cam_angle = 60
    cam_width = 7.2 #width between two cameras in cm  closest=7.2

    font                   = cv2.FONT_HERSHEY_SIMPLEX
    locationText2 = (0,60)
    fontScale              = 1
    fontColor              = (0,0,255)
    lineType               = 2
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_alt.xml')

    cap1 = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    cap1.set(cv2.CAP_PROP_BUFFERSIZE, 2)
    cap2 = cv2.VideoCapture(1,cv2.CAP_DSHOW)
    cap2.set(cv2.CAP_PROP_BUFFERSIZE, 2)

    getdistance = GetDistance(cam_width,cam_angle, 1280, 720)
    print("Start of loop")

    while True:
        ret1, img1 = cap1.read()
        ret2, img2 = cap2.read()

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
  