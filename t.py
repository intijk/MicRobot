import sys
from MicRobot import MicRobot
from PyQt5 import QtCore
from PyQt5.QtCore import Qt,QObject,QTimer,QUrl,QFileInfo
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage,QPixmap,QPen,QColor,QPainter


class Example(QMainWindow):
	def __init__(self):
		super(Example,self).__init__()
		self.initUI()
		self.initRobot()
		self.initTimer()
		self.label.show()

	def initUI(self):
		self.imgAvailable=QImage("./image/robot_available.png")
		self.imgDisable=QImage("./image/robot_disable.png")
		self.label=QLabel()
		self.label.setPixmap(QPixmap.fromImage(self.imgDisable))

	def initRobot(self):
		self.R=MicRobot()
		self.R.serReady.connect(self.robotReady)
		self.R.serFail.connect(self.robotFail)

	def robotReady(self):
		self.label.setPixmap(QPixmap.fromImage(self.imgAvailable))

	def robotFail(self):
		print 'robotFail'
		self.label.setPixmap(QPixmap.fromImage(self.imgDisable))

	def initTimer(self):
		self.timer=QTimer()	
		self.timer.timeout.connect(self.R.checkAvailable)
		self.timer.start(1000)
			
app=QApplication(sys.argv)
e=Example()
sys.exit(app.exec_())
