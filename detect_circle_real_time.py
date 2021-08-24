import cv2
from detect_distance import GetDistance

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

    cap1 = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    cap1.set(cv2.CAP_PROP_BUFFERSIZE, 2)
    cap2 = cv2.VideoCapture(1,cv2.CAP_DSHOW)
    cap2.set(cv2.CAP_PROP_BUFFERSIZE, 2)

    getdistance = GetDistance(cam_width,cam_angle)
    print("Start of loop")

    while True:
        ret1, img1 = cap1.read()
        ret2, img2 = cap2.read()

        getdistance.next_frame(img1,img2)
        getdistance.process_circle()
        getdistance.printdata()
        distance = getdistance.getdistance()

        circles1, circles2 = getdistance.getcircle()
        
        if circles1 is not None and circles2 is not None:   

            for (x, y, r) in circles1:
                cv2.circle(img1, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(img1, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

            for (x, y, r) in circles2:
                cv2.circle(img2, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(img2, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

        cv2.putText(img1,"d1 = "+str(abs(distance)), 
        locationText1, 
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
  