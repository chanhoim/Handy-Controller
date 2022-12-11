import cv2
import time
import platform
from HandTrackingModule import HandDetector
from pynput.keyboard import Key, Controller
import pyautogui
import numpy as np
import screen_brightness_control as sbc

keyboard = Controller()

# check operating system
myOS = platform.system()  # Windows / Darwin(Mac)

if myOS == "Windows":
    print("Program running on Windows")
elif myOS == "Darwin":
    print("Program running on MacOSX")
else:
    print("Program running on other OSs")

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
cyan = (255, 255, 0)
purple = (255, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)

# time variables
pTime = 0  # page control time
mocTime = 0.2  # mouse control time
mvcTime = 0.1  # media volume control time
mdcTime = 0.4  # media control time
pgcTime = 0.2  # page control time
dkcTime = 0.1  # desktop control time

# finger to finger distances
tiDist1 = 30  # thumb - index finger distance
tmDist1 = 30  # thumb - middle finger distance
miDist1 = 40  # middle finger - index finger distance
mrDist1 = 20  # middle finger - ring finger distance
tiDist2 = 30  # thumb - index finger distance
tmDist2 = 20  # thumb - middle finger distance
miDist2 = 35  # middle finger - index finger distance

# input sources
camInput = 0  # 0 for webcam, 1 for external source
cap = cv2.VideoCapture(camInput)

# mouse location variables
smoothening = 3.5
plocX, plocY = 0, 0
clocX, clocY = 0, 0
camW, camH = 640, 480  # camera size
frmW, frmH = 150, 100  # frame reduction size
scrW, scrH = pyautogui.size()  # screen size (1680, 1050)
cap.set(3, camW)
cap.set(4, camH)

# new detector object from HandDetector class
detector = HandDetector(detectionCon=0.9, maxHands=2)

# control mode
controlMode=None
mode={
    None: "None",
    0 : "Idle",
    1 : "Volume",
    2 : "Mouse-1",
    3 : "Mouse-2",
    4 : "Media",
    5 : "Page",
    6 : "Desktop",
    7 : "Bright"
}



def translateControlMode(controlMode):
    return mode.get(controlMode,"Error")

# boolean value for idle mode
idle=False



while True:
    success, img = cap.read()
    if camInput == 0:
        img = cv2.flip(img, 1)  # flip for webcam
        hands, img = detector.findHands(img, flipType=False)  # flip type for webcam
    else:
        hands, img = detector.findHands(img)

    if hands:
        if len(hands) == 1:
            """
            1. Single Hand Detected.
            """
            # 1st hand info
            hand1 = hands[0]
            lmList1 = hand1["lmList"]  # list of 21 landmarks of points
            bbox1 = hand1["bbox"]  # bounding box info (x, y, w, h)
            bbox1Area = bbox1[2] * bbox1[3]
            centerPoint1 = hand1["center"]  # center of the hand cx, cy
            handType1 = hand1["type"]  # hand type (left or right)
            fingers1 = detector.fingersUp(hand1)
            x1, y1 = lmList1[8][0], lmList1[8][1]  # index finger location

            # print(x1, y1)
            #print(f"{handType1} Hand, Center = {centerPoint1}, Fingers = {fingers1}")
            # print("bounding box area = ", bbox1Area)

            cv2.rectangle(img=img, pt1=(frmW, frmH), pt2=(camW - frmW, camH - frmH), color=purple,
                          thickness=lineThickness2)
            
            if handType1 == "Left":
                if fingers1[0:5] == [0, 0, 0, 0, 0]:
                    print("idle state Mode")
                    controlMode=0
                    idle= not idle
                    print("idle:"+str(idle))
                    time.sleep(1)
                elif fingers1[0:5] == [0, 1, 0, 0, 0] and not idle:
                    print("volume control mode")
                    controlMode=1
                elif fingers1[0:5] == [0, 1, 1, 0, 0] and not idle:
                    modeLength, modeInfo, img = detector.findDistance(lmList1[12], lmList1[8], img)
                    if modeLength > miDist1:
                       print("mouse control mode-1")
                       controlMode=2
                    else:
                       print("mouse control mode-2")
                       controlMode=3
                       
                elif fingers1[0:5] == [0, 1, 1, 1, 0] and not idle:
                    print("media control mode")
                    controlMode=4
                elif fingers1[0:5] == [0, 1, 1, 1, 1] and not idle:
                    print("page control mode")
                    controlMode=5
                elif fingers1[0:5] == [1, 1, 1, 1, 1] and not idle:
                    print("desktop control mode")
                    controlMode=6
                elif fingers1[0:5] == [1,0,0,0,0] and not idle:
                    print("brightness control mode")
                    controlMode=7
                elif fingers1[0:5] == [0, 0, 1, 0, 0] and not idle:
                    print("quit")
                    exit()
            

                    
            elif handType1== "Right":
                #print("Control Mode Status="+translateControlMode(controlMode))
                if idle:
                    print("It's idle status, do nothing")
                else:
                    if controlMode == 1:
                        print("Volume Control Mode")
                        mvuLength, mvuInfo, img = detector.findDistance(lmList1[4], lmList1[10], img)
                        mvdLength, mvdInfo, img = detector.findDistance(lmList1[4], lmList1[11], img)
                        mvmLength, mvmInfo, img = detector.findDistance(lmList1[8], lmList1[4], img)


                        #print(mvuLength, mvuInfo[4], mvuInfo[5])

                        if mvuLength < tiDist1 - 5:
                            print("volume up")
                            cv2.circle(img, (mvuInfo[4], mvuInfo[5]), circleRadius2, purple, cv2.FILLED)
                            keyboard.press(Key.media_volume_up)
                            time.sleep(mvcTime)
                            keyboard.release(Key.media_volume_up)

                        if mvdLength < tiDist1 - 5:
                            print("volume down")
                            cv2.circle(img, (mvdInfo[4], mvdInfo[5]), circleRadius2, purple, cv2.FILLED)
                            keyboard.press(Key.media_volume_down)
                            time.sleep(mvcTime)
                            keyboard.release(Key.media_volume_down)

                        if mvmLength < tiDist2:
                            print("mute")
                            cv2.circle(img, (mvmInfo[4], mvmInfo[5]), circleRadius2, purple, cv2.FILLED)
                            keyboard.press(Key.media_volume_mute)
                            time.sleep(4 * mvcTime)
                            keyboard.release(Key.media_volume_mute)

                        
                    elif controlMode == 2:
                        print("Mouse Mode 1")

                        x3 = np.interp(x1, (frmW, camW - frmW), (0, scrW))
                        y3 = np.interp(y1, (frmH, camH - frmH), (0, scrH))

                        # smoothen values
                        clocX = plocX + (x3 - plocX) / smoothening
                        clocY = plocY + (y3 - plocY) / smoothening

                        # print(clocX, clocY)  # cursor location
                        # print(x3, y3)  # index finger location in  window

                        # mouse move
                        if fingers1 == [1, 1, 1, 0, 0]:
                            pyautogui.moveTo(clocX, clocY)
                            cv2.circle(img, (x1, y1), circleRadius2, cyan, cv2.FILLED)
                            plocX, plocY = clocX, clocY

                        
                        mlcLength, mlcInfo, img = detector.findDistance(lmList1[8], lmList1[6], img)
                        mrcLength, mrcInfo, img = detector.findDistance(lmList1[12], lmList1[10], img)
                        gbLength, gbInfo, img = detector.findDistance(lmList1[4], lmList1[6], img) #4,15 -> 4,6
                        gfLength, gfInfo, img = detector.findDistance(lmList1[4], lmList1[5], img) #4,14 -> 4,5

                        if mlcLength < 40:
                            print("left click")
                            cv2.circle(img, (mlcInfo[4], mlcInfo[5]), circleRadius2, purple, cv2.FILLED)
                            pyautogui.click(interval=mocTime)

                        if mrcLength < 40:
                            print("right click")
                            cv2.circle(img, (mrcInfo[4], mrcInfo[5]), circleRadius2, purple, cv2.FILLED)
                            pyautogui.rightClick(interval=mocTime)

                        if gfLength < 40:    #mrDist1 -> 40
                            print("go forward")
                            cv2.circle(img, (gfInfo[4], gfInfo[5]), circleRadius2, purple, cv2.FILLED)
                            if myOS == "Windows":
                                pyautogui.hotkey('alt', 'right')
                            if myOS == "Darwin":
                                pyautogui.hotkey('command', ']')

                        if gbLength < 40:   #mrDist1 -> 40
                            print("gp backward")
                            cv2.circle(img, (gbInfo[4], gbInfo[5]), circleRadius2, purple, cv2.FILLED)
                            if myOS == "Windows":
                                pyautogui.hotkey('alt', 'left')
                            if myOS == "Darwin":
                                pyautogui.hotkey('command', '[')

                    elif controlMode==3:
                        print("Mouse Mode 2")

                        x3 = np.interp(x1, (frmW, camW - frmW), (0, scrW))
                        y3 = np.interp(y1, (frmH, camH - frmH), (0, scrH))

                        # smoothen values
                        clocX = plocX + (x3 - plocX) / smoothening
                        clocY = plocY + (y3 - plocY) / smoothening

                        # print(clocX, clocY)  # cursor location
                        # print(x3, y3)  # index finger location in  window

                        # mouse move
                        if fingers1 == [1, 1, 1, 0, 0]:
                            pyautogui.moveTo(clocX, clocY)
                            cv2.circle(img, (x1, y1), circleRadius2, cyan, cv2.FILLED)
                            plocX, plocY = clocX, clocY

                        
                        mdLength, mdInfo, img = detector.findDistance(lmList1[8], lmList1[6], img)
                        puLength, puInfo, img = detector.findDistance(lmList1[4], lmList1[5], img) #4,14 -> 4,5
                        pdLength, pdInfo, img = detector.findDistance(lmList1[4], lmList1[6], img) #4,15 -> 4,6

                        if mdLength < 40:
                            print("mouse drag")
                            cv2.circle(img, (mdInfo[4], mdInfo[5]), circleRadius2, purple, cv2.FILLED)
                            pyautogui.dragTo(clocX, clocY, button='left')

                        if puLength < 40:   #mrDist1->40
                            print("page up")
                            cv2.circle(img, (puInfo[4], puInfo[5]), circleRadius2, purple, cv2.FILLED)
                            if myOS == "Windows":
                                pyautogui.scroll(250)
                            if myOS == "Darwin":
                                pyautogui.scroll(10)

                        if pdLength < 40:  #mrDist1->40
                            print("page down")
                            cv2.circle(img, (pdInfo[4], pdInfo[5]), circleRadius2, purple, cv2.FILLED)
                            if myOS == "Windows":
                                pyautogui.scroll(-250)
                            if myOS == "Darwin":
                                pyautogui.scroll(-10)
                    
                    elif controlMode == 4:
                        print("Media Control Mode")
                        mnLength, mnInfo, img = detector.findDistance(lmList1[4], lmList1[10], img)
                        mpLength, mpInfo, img = detector.findDistance(lmList1[4], lmList1[11], img)

                        mppLength, mppInfo, img = detector.findDistance(lmList1[8], lmList1[4], img)

                        if mpLength < tmDist2:
                            print("play previous")
                            cv2.circle(img, (mpInfo[4], mpInfo[5]), circleRadius2, purple, cv2.FILLED)
                            keyboard.press(Key.media_previous)
                            time.sleep(mdcTime)
                            keyboard.release(Key.media_previous)

                        if mnLength < tmDist2:
                            print("play next")
                            cv2.circle(img, (mnInfo[4], mnInfo[5]), circleRadius2, purple, cv2.FILLED)
                            keyboard.press(Key.media_next)
                            time.sleep(mdcTime)
                            keyboard.release(Key.media_next)

                        if mppLength < tiDist2:
                            print("play/pause")
                            cv2.circle(img, (mppInfo[4], mppInfo[5]), circleRadius2, purple, cv2.FILLED)
                            keyboard.press(Key.media_play_pause)
                            time.sleep(mdcTime)
                            keyboard.release(Key.media_play_pause)

                    elif controlMode == 5:
                        print("Page Control Mode")
                        puLength, puInfo, img = detector.findDistance(lmList1[4], lmList1[10], img)
                        pdLength, pdInfo, img = detector.findDistance(lmList1[4], lmList1[11], img)

                        phLength, phInfo, img = detector.findDistance(lmList1[8], lmList1[4], img)
                        peLength, peInfo, img = detector.findDistance(lmList1[8], lmList1[3], img)

                        if pdLength < tmDist2:
                            print("page down")
                            cv2.circle(img, (pdInfo[4], pdInfo[5]), circleRadius2, purple, cv2.FILLED)
                            if myOS == "Windows":
                                pyautogui.scroll(-250)
                            if myOS == "Darwin":
                                pyautogui.scroll(-10)

                        if puLength < tmDist2:
                            print("page up")
                            cv2.circle(img, (puInfo[4], puInfo[5]), circleRadius2, purple, cv2.FILLED)
                            if myOS == "Windows":
                                pyautogui.scroll(250)
                            if myOS == "Darwin":
                                pyautogui.scroll(10)

                        if phLength < tiDist2:
                            print("home")
                            cv2.circle(img, (phInfo[4], phInfo[5]), circleRadius2, purple, cv2.FILLED)
                            keyboard.press(Key.home)
                            time.sleep(pgcTime)
                            keyboard.release(Key.home)

                        if peLength < tiDist2:
                            print("end")
                            cv2.circle(img, (peInfo[4], peInfo[5]), circleRadius2, purple, cv2.FILLED)
                            keyboard.press(Key.end)
                            time.sleep(pgcTime)
                            keyboard.release(Key.end)

                    elif controlMode == 6:
                        print("Desktop Control Mode")
                        ndLength, ndInfo, img = detector.findDistance(lmList1[4], lmList1[10], img)
                        pdLength, pdInfo, img = detector.findDistance(lmList1[4], lmList1[11], img)

                        mlcLength, mlcInfo, img = detector.findDistance(lmList1[8], lmList1[4], img)
                        sdLength, sdInfo, img = detector.findDistance(lmList1[8], lmList1[3], img)

                        if pdLength < tmDist2:
                            print("previous desktop")
                            cv2.circle(img, (pdInfo[4], pdInfo[5]), circleRadius2, purple, cv2.FILLED)
                            if myOS == "Windows":
                                pyautogui.hotkey('win', 'ctrl', 'left')
                            if myOS == "Darwin":
                                pyautogui.hotkey('ctrl', 'left')

                        if ndLength < tmDist2:
                            print("next desktop")
                            cv2.circle(img, (ndInfo[4], ndInfo[5]), circleRadius2, purple, cv2.FILLED)
                            if myOS == "Windows":
                                pyautogui.hotkey('win', 'ctrl', 'right')
                            if myOS == "Darwin":
                                pyautogui.hotkey('ctrl', 'right')

                        if mlcLength < tiDist2:
                            print("show applications")
                            cv2.circle(img, (mlcInfo[4], mlcInfo[5]), circleRadius2, purple, cv2.FILLED)
                            if myOS == "Windows":
                                pyautogui.hotkey('win', 'tab')
                            if myOS == "Darwin":
                                pyautogui.hotkey('ctrl', 'up')

                        if sdLength < tiDist2:
                            print("show desktop")
                            cv2.circle(img, (sdInfo[4], sdInfo[5]), circleRadius2, purple, cv2.FILLED)
                            if myOS == "Windows":
                                pyautogui.hotkey('win', 'd')
                            if myOS == "Darwin":
                                pyautogui.hotkey('fn', 'f10')

                    elif controlMode==7:
                        print("Brightness Control Mode")
                        buLength, buInfo, img = detector.findDistance(lmList1[4], lmList1[10], img)
                        bdLength, bdInfo, img = detector.findDistance(lmList1[4], lmList1[11], img)

                        bMaxLength, bMaxInfo, img = detector.findDistance(lmList1[8], lmList1[4], img)
                        bMinLength, bMinInfo, img = detector.findDistance(lmList1[8], lmList1[3], img)

                        # TODO: fix brightness up & down feature for MacOSX
                        if bdLength < tmDist2:
                            print("brightness down")
                            cv2.circle(img, (bdInfo[4], bdInfo[5]), circleRadius2, purple, cv2.FILLED)
                            if myOS == "Windows":
                                sbc.set_brightness('-10')  # decrease by 10 %
                            if myOS == "Darwin":
                                pyautogui.hotkey('fn', 'f11')

                        if buLength < tmDist2:
                            print("brightness up")
                            cv2.circle(img, (buInfo[4], buInfo[5]), circleRadius2, purple, cv2.FILLED)
                            if myOS == "Windows":
                                sbc.set_brightness('+10')  # increase by 10 %
                            if myOS == "Darwin":
                                pyautogui.hotkey('fn', 'f12')

                        # TODO: implement max and min brightness feature for MacOSX
                        if bMaxLength < tiDist2:
                            print("brightness 100%")
                            cv2.circle(img, (bMaxInfo[4], bMaxInfo[5]), circleRadius2, purple, cv2.FILLED)
                            if myOS == "Windows":
                                sbc.set_brightness(100)
                            if myOS == "Darwin":
                                print("not implemented in MacOSX yet")

                        if bMinLength < tiDist2:
                            print("brightness 0%")
                            cv2.circle(img, (bMinInfo[4], bMinInfo[5]), circleRadius2, purple, cv2.FILLED)
                            if myOS == "Windows":
                                sbc.set_brightness(0)
                            if myOS == "Darwin":
                                print("not implemented in MacOSX yet")
                        

            

        
        if len(hands) == 2:
            print("do nothing")
            print("")

    

    # show fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 30), cv2.FONT_HERSHEY_PLAIN, fontSize1,
                green, lineThickness1)
    cv2.putText(img,"MODE:"+translateControlMode(controlMode),(450,30),cv2.FONT_HERSHEY_PLAIN, fontSize1,
                green, lineThickness1)

    cv2.imshow("main", img)
    if cv2.waitKey(1) == ord('q'):
        break
