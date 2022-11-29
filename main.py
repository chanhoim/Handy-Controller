from cv2 import cv2
import time
from HandTrackingModule import HandDetector
import osascript
from pynput.keyboard import Key, Controller
keyboard = Controller()

# finger tip variables
tipIds = [4, 8, 12, 16, 20]

# circle variables
circleRadius1 = 5
circleRadius2 = 10
circleRadius3 = 15

# font variables
fontSize1 = 1.5
fontThickness1 = 2  # integer only
fontSize2 = 2.5
fontThickness2 = 3  # integer only

# line variables
lineThickness1 = 2
lineThickness2 = 4

# color variables
red = (0, 0, 255)
green = (0, 255, 0)
blue = (255, 0, 0)
yellow = (0, 255, 255)
white = (255, 255, 255)
purple = (255, 0, 255)

# time variables
pTime = 0
volTime = 0.3
medTime = 0.4  # 0.1 ~ 0.5
scrTime = 0.3

# input sources
camInput = 0  # 0 for webcam, 1 for external source
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
        # single hand detected 
        if len(hands) == 1:
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

        # two hands detected 
        if len(hands) == 2:
            # hand 1 
            hand1 = hands[0]
            lmList1 = hand1["lmList"]  # list of 21 landmarks of points
            bbox1 = hand1["bbox"]  # bounding box info (x, y, w, h)
            centerPoint1 = hand1["center"]  # center of the hand cx, cy
            handType1 = hand1["type"]  # hand type (left or right)
            fingers1 = detector.fingersUp(hand1)

            print(f"{handType1} Hand, Center = {centerPoint1}, Fingers = {fingers1}")

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

                # 1. Volume Control Mode
                if fingers1.count(1) == 1:
                    print("Volume Control Mode")
                    mvdLength, mvdInfo, img = detector.findDistance(lmList2[8], lmList2[3], img)
                    mvuLength, mvuInfo, img = detector.findDistance(lmList2[8], lmList2[4], img)

                    if fingers2 == [0, 1, 1, 1, 1]:
                        print("mute")
                        keyboard.press(Key.media_volume_mute)
                        time.sleep(volTime)
                        keyboard.release(Key.media_volume_mute)

                    if fingers2[0] == 1:
                        if mvdLength < 30:
                            cv2.circle(img, (mvdInfo[4], mvdInfo[5]), circleRadius3, blue, cv2.FILLED)
                            print("volume down")
                            keyboard.press(Key.media_volume_down)
                            time.sleep(volTime)
                            keyboard.release(Key.media_volume_down)

                        elif mvuLength < 30:
                            cv2.circle(img, (mvuInfo[4], mvuInfo[5]), circleRadius3, blue, cv2.FILLED)
                            print("volume up")
                            keyboard.press(Key.media_volume_up)
                            time.sleep(volTime)
                            keyboard.release(Key.media_volume_up)

                # 2. Media Control Mode
                elif fingers1.count(1) == 2:
                    print("Media Control Mode")
                    mpLength, mpInfo, img = detector.findDistance(lmList2[8], lmList2[3], img)
                    mnLength, mnInfo, img = detector.findDistance(lmList2[8], lmList2[4], img)

                    if fingers2 == [0, 1, 1, 1, 1]:
                        print("play/pause")
                        keyboard.press(Key.media_play_pause)
                        time.sleep(medTime)
                        keyboard.release(Key.media_play_pause)

                    if fingers2[0] == 1:
                        if mpLength < 30:
                            cv2.circle(img, (mpInfo[4], mpInfo[5]), circleRadius3, blue, cv2.FILLED)
                            print("play previous")
                            keyboard.press(Key.media_previous)
                            time.sleep(medTime)
                            keyboard.release(Key.media_previous)

                        elif mnLength < 30:
                            cv2.circle(img, (mnInfo[4], mnInfo[5]), circleRadius3, blue, cv2.FILLED)
                            print("play next")
                            keyboard.press(Key.media_next)
                            time.sleep(medTime)
                            keyboard.release(Key.media_next)

                # 3. Page Control Mode
                elif fingers1.count(1) == 3:
                    print("Page Control Mode")
                    pdLength, pdInfo, img = detector.findDistance(lmList2[8], lmList2[3], img)
                    puLength, puInfo, img = detector.findDistance(lmList2[8], lmList2[4], img)

                    if fingers2[0] == 1:
                        if pdLength < 30:
                            cv2.circle(img, (pdInfo[4], pdInfo[5]), circleRadius3, blue, cv2.FILLED)
                            print("page down")
                            keyboard.press(Key.page_down)
                            time.sleep(scrTime)
                            keyboard.release(Key.page_down)

                        elif puLength < 30:
                            cv2.circle(img, (puInfo[4], puInfo[5]), circleRadius3, blue, cv2.FILLED)
                            print("page up")
                            keyboard.press(Key.page_up)
                            time.sleep(scrTime)
                            keyboard.release(Key.page_up)

                # 4. Control Mode
                elif fingers1.count(1) == 4:
                    print("4")

                # 5. Idle State Mode
                elif fingers1.count(1) == 5:
                    print("Idle State Mode")

                # 0. Desktop Control Mode
                else:
                    print("Desktop Control Mode")
                    if fingers2 == [0, 1, 1, 1, 1]:
                        print("Toggle desktop")
                        keyboard.press(Key.f11)
                        # time.sleep(0.3)
                        keyboard.release(Key.f11)

            # TODO: fix hand type flipping issue
            # e.g. handType1 = right, handType2 = left
            # set hand types accordingly

            print("")

    # show fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 30), cv2.FONT_HERSHEY_PLAIN, 1.5,
                (0, 255, 0), 2)

    cv2.imshow("main", img)
    cv2.waitKey(1)
