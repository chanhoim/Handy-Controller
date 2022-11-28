from cv2 import cv2
import time
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(1)  # 0 for webcam, 1 for external
detector = HandDetector(detectionCon=0.8, maxHands=1)
pTime = 0

while True:
    success, img = cap.read()
    # img = cv2.flip(img, 1)  # flip for webcam
    hands, img = detector.findHands(img)

    if hands:
        # hand1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # list of 21 landmarks of points
        bbox1 = hand1["bbox"]  # bounding box info (x, y, w, h)
        centerPoint1 = hand1["center"]  # center of the hand cx, cy
        handType1 = hand1["type"]  # hand type (left or right)
        fingers1 = detector.fingersUp(hand1)

        print(f"{handType1} Hand, Center = {centerPoint1}, Fingers = {fingers1}")

    # show fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 30), cv2.FONT_HERSHEY_PLAIN, 1.5,
                (0, 255, 0), 2)

    cv2.imshow("main", img)
    cv2.waitKey(1)
