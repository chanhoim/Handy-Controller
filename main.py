from cv2 import cv2
import time
from HandTrackingModule import HandDetector

camInput = 1  # 0 for webcam, 1 for external source

cap = cv2.VideoCapture(camInput)
detector = HandDetector(detectionCon=0.8, maxHands=2)
pTime = 0
tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    if camInput == 0:
        img = cv2.flip(img, 1)  # flip for webcam
        hands, img = detector.findHands(img, flipType=False)  # flip type for webcam
    else:
        hands, img = detector.findHands(img)

    if hands:
        # hand1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # list of 21 landmarks of points
        bbox1 = hand1["bbox"]  # bounding box info (x, y, w, h)
        centerPoint1 = hand1["center"]  # center of the hand cx, cy
        handType1 = hand1["type"]  # hand type (left or right)
        fingers1 = detector.fingersUp(hand1)
        for id in range(1, 5):
            length, info, img = detector.findDistance(lmList1[4], lmList1[tipIds[id]], img)

        print(f"{handType1} Hand, Center = {centerPoint1}, Fingers = {fingers1}")

        if len(hands) == 2:
            # hand2
            hand2 = hands[1]
            lmList2 = hand2["lmList"]  # list of 21 landmarks of points
            bbox2 = hand2["bbox"]  # bounding box info (x, y, w, h)
            centerPoint2 = hand2["center"]  # center of the hand cx, cy
            handType2 = hand2["type"]  # hand type (left or right)
            fingers2 = detector.fingersUp(hand2)
            for id in range(1, 5):
                length, info, img = detector.findDistance(lmList2[4], lmList2[tipIds[id]], img)

            print(f"{handType2} Hand, Center = {centerPoint2}, Fingers = {fingers2}")
            print("")

    # show fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 30), cv2.FONT_HERSHEY_PLAIN, 1.5,
                (0, 255, 0), 2)

    cv2.imshow("main", img)
    cv2.waitKey(1)
