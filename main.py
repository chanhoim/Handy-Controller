from cv2 import cv2
import time
from HandTrackingModule import HandDetector
import osascript
from pynput.keyboard import Key, Controller

keyboard = Controller()

camInput = 0  # 0 for webcam, 1 for external source
tipIds = [4, 8, 12, 16, 20]

circleRadius1 = 5
circleRadius2 = 10
circleRadius3 = 15

fontSize1 = 1.5
fontThickness1 = 2  # integer only

fontSize2 = 2.5
fontThickness2 = 3  # integer only

lineThickness1 = 2
lineThickness2 = 4

red = (0, 0, 255)
green = (0, 255, 0)
blue = (255, 0, 0)
yellow = (0, 255, 255)
white = (255, 255, 255)
purple = (255, 0, 255)

pTime = 0
volTime = 0.1
medTime = 0.5

cap = cv2.VideoCapture(camInput)
detector = HandDetector(detectionCon=0.8, maxHands=2)

while True:
    success, img = cap.read()
    if camInput == 0:
        img = cv2.flip(img, 1)  # flip for webcam
        hands, img = detector.findHands(img, flipType=False)  # flip type for webcam
    else:
        hands, img = detector.findHands(img)

    if hands:
        # hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # list of 21 landmarks of points
        bbox1 = hand1["bbox"]  # bounding box info (x, y, w, h)
        centerPoint1 = hand1["center"]  # center of the hand cx, cy
        handType1 = hand1["type"]  # hand type (left or right)
        fingers1 = detector.fingersUp(hand1)

        print(f"{handType1} Hand, Center = {centerPoint1}, Fingers = {fingers1}")

        # TODO: implement 1 hand quit sign
        # quit sign

        if len(hands) == 2:
            # hand 2
            hand2 = hands[1]
            lmList2 = hand2["lmList"]  # list of 21 landmarks of points
            bbox2 = hand2["bbox"]  # bounding box info (x, y, w, h)
            centerPoint2 = hand2["center"]  # center of the hand cx, cy
            handType2 = hand2["type"]  # hand type (left or right)
            fingers2 = detector.fingersUp(hand2)

            print(f"{handType2} Hand, Center = {centerPoint2}, Fingers = {fingers2}")

            # handType1 is left hand and handType2 is right hand
            if handType1 == "Left" and handType2 == "Right":
                if fingers1.count(1) == 1:
                    print("Volume Control Mode")
                    iLength, iInfo, img = detector.findDistance(lmList2[4], lmList2[8], img)
                    mLength, mInfo, img = detector.findDistance(lmList2[8], lmList2[12], img)

                    if iLength < 30:
                        cv2.circle(img, (iInfo[4], iInfo[5]), circleRadius3, blue, cv2.FILLED)
                        print("volume down")
                        keyboard.press(Key.media_volume_down)
                        time.sleep(volTime)
                        keyboard.release(Key.media_volume_down)

                    if mLength < 30:
                        cv2.circle(img, (mInfo[4], mInfo[5]), circleRadius3, blue, cv2.FILLED)
                        print("volume up")
                        keyboard.press(Key.media_volume_up)
                        time.sleep(volTime)
                        keyboard.release(Key.media_volume_up)

                elif fingers1.count(1) == 2:
                    print("Media Control Mode")
                    iLength, iInfo, img = detector.findDistance(lmList2[4], lmList2[8], img)
                    mLength, mInfo, img = detector.findDistance(lmList2[8], lmList2[12], img)

                    if fingers2 == [1, 0, 0, 0, 0]:
                        print("play/pause")
                        keyboard.press(Key.media_play_pause)
                        time.sleep(medTime)
                        keyboard.release(Key.media_play_pause)

                    if iLength < 30:
                        cv2.circle(img, (iInfo[4], iInfo[5]), circleRadius3, blue, cv2.FILLED)
                        print("play previous")
                        keyboard.press(Key.media_previous)
                        time.sleep(volTime)
                        keyboard.release(Key.media_previous)

                    if mLength < 30:
                        cv2.circle(img, (mInfo[4], mInfo[5]), circleRadius3, blue, cv2.FILLED)
                        print("play next")
                        keyboard.press(Key.media_next)
                        time.sleep(volTime)
                        keyboard.release(Key.media_next)

                elif fingers1.count(1) == 3:
                    print("3")
                elif fingers1.count(1) == 4:
                    print("4")
                elif fingers1.count(1) == 5:
                    print("5")
                else:
                    print("Desktop Mode")

            # handType2 is left hand and handType1 is right hand
            if handType1 == "Right" and handType2 == "Left":
                if fingers2.count(1) == 1:
                    print("Volume Mode")
                    iLength, iInfo, img = detector.findDistance(lmList1[4], lmList1[8], img)
                    mLength, mInfo, img = detector.findDistance(lmList1[8], lmList1[12], img)

                    if iLength < 30:
                        cv2.circle(img, (iInfo[4], iInfo[5]), circleRadius3, blue, cv2.FILLED)
                        print("volume down")
                        keyboard.press(Key.media_volume_down)
                        time.sleep(volTime)
                        keyboard.release(Key.media_volume_down)

                    if mLength < 30:
                        cv2.circle(img, (mInfo[4], mInfo[5]), circleRadius3, blue, cv2.FILLED)
                        print("volume up")
                        keyboard.press(Key.media_volume_up)
                        time.sleep(volTime)
                        keyboard.release(Key.media_volume_up)

                elif fingers2.count(1) == 2:
                    print("Media Control Mode")
                    iLength, iInfo, img = detector.findDistance(lmList1[4], lmList1[8], img)
                    mLength, mInfo, img = detector.findDistance(lmList1[8], lmList1[12], img)

                    if fingers1 == [1, 0, 0, 0, 0]:
                        print("play/pause")
                        keyboard.press(Key.media_play_pause)
                        time.sleep(medTime)
                        keyboard.release(Key.media_play_pause)

                    if iLength < 30:
                        cv2.circle(img, (iInfo[4], iInfo[5]), circleRadius3, blue, cv2.FILLED)
                        print("play previous")
                        keyboard.press(Key.media_previous)
                        time.sleep(volTime)
                        keyboard.release(Key.media_previous)

                    if mLength < 30:
                        cv2.circle(img, (mInfo[4], mInfo[5]), circleRadius3, blue, cv2.FILLED)
                        print("play next")
                        keyboard.press(Key.media_next)
                        time.sleep(volTime)
                        keyboard.release(Key.media_next)

                elif fingers2.count(1) == 3:
                    print("3")
                elif fingers2.count(1) == 4:
                    print("4")
                elif fingers2.count(1) == 5:
                    print("5")
                else:
                    print("Desktop Mode")
            print("")

    # show fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 30), cv2.FONT_HERSHEY_PLAIN, 1.5,
                (0, 255, 0), 2)

    cv2.imshow("main", img)
    cv2.waitKey(1)
