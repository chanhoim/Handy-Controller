from cv2 import cv2
import mediapipe
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)  # 0 for webcam
detector = HandDetector(detectionCon=0.8, maxHands=2)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # flip for webcam
    hands, img = detector.findHands(img, flipType=False)

    cv2.imshow("MultiHand", img)
    cv2.waitKey(1)
