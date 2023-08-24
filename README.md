# AI_GestureGame
## 写在前面：
##### 隐马尔可夫算法预测猜拳小游戏


作者新手一枚

欢迎指点：QQ 3230542759
###### 文件目录
│  forecast.py

│  HMM.py

│  loginWindow.py

│  loginWindow.ui

│  Main_Video_Window.py

│  My_Entrence.py

│  UI_MainVideoWindow.py

│  UI_MainVideoWindow.ui

│  user.csv

│  

└─img
       

## 环境
cvzone==1.5.6

mediapipe==0.10.2

numpy==1.24.4

opencv-contrib-python==4.8.0.74

opencv-python==4.7.0.72

pomegranate==1.0.0

pyqt5-tools==5.15.9.3.3

PyQt5==5.15.9

PySide2==5.15.2.1

## 启动方式
运行My_Entrance.py


## 代码
### 视频
- cv2.VideoCapture，获取摄像头的帧图
- 调用cv2中的HandDetector，通过fingerUp函数分析手指UP个数，从而知道使用者出的什么招式（剪刀石头布）
- 将cv2的视频导入pyqt5：转换cv2的img的格式，适配pyqt5中的Qlabel
### 算法：HiddenMarkovModels    （隐马尔科夫模型）
- 概括
	- 通过“隐状态”这个背景信息来推断表状态
	- 天下雨(隐状态)——>不出门(表状态)
	- AND
	- 不出门——>天下雨，通过不出门来确定隐状态是天下雨，隐状态（天下雨）又可以推出表状态：不出门
- 调用算法库pomegranate
	- from pomegranate.hmm import SparseHMM
	- 初始化各个“隐状态”概率
	- 导入“视频”和“数据库”的数据，进行拟合
### “数据库”：user.csv
- pandas模块操作csv文件，实现类似数据库的功能
- 在运行结束时，重写close函数。清洗并记录figerUp检测出的招式，用户Account，Secret和胜率等信息
- 算法启动时，载入”数据库“用户出招记录，对模型进行预训练
- 导入”前端“Ranking页面中，展示游戏排名
## pyqt5
### 该项目有两个UI
### “登陆”Log_In
- log_in对象继承pyuic5自动生成的UI.py
- ![](causally/handpose_model/my_Try/img/Show_login.jpg)
### "游戏“Gesture_Game
- VideoUI继承自pyuic5自动生成的UI.py，所列函数在其中完成相应功能
- QMenu中QAction对应的函数切换栈容器stackwidget，实现游戏页面与Ranking页面的转跳
- stackwidget+Qtimer实现计时器，每隔三秒进行一次猜拳
- stackwidget+Qtimer+隐马尔科夫模型，实现游戏对话框
- 排名页面，由”数据库“user.csv导出，给出玩家胜率的排名

![](causally/handpose_model/my_Try/img/show_main2.jpg)
