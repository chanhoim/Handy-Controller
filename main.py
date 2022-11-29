from cv2 import cv2
import time
import subprocess
from HandTrackingModule import HandDetector
from pynput.keyboard import Key, Controller

keyboard = Controller()

# finger tip variables
tipIds = [4, 8, 12, 16, 20]

# circle variables
circleRadius1 = 5
circleRadius2 = 10
circleRadius3 = 15

# font variable
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
dktTime = 0.1

# input sources
camInput = 0  # 0 for webcam, 1 for external source
cap = cv2.VideoCapture(camInput)

detector = HandDetector(detectionCon=0.8, maxHands=2)


def asRun(aScript):
    """
    Run the given AppleScript and
    return the standard output and error.
    """
    osa = subprocess.Popen(['osascript', '-'],
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE)
    return osa.communicate(bytes(aScript, 'UTF-8'))[0]


def asQuote(aStr):
    """
    Return the AppleScript equivalent of the given string.
    """
    aStr = aStr.replace('"', '" & quote & "')
    return '"{}"'.format(aStr)


# previous desktop
pdScript = '''
tell application "System Events"
    key code 123 using {control down}
end tell
'''

# next desktop
ndScript = '''
tell application "System Events"
    key code 124 using {control down}
end tell
'''

# mission control
mcScript = '''
tell application "System Events"
    key code 126 using {control down}
end tell
'''

# show desktop
sdScript = '''
tell application "System Events"
    key code 103
end tell
'''

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

            # 0. Idle State Mode
            if fingers1.count(1) == 0:
                print("Idle State Mode")

            # 1. Control Mode
            elif fingers1.count(1) == 1:
                print("1")

            # 2. Control Mode
            elif fingers1.count(1) == 2:
                print("2")

            # 3. Control Mode
            elif fingers1.count(1) == 3:
                print("3")

            # 4. Control Mode
            elif fingers1.count(1) == 4:
                print("4")

            # 5. Control Mode
            else:
                print("5")

            # TODO: implement 1 hand quit sign
            if fingers1[3:5] == [0, 0]:
                print("Quit Mode")
                if fingers1[0:3] == [1, 0, 0]:
                    print("Quit!")  # for testing

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
                    if fingers2[2:5] == [0, 0, 0] and fingers2 != [0, 0, 0, 0, 0]:
                        print("Volume Control Mode (Active)")
                        mvdLength, mvdInfo, img = detector.findDistance(lmList2[8], lmList2[3], img)
                        mvuLength, mvuInfo, img = detector.findDistance(lmList2[8], lmList2[4], img)

                        mvmLength, mvmInfo, img = detector.findDistance(lmList2[4], lmList2[11], img)

                        if mvdLength < 30:
                            cv2.circle(img, (mvdInfo[4], mvdInfo[5]), circleRadius3, blue, cv2.FILLED)
                            print("volume down")
                            keyboard.press(Key.media_volume_down)
                            time.sleep(volTime)
                            keyboard.release(Key.media_volume_down)

                        if mvuLength < 30:
                            cv2.circle(img, (mvuInfo[4], mvuInfo[5]), circleRadius3, blue, cv2.FILLED)
                            print("volume up")
                            keyboard.press(Key.media_volume_up)
                            time.sleep(volTime)
                            keyboard.release(Key.media_volume_up)

                        if mvmLength < 40:
                            print("mute")
                            cv2.circle(img, (mvmInfo[4], mvmInfo[5]), circleRadius3, blue, cv2.FILLED)
                            keyboard.press(Key.media_volume_mute)
                            time.sleep(volTime)
                            keyboard.release(Key.media_volume_mute)
                    else:
                        print("Volume Control Mode (Inactive)")

                # 2. Media Control Mode
                elif fingers1.count(1) == 2:
                    if fingers2[2:5] == [0, 0, 0] and fingers2 != [0, 0, 0, 0, 0]:
                        print("Media Control Mode (Active)")
                        mpLength, mpInfo, img = detector.findDistance(lmList2[8], lmList2[3], img)
                        mnLength, mnInfo, img = detector.findDistance(lmList2[8], lmList2[4], img)

                        mppLength, mppInfo, img = detector.findDistance(lmList2[4], lmList2[11], img)

                        if mpLength < 30:
                            cv2.circle(img, (mpInfo[4], mpInfo[5]), circleRadius3, blue, cv2.FILLED)
                            print("play previous")
                            keyboard.press(Key.media_previous)
                            time.sleep(medTime)
                            keyboard.release(Key.media_previous)

                        if mnLength < 30:
                            cv2.circle(img, (mnInfo[4], mnInfo[5]), circleRadius3, blue, cv2.FILLED)
                            print("play next")
                            keyboard.press(Key.media_next)
                            time.sleep(medTime)
                            keyboard.release(Key.media_next)

                        if mppLength < 40:
                            print("play/pause")
                            cv2.circle(img, (mppInfo[4], mppInfo[5]), circleRadius3, blue, cv2.FILLED)
                            keyboard.press(Key.media_play_pause)
                            time.sleep(medTime)
                            keyboard.release(Key.media_play_pause)
                    else:
                        print("Media Control Mode (Inactive)")

                # 3. Page Control Mode
                elif fingers1.count(1) == 3:
                    if fingers2[2:5] == [0, 0, 0] and fingers2 != [0, 0, 0, 0, 0]:
                        print("Page Control Mode (Active)")
                        pdLength, pdInfo, img = detector.findDistance(lmList2[8], lmList2[3], img)
                        puLength, puInfo, img = detector.findDistance(lmList2[8], lmList2[4], img)

                        phLength, phInfo, img = detector.findDistance(lmList2[4], lmList2[10], img)
                        peLength, peInfo, img = detector.findDistance(lmList2[4], lmList2[11], img)

                        if pdLength < 30:
                            cv2.circle(img, (pdInfo[4], pdInfo[5]), circleRadius3, blue, cv2.FILLED)
                            print("page down")
                            keyboard.press(Key.page_down)
                            time.sleep(scrTime)
                            keyboard.release(Key.page_down)

                        if puLength < 30:
                            cv2.circle(img, (puInfo[4], puInfo[5]), circleRadius3, blue, cv2.FILLED)
                            print("page up")
                            keyboard.press(Key.page_up)
                            time.sleep(scrTime)
                            keyboard.release(Key.page_up)

                        if phLength < 40:
                            print("home")
                            cv2.circle(img, (phInfo[4], phInfo[5]), circleRadius3, blue, cv2.FILLED)
                            keyboard.press(Key.home)
                            time.sleep(scrTime)
                            keyboard.release(Key.home)

                        if peLength < 40:
                            print("end")
                            cv2.circle(img, (peInfo[4], peInfo[5]), circleRadius3, blue, cv2.FILLED)
                            keyboard.press(Key.end)
                            time.sleep(scrTime)
                            keyboard.release(Key.end)
                    else:
                        print("Page Control Mode (Inactive)")

                # 4. Control Mode
                elif fingers1.count(1) == 4:
                    if fingers2[2:5] == [0, 0, 0] and fingers2 != [0, 0, 0, 0, 0]:
                        print("4 Control Mode (Active)")
                    else:
                        print("4 Control Mode (Inactive)")

                # 5. Desktop Control Mode
                elif fingers1.count(1) == 5:
                    if fingers2[2:5] == [0, 0, 0] and fingers2 != [0, 0, 0, 0, 0]:
                        print("Desktop Control Mode (Active)")
                        ndLength, ndInfo, img = detector.findDistance(lmList2[8], lmList2[3], img)
                        pdLength, pdInfo, img = detector.findDistance(lmList2[8], lmList2[4], img)

                        mcLength, mcInfo, img = detector.findDistance(lmList2[4], lmList2[10], img)
                        sdLength, sdInfo, img = detector.findDistance(lmList2[4], lmList2[11], img)

                        if pdLength < 30:
                            print("previous desktop")
                            cv2.circle(img, (pdInfo[4], pdInfo[5]), circleRadius3, blue, cv2.FILLED)
                            asRun(pdScript)

                        if ndLength < 30:
                            print("next desktop")
                            cv2.circle(img, (ndInfo[4], ndInfo[5]), circleRadius3, blue, cv2.FILLED)
                            asRun(ndScript)

                        if mcLength < 40:
                            print("mission control")
                            cv2.circle(img, (mcInfo[4], mcInfo[5]), circleRadius3, blue, cv2.FILLED)
                            asRun(mcScript)

                        if sdLength < 40:
                            print("show desktop")
                            cv2.circle(img, (sdInfo[4], sdInfo[5]), circleRadius3, blue, cv2.FILLED)
                            asRun(sdScript)
                    else:
                        print("Desktop Control Mode (Inactive)")

                # 0. Idle State Mode
                else:
                    print("Idle State Mode")

            # TODO: fix hand type flipping issue
            # e.g. handType1 = right, handType2 = left
            # set hand types accordingly

            print("")

    # show fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 30), cv2.FONT_HERSHEY_PLAIN, fontSize1,
                green, lineThickness1)

    cv2.imshow("main", img)
    cv2.waitKey(1)
