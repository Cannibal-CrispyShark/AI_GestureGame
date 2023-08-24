import sys
import cv2
import numpy as np
import pandas as pd

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QTableWidgetItem as QTT
from cvzone.HandTrackingModule import HandDetector
from HMM import HMM
from UI_MainVideoWindow import *


class Video_Predict():
    def __init__(self):
        self.capture = cv2.VideoCapture(0)
        self.currentFrame = np.array([])
        self.previousFrame = np.array([])

        self.Button_state = False
        self.detector = HandDetector(detectionCon=0.8,maxHands=1)
        self.hands = range(6)
        self.pre = ''
        self.HMM = HMM()
        self.fingers = []
        self.sum1 = 1

        self.Record = ''

    def captureFrame(self):
        ret, readFrame = self.capture.read()
        return readFrame
    def captureNextFrame(self):
        ret, readFrame = self.capture.read()
        self.hands, img2 = self.detector.findHands(readFrame)
        if len(self.hands) != 0:
            self.fingers = self.detector.fingersUp(self.hands[0])
            self.sum1 = sum(self.fingers)
        if ret:
            self.currentFrame = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    def convertFrame(self):
        try:
            height, width = self.currentFrame.shape[:2]
            img = QImage(cv2.flip(self.currentFrame, 1),
                         width,
                         height,
                         QImage.Format_RGB888)
            img = QPixmap.fromImage(img)
            self.previousFrame = self.currentFrame
            return img
        except:
            print('fail to convert currentFrame to img')
            return None
    def HMM_Predict(self):
        print('-------------')
        Pos=self.sum1
        if self.sum1 in [0, 2, 5]:
            if self.sum1 == 2 and len(self.hands) != 0:
                print('your: scissors')
                print('-------------')
                self.pre = self.pre + 'J'
                self.Record = self.Record + 'J'
            elif self.sum1 == 0:
                print('your: stone')
                print('-------------')
                self.pre = self.pre + 'S'
                self.Record = self.Record + 'S'
            elif self.sum1 == 5:
                print('your: cloth')
                print('-------------')
                self.pre = self.pre + 'B'
                self.Record = self.Record + 'B'
            self.sum1 = 1
            if len(self.pre) == 5:
                res = self.HMM.HiddenMarkovModels(self.pre, fit=True)
                print(res)
                self.pre = ''
                return Pos,res
            elif len(self.pre) != 0:

                res = self.HMM.HiddenMarkovModels(self.pre, fit=False)
                print(res)
                return Pos,res
        else:
            print('Waiting...')
            return 'Waiting...'
    def advance_Predict(self):
        if self.Record!='':
            self.HMM.HiddenMarkovModels(self.Record, fit=True)

class VideoUI(QMainWindow, Nihao_Ui_MainWindow):
    def __init__(self, parent=None):
        super(VideoUI, self).__init__(parent)
        self.setupUi(self)

        self.VP = Video_Predict()
        self.Video_timer = QTimer(self)
        self.Video_timer.timeout.connect(self.play)
        self.Video_timer.start(27)

        self.HMM_timer = QTimer(self)
        self.HMM_timer.timeout.connect(self.HMM_Predict)
        self.HMM_timer.start(3000)

        self.time = 0
        self.Clock = QTimer(self)
        self.Clock.timeout.connect(self.Timer)
        self.Clock.start(1000)

        self.update()
        self.videoFrame = self.label_Video

        self.ret, self.capturedFrame = self.VP.capture.read()
        self.df = pd.read_csv('user.csv')
        self.dataForm = pd.read_csv('user.csv')
        del self.dataForm[self.df.columns[0]]
        del self.dataForm['Secret']
        del self.dataForm['Log']

        self.Id = -1
        self.Win = 0
        self.All = 0
    def getId(self, index):
        self.Id = index
    def loadinData(self):
        self.Win = int(self.df.loc[[self.Id], 'Win'])
        self.All = int(self.df.loc[[self.Id], 'All'])
        self.VP.Record = str(self.df.loc[[self.Id], 'Log'].values).strip('[]')
        self.VP.Record.strip()
        if self.VP.Record=='nan':
            self.VP.Record=''
            self.All-=5
        self.VP.advance_Predict()

    def closeEvent(self, event):
        self.pushData()
        event.accept()
    def pushData(self):
        self.df.at[self.Id, 'Win']=self.Win
        self.df.at[self.Id, 'All'] = self.All
        #数据清洗
        self.VP.Record = [char for char in self.VP.Record if char in ['S', 'J', 'B']]
        self.df.at[self.Id, 'Log']=self.VP.Record
        self.df.at[self.Id, 'Rate'] = str((float(self.Win) / self.All)*100) + '%'
        del self.df[self.df.columns[0]]
        self.df.to_csv('user.csv')
        print('Push_Success')
    def HMM_Predict(self):
        self.time = 0
        myPos,*res = self.VP.HMM_Predict()
        if res == ['its: stone']:
            self.JSBwindows.setCurrentIndex(2)
            if myPos == 5: self.Win += 1
            self.All += 1
        if res == ['its: scissors']:
            self.JSBwindows.setCurrentIndex(1)
            if myPos == 0: self.Win += 1
            self.All += 1
        if res == ['its: cloth']:
            self.JSBwindows.setCurrentIndex(3)
            if myPos == 2: self.Win += 1
            self.All += 1
        if res == ['a', 'i', 't', 'i', 'n', 'g', '.', '.', '.']:
            self.JSBwindows.setCurrentIndex(0)
    def Timer(self):
        self.time %= 3
        self.stackedWidget_2.setCurrentIndex(self.time)
        self.time += 1
    def show_Ranking(self):
        self.stackedWidget.setCurrentIndex(1)
        self.HMM_timer.stop()
        self.Clock.stop()
        self.creatRankingForm()
    def createRankingForm(self):
        NumColumns = 4
        NumRows = len(self.dataForm.index)
        print(type(self.dataForm.index))
        print(self.dataForm.head())
        self.DataWidgit.setColumnCount(NumColumns)
        self.DataWidgit.setRowCount(NumRows)
        # headItem=QtWidgets.QTableWidgetItem()
        # headItem=self.dataForm.columns
        # headItem = [QTableWidgetItem(col) for col in self.dataForm.columns]
        # brush = QtGui.QBrush(QtGui.QColor(76, 140, 255))
        # brush.setStyle(QtCore.Qt.SolidPattern)
        # headItem.setForeground(brush)
        self.DataWidgit.setHorizontalHeaderLabels(self.dataForm.columns)
        self.DataWidgit.horizontalHeader().setStyleSheet("color: rgb(0, 0, 255);")
        for i in range(NumRows):
            for j in range(len(self.dataForm.columns)):
                Item= QTT(str(self.dataForm.iat[i, j]))
                Item.setFont(QFont('Times', 14, QFont.Black))
                Item.setBackground(QBrush(QColor(137, 207, 240)))
                self.DataWidgit.setItem(i, j, Item)
        self.DataWidgit.resizeRowsToContents()
        self.DataWidgit.horizontalHeader().setStretchLastSection(True)
    def show_Game(self):
        self.stackedWidget.setCurrentIndex(0)
        self.HMM_timer.start(3000)
        self.Clock.start(1000)
    def play(self):
        try:
            self.VP.captureNextFrame()
            self.videoFrame.setPixmap(self.VP.convertFrame())
            self.videoFrame.setScaledContents(True)
        except TypeError:
            print('No Frame')

