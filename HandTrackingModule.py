"""
Hand Tracking Module
By: Computer Vision Zone
Website: https://www.computervision.zone/
"""

import cv2
import mediapipe as mp
import math
import numpy as np

circleRadius1 = 5
circleRadius2 = 10

fontSize1 = 1
fontThickness1 = 2  # integer only

fontSize2 = 1.5
fontThickness2 = 2  # integer only

lineThickness2 = 4

red = (0, 0, 255)
green = (0, 255, 0)
blue = (255, 0, 0)
yellow = (0, 255, 255)
white = (255, 255, 255)
purple = (255, 0, 255)


class HandDetector:
    """
    Finds Hands using the mediapipe library. Exports the landmarks
    in pixel format. Adds extra functionalities like finding how
    many fingers are up or the distance between two fingers. Also
    provides bounding box info of the hand found.
    """

    def __init__(self, mode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5):
        """
        :param mode: In static mode, detection is done on each image: slower
        :param maxHands: Maximum number of hands to detect
        :param detectionCon: Minimum Detection Confidence Threshold
        :param minTrackCon: Minimum Tracking Confidence Threshold
        """

        self.mode = mode
        self.maxHands = maxHands
        self.modelComplexity = modelComplexity
        self.detectionCon = detectionCon
        self.minTrackCon = minTrackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplexity,
                                        self.detectionCon, self.minTrackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        self.fingers = []
        self.lmList = []

    def findHands(self, img, draw=True, flipType=True):
        """
        Finds hands in a BGR image.
        :param img: Image to find the hands in.
        :param draw: Flag to draw the output on the image.
        :param flipType:
        :return: Image with or without drawings
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        allHands = []
        h, w, c = img.shape
        if self.results.multi_hand_landmarks:
            for handType, handLms in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                myHand = {}
                # lmList
                mylmList = []
                xList = []
                yList = []
                for id, lm in enumerate(handLms.landmark):
                    px, py = int(lm.x * w), int(lm.y * h)
                    mylmList.append([px, py])
                    xList.append(px)
                    yList.append(py)

                    # wrist
                    if id == 0:
                        cv2.circle(img, (px, py), circleRadius2, red, cv2.FILLED)
                        cv2.putText(img, str(int(id)), (px + 15, py), cv2.FONT_HERSHEY_PLAIN, fontSize1, red,
                                    fontThickness1)
                    # thumb tips
                    elif id == 4:

                        cv2.circle(img, (px, py), circleRadius2, green, cv2.FILLED)
                        cv2.putText(img, str(int(id)), (px + 15, py), cv2.FONT_HERSHEY_PLAIN, fontSize1, green,
                                    fontThickness1)
                    # other tips
                    elif id in (8, 12, 16, 20):
                        cv2.circle(img, (px, py), circleRadius2, green, cv2.FILLED)
                        cv2.putText(img, str(int(id)), (px + 15, py), cv2.FONT_HERSHEY_PLAIN, fontSize1, green,
                                    fontThickness1)
                    # other parts
                    else:
                        cv2.circle(img, (px, py), circleRadius2, white, cv2.FILLED)
                        cv2.putText(img, str(int(id)), (px + 15, py), cv2.FONT_HERSHEY_PLAIN, fontSize1, white,
                                    fontThickness1)

                # bbox
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                boxW, boxH = xmax - xmin, ymax - ymin
                bbox = xmin, ymin, boxW, boxH
                cx, cy = bbox[0] + (bbox[2] // 2), bbox[1] + (bbox[3] // 2)

                myHand["lmList"] = mylmList
                myHand["bbox"] = bbox
                myHand["center"] = (cx, cy)

                if flipType:
                    if handType.classification[0].label == "Right":
                        myHand["type"] = "Left"
                    else:
                        myHand["type"] = "Right"
                else:
                    myHand["type"] = handType.classification[0].label
                allHands.append(myHand)

                # draw
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
                    cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
                                  (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),
                                  purple, lineThickness2)
                    cv2.putText(img, myHand["type"], (bbox[0] - 30, bbox[1] - 30), cv2.FONT_HERSHEY_PLAIN,
                                fontSize2, purple, fontThickness2)
        if draw:
            return allHands, img
        else:
            return allHands

    def fingersUp(self, myHand):
        """
        Finds how many fingers are open and returns in a list.
        Considers left and right hands separately
        :return: List of which fingers are up
        """
        myHandType = myHand["type"]
        myLmList = myHand["lmList"]
        if self.results.multi_hand_landmarks:
            fingers = []

            # TODO: fix thumb not recognizing problem (ti - mrp)
            # right thumb
            if myHandType == "Right":
                if abs(myLmList[self.tipIds[0]][0] - myLmList[self.tipIds[1] + 1][0]) > 50:
                    if abs(myLmList[self.tipIds[0]][0] - myLmList[self.tipIds[0] + 2][0]) < 30 or abs(
                            myLmList[self.tipIds[0]][0] - myLmList[self.tipIds[1] + 2][0]) < 30:
                        fingers.append(0)
                    else:
                        fingers.append(1)
                else:
                    fingers.append(0)
            # left thumb
            else:
                if abs(myLmList[self.tipIds[0]][0] - myLmList[self.tipIds[1] + 1][0]) > 50:
                    if abs(myLmList[self.tipIds[0]][0] - myLmList[self.tipIds[0] + 2][0]) < 30 or abs(
                            myLmList[self.tipIds[0]][0] - myLmList[self.tipIds[1] + 2][0]) < 30:
                        fingers.append(0)
                    else:
                        fingers.append(1)
                else:
                    fingers.append(0)

            # 4 fingers
            for id in range(1, 5):
                if myLmList[0][1] > myLmList[self.tipIds[2]][1]:
                    if myLmList[self.tipIds[id]][1] < myLmList[self.tipIds[id] - 2][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                else:
                    if myLmList[self.tipIds[id]][1] < myLmList[self.tipIds[id] - 2][1]:
                        fingers.append(0)
                    else:
                        fingers.append(1)

        return fingers

    # noinspection PyMethodMayBeStatic
    def findDistance(self, p1, p2, img=None, draw=True):
        """
        Find the distance between two landmarks based on their
        index numbers.
        :param p1: Point1
        :param p2: Point2
        :param img: Image to draw on.
        :param draw: Flag to draw the output on the image.
        :return: Distance between the points
                 Image with output drawn
                 Line information
        """

        x1, y1 = p1
        x2, y2 = p2
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        length = math.hypot(x2 - x1, y2 - y1)
        info = (x1, y1, x2, y2, cx, cy)
        if draw is True:
            cv2.circle(img, (x1, y1), circleRadius1, blue, cv2.FILLED)
            cv2.circle(img, (x2, y2), circleRadius1, blue, cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), blue, 3)
            cv2.circle(img, (cx, cy), circleRadius1, blue, cv2.FILLED)

            return length, info, img
        else:
            return length, info


def main():
    """
    Dummy codes for testing.
    """
    cap = cv2.VideoCapture(0)
    detector = HandDetector(detectionCon=0.8, maxHands=2)
    while True:
        # get image frame
        success, img = cap.read()
        img = cv2.flip(img, 1)  # flip for webcam
        # find the hand and its landmarks
        hands, img = detector.findHands(img, flipType=False)  # with draw
        # hands = detector.findHands(img, draw=False)  # without draw

        if hands:
            # hand 1
            hand1 = hands[0]
            lmList1 = hand1["lmList"]  # list of 21 landmark points
            bbox1 = hand1["bbox"]  # bounding box info x,y,w,h
            centerPoint1 = hand1['center']  # center of the hand cx,cy
            handType1 = hand1["type"]  # hand type left or right
            fingers1 = detector.fingersUp(hand1)

            print(f"{handType1} Hand, Center = {centerPoint1}, Fingers = {fingers1}")

            if len(hands) == 2:
                # hand 2
                hand2 = hands[1]
                lmList2 = hand2["lmList"]  # list of 21 landmark points
                bbox2 = hand2["bbox"]  # bounding box info x,y,w,h
                centerPoint2 = hand2['center']  # center of the hand cx,cy
                handType2 = hand2["type"]  # hand Type "Left" or "Right"
                fingers2 = detector.fingersUp(hand2)

                print(f"{handType2} Hand, Center = {centerPoint2}, Fingers = {fingers2}")

                # find Distance between two Landmarks. (could be same hand or different hands)
                length, info, img = detector.findDistance(lmList1[8], lmList2[8], img)  # with draw
                # length, info = detector.findDistance(lmList1[8], lmList2[8])  # with draw

                print("")

        # display
        cv2.imshow("HandTrackingModule", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
