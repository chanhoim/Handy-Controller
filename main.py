from cv2 import cv2
import time
import mediapipe
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)  # 0 for webcam
detector = HandDetector(detectionCon=0.8, maxHands=2)
pTime = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # flip for webcam
    hands, img = detector.findHands(img, flipType=False)

    # show fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 30), cv2.FONT_HERSHEY_PLAIN, 1.5,
                (0, 255, 0), 2)

    cv2.imshow("MultiHand", img)
    cv2.waitKey(1)
