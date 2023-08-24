from time import sleep
import threading
import cv2
from cvzone.HandTrackingModule import HandDetector
from HMM import HMM


class Test:
    def __init__(self):
        self.hands = range(6)
        self.cap = cv2.VideoCapture(0)
        self.detector = HandDetector(detectionCon=0.8)
        self.fingers = []
        self.Button_state = False
        self.pre = ''
        self.HMM = HMM()

    def Video(self):
        self.cap.set(3, 1280)
        self.cap.set(4, 720)
        while True:
            success, img = self.cap.read()
            hands, img2 = self.detector.findHands(img)
            if len(hands) != 0:
                self.fingers = self.detector.fingersUp(hands[0])
            Img = cv2.flip(img, 1)
            cv2.imshow("Image", Img)
            cv2.waitKey(1)

    def Count(self):
        while True:
            sleep(3)
            sum1 = sum(self.fingers)
            self.fingers = range(6)
            if sum1 in [0, 2, 5]:
                if sum1 == 2:
                    print('your: scissors')
                    self.pre = self.pre + 'J'
                elif sum1 == 0:
                    print('your: stone')
                    self.pre = self.pre + 'S'
                elif sum1 == 5:
                    print('your: cloth')
                    self.pre = self.pre + 'B'
                if len(self.pre) == 5:
                    print(self.HMM.HiddenMarkovModels(self.pre, fit=True),
                          '\n---------------FIXED----------------')
                    self.pre = ''
                elif len(self.pre) != 0:
                    print(self.HMM.HiddenMarkovModels(self.pre[-1], fit=False),
                          '\n---------------SENDING---------------')


test = Test()

thread1 = threading.Thread(target=test.Video)
thread2 = threading.Thread(target=test.Count)

thread1.start()
thread2.start()
