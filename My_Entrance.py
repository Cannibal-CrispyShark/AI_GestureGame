import sys

import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow
from loginWindow import *
from PyQt5.QtCore import Qt
from Main_Video_Window import *

class login(QMainWindow, Ui_MainWindow_Login):
    def __init__(self, parent=None):
        super(login, self).__init__(parent)
        self.setupUi(self)

        self.name = ''
        self.password = ''
    def saveName(self, QString):
        # global name
        self.name = QString
    def savePassword(self, QString):
        # global password
        self.password = QString
    def echoWaringLand(self, value):
        if value==QMessageBox.Yes:
            self.password_edit.setText('')
        if value==QMessageBox.No:
            self.password_edit.setText('')
            self.name_edit.setText('')
    def waringLand(self,event):  # 消息：警告
        reply = QMessageBox.warning(self,
                                    "警告",
                                    event,
                                    QMessageBox.Yes | QMessageBox.No)
        self.echoWaringLand(reply)
    def waringRegisterToLand(self,event):  # 消息：警告
        reply = QMessageBox.warning(self,
                                    "警告",
                                    event,
                                    QMessageBox.Yes | QMessageBox.No)
        self.echoRegisterToLand(reply)
    def echoRegisterToLand(self, value):
        if value==QMessageBox.No:
            self.password_edit.setText('')
            self.name_edit.setText('')
    def waring(self,event):  # 消息：警告
        reply = QMessageBox.warning(self,
                                    "警告",
                                    event,
                                    QMessageBox.Yes | QMessageBox.No)
        pass
    def register(self):
        if len(self.name)==0 :
            self.waring('用户名不能为空')
        if len(self.name)>0 and len(self.password)<5:
            self.waring('密码不少于5位数')
        if len(self.name) >0 and len(self.password) >= 5:
            user=pd.read_csv('user.csv')
            register_flag = 0
            if self.name in user.loc[:'Account'].values:
                self.waringRegisterToLand('该用户已经注册，请登录')
                register_flag += 1
            if register_flag == 0:
                user.loc[len(user.index)]=[user.shape[0],self.name,self.password,0,0,np.nan,np.nan]
                user.to_csv('user.csv')
                self.success.setText('恭喜用户：' + self.name + ' 注册成功')
                self.success.adjustSize()
                self.success.setWordWrap(True)
                self.success.setAlignment(Qt.AlignCenter)
                self.name_edit.setText('')
                self.password_edit.setText('')
    def land(self):
        if len(self.name)==0 :
            self.waring('用户名不能为空')
        if len(self.name)>0 and len(self.password)<5:
            self.waring('密码不少于5位数')
        if len(self.name) > 0 and len(self.password) >= 5:
            user = pd.read_csv('user.csv')
            land_flag = 0
            index=user[user.Account.apply(str) == self.name].index.tolist()[0]
            if (self.name in str(user.loc[:'Account'].values)) and (self.password == str(user.loc[[index],'Secret'].values[0])):
                land_flag += 1
                mainWindows_show.getId(index)
                mainWindows_show.loadinData()
                mainWindows_show.show()
                login_show.hide()
            elif (self.name in str(user.loc[:'Account'].values)) and (self.password != str(user.loc[[index],'Secret'].values[0])):
                self.waringLand('密码错误，请重新输入')
                land_flag += 1

            if land_flag == 0:
                self.success.setText(self.name + '没有注册，请注册之后再登陆')
                self.success.adjustSize()
                self.success.setWordWrap(True)
                self.success.setAlignment(Qt.AlignCenter)


app = QApplication(sys.argv)
login_show=login()
login_show.show()
mainWindows_show = VideoUI()
sys.exit(app.exec_())