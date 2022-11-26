import cv2 
import mediapipe

if __main__=="__main__":
    mycam= cv2.VideoCapture(0)

    while True:
        ret_val, frame= mycam.read()

        cv2.imshow("frame",frame)

        if cv2.waitKey(1) == 27:
            break

 