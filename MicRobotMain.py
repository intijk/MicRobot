# coding=UTF-8
#system
import sys,os,time
import math
import numpy as np
import openni
import serial
from functools import partial
#PyQt5
from PyQt5 import QtCore
from PyQt5.QtCore import Qt,QObject,QTimer,QUrl,QFileInfo
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage,QPixmap,QPen,QColor,QPainter,QIcon
#Project
import KinectSensor as KS
from MicRobot import MicRobot
import mapTable

class AngleInfo(QObject):
	swingAngleV=0
	armAngleV=0
	armSpringAngleV=0
	armFrontAngleV=0
	KMConnectedV=False
	def _swingAngle(self):
		return self.swingAngleV;
	def _armAngle(self):
		return self.armAngleV;
	def _armSpringAngle(self):
		return self.armSpringAngleV;
	def _armFrontAngle(self):
		return self.armFrontAngleV;
	def _KMConnected(self):
		return self.KMConnectedV;

	def _swingAngleS(self,v):
		self.swingAngleV=v;
	def _armAngleS(self,v):
		self.armAngleV=v;
	def _armSpringAngleS(self,v):
		self.armSpringAngleV=v;
	def _armFrontAngleS(self,v):
		self.armFrontAngleV=v;

		#return swingAngleV;
	swingAngle=QtCore.pyqtProperty(float, fget=_swingAngle,fset=_swingAngleS);
	armAngle=QtCore.pyqtProperty(float, fget=_armAngle,fset=_armAngleS);
	armSpringAngle=QtCore.pyqtProperty(float,
			fget=_armSpringAngle,fset=_armSpringAngleS);
	armFrontAngle=QtCore.pyqtProperty(float,
			fget=_armFrontAngle,fset=_armFrontAngleS);
	KMConnected=QtCore.pyqtProperty(bool, fget=_KMConnected);

class RefreshTimerThread(QtCore.QThread):
	#trigger=QtCore.pyqtSignal(int)
	KinectFail=QtCore.pyqtSignal() 
	KinectReady=QtCore.pyqtSignal() 
	joint_request=['head','neck',
			'torso','left_shoulder','left_elbow','left_hand']
	joint_list=[]
	joint_dic={}
	refreshInterval=0.041

	def __init__(self,parent=None):
		super(RefreshTimerThread,self).__init__(parent)
		#self.initTimer()
	def setup(self, m):
		self.m=m
	def run(self):
		while True:
			#time.sleep(0.001)
			time.sleep(self.refreshInterval)
			self.refresh();
	def initTimer(self):
		self.timer=QTimer()
		self.timer.timeout.connect(self.refresh)
		self.timer.start(11)
		#self.kstimer=QTimer()
		#self.kstimer.timeout.connect(self.refresh)	
		#self.kstimer.start(41)
	def dist(self,a,b,d=3):
		s=0
		for i in range(d):
			s+=(a[i]-b[i])*(a[i]-b[i])
		return math.sqrt(s)	

			
	def armTranspose(self):
		if len(self.joint_request) != len(self.joint_list):
			#print "need all %d points for transpose" % len(self.joint_request)
			return
		for i in range(len(self.joint_request)):
			self.joint_dic[self.joint_request[i]]=self.joint_list[i]
		j=self.joint_dic	
		u=self.dist(j['head'], j['torso'])/2

		head_x=j['head'][0]
		head_y=j['head'][1]
		head_d=j['head'][2]


		hand_x=j['left_hand'][0]
		hand_y=j['left_hand'][1]
		hand_d=j['left_hand'][2]

		torso_x=j['torso'][0]
		torso_y=j['torso'][1]
		torso_d=j['torso'][2]

		self.m.angleInfo.swingAngleV=math.atan2(torso_d-hand_d, torso_x-hand_x)#+math.pi/2
		
		h=(head_y-torso_y)
		u=h/1.5	
		dx=-1*math.sqrt((torso_x-hand_x)*(torso_x-hand_x)+(torso_d-hand_d)*(torso_d-hand_d))
		dy=-1*(torso_y-hand_y)
		ux=dx/u
		uy=dy/u
		mx=ux*230/3;
		mx+=250;
		my=uy*230/3;

		try:
			if int(mx)>=-230 and int(mx)<230 and int(my)>0 and int(my)<230 and mapTable.mapTable[int(mx)][int(my)][0] > -3.14:
				self.m.angleInfo.armAngleV=mapTable.mapTable[int(mx)][int(my)][0]/180.0*math.pi
				self.m.angleInfo.armSpringAngleV=mapTable.mapTable[int(mx)][int(my)][1]/180.0*math.pi
				self.m.angleInfo.armFrontAngleV=mapTable.mapTable[int(mx)][int(my)][2]/180.0*math.pi
		except IndexError:
			print "out of robot range"
			


	def hmapping(self,value, ulimit=3000, llimit=1500):
		if value < llimit:
			value = llimit
		elif value >ulimit:
			value = ulimit
		return ((value-llimit)*300)/(ulimit-llimit)

		
			
	def refresh(self):
		#self.m.angleInfo.swingAngleV+=0.05
		#self.m.angleInfo.armAngleV=math.pi/6;
		#self.m.angleInfo.armSpringAngleV=math.pi/6;
		#self.m.angleInfo.armFrontAngleV=math.pi/6;

		refreshDepthImage=None
		refreshImageImage=None
		
		if self.m.KSAvailable!=True:
			refreshDepthImage=self.m.imgBlank
			refreshImageImage=self.m.imgBlank
		else:
			try:
				#RGB Image
				imageFrame=KS.readImage()
				self.m.imageList[self.m.imgpos]=(
						QImage(imageFrame,640,480,
							QImage.Format_RGB888).rgbSwapped())
				refreshImageImage=self.m.imageList[self.m.imgpos]

				#Depth image
				frame=KS.readDepth()
				f=np.fromstring(frame,dtype=np.uint8)
				self.m.depthList[self.m.imgpos]=QImage(
						f.repeat(4),640,480,QImage.Format_RGB32)
				refreshDepthImage=self.m.depthList[self.m.imgpos]

				#Draw points on depth image
				skeleton_list = []
				KS.ctx.wait_and_update_all()
				user_list=[]
				for u_id in KS.userNode.users:
					readRet=KS.readSkeleton(self.joint_request, u_id)
					user_list.append(readRet)
					
				max_u=[[],[]]
				for u in user_list:
					if len(u[0])>=len(max_u[0]):
						max_u=u
				skeleton_list = max_u[0]
				self.joint_list=max_u[1]
				modifier = QPainter()
				color=QColor()
				modifier.begin(refreshDepthImage)
				for ske_joint in skeleton_list:
					if ske_joint[1] < 0:
						continue
					depth=self.hmapping(ske_joint[2])
					color.setHsv(depth,255,255)
					modifier.setPen(
							QPen(color,
								15, 
								cap=Qt.RoundCap)
							)
					modifier.drawPoint(ske_joint[0],ske_joint[1])

				modifier.end()	

			except openni.OpenNIError:
				self.m.KSAvailable=False
				print 'Kinect Sensor disconnected.'
				self.m.KSCheck('failurecheck');
				return 
		self.armTranspose()
		#Depth	
		self.m.depthLabel.setPixmap(
				QPixmap.fromImage(refreshDepthImage.scaled(
						self.m.depthLabel.width(),self.m.depthLabel.height(),
						Qt.KeepAspectRatio))
				)
		#Image
		self.m.imageLabel.setPixmap(
				QPixmap.fromImage(refreshImageImage.scaled(
					self.m.imageLabel.width(),self.m.imageLabel.height(),
					Qt.KeepAspectRatio))
				)
		
		self.m.imgpos=1-self.m.imgpos;
class RefreshRobotThread(QtCore.QThread):
	refreshInterval=0.08
	def __init__(self,m):
		super(RefreshRobotThread,self).__init__()
		self.m=m
	def run(self):
		while True:
			time.sleep(self.refreshInterval)
			if self.m.MRConnected and self.m.Robot.connected:
				self.refresh()
	def refresh(self):
		print self.m.angleInfo.swingAngleV
		print self.m.angleInfo.armAngleV
		print self.m.angleInfo.armSpringAngleV
		print self.m.angleInfo.armFrontAngleV

		cmd="A %d %d %d %d %d" % (
				-1,
				int(self.m.angleInfo.armFrontAngleV/math.pi*180),
				int(self.m.angleInfo.armSpringAngleV/math.pi*180),
				int(self.m.angleInfo.armAngleV/math.pi*180),
				int(self.m.angleInfo.swingAngleV/math.pi*180)+90)
		print cmd
		try:
			self.m.Robot.write(cmd)
			self.m.Robot.ser.flushInput()
			self.m.Robot.ser.flushOutput()
		except serial.serialutil.SerialException:
			print "Refresh Robot Write Fail"




class MicRobotMain(QMainWindow):

	#For Kinect
	imgpos=0
	depthList=[]
	imageList=[]
	KSAvailable=False

	#For robot
	#pl=R.listActivePorts()
	#R.setPar(pl[0],115200)
	#R.connect()

	def __init__(self):
		super(MicRobotMain, self).__init__()
		self.initUI()

	def initSim(self):
		self.simView=QWebView()

		self.angleInfo=AngleInfo()
		self.simView.page().mainFrame().\
			addToJavaScriptWindowObject("angleInfo",self.angleInfo)

		self.simPath=QFileInfo("./html/index.html").absoluteFilePath()
		self.simView.setUrl(QUrl.fromLocalFile(self.simPath))
		self.simView.setWindowFlags(Qt.FramelessWindowHint)

	def initRobot(self):
		self.Robot=MicRobot()
		'''
		self.testLabel=QLabel()
		self.testLabel.setText("abc")
		self.testSlider=QSlider(Qt.Horizontal)
		self.testSlider.setRange(0,180)
		self.testSlider.setValue(0)
		self.testSlider.valueChanged.connect(self.fun)
		'''

	def initKinectUI(self):
		#UI For Kinect RGB image and Depth image
		self.imgBlank=QImage("./image/kinect.png")

		self.depthLabel=QLabel()
		self.imageLabel=QLabel()
		self.depthLabel.setAlignment(Qt.AlignCenter)
		self.imageLabel.setAlignment(Qt.AlignCenter)

		self.depthList.append(self.imgBlank)
		self.depthList.append(self.imgBlank)
		self.imageList.append(self.imgBlank)
		self.imageList.append(self.imgBlank)
	
		self.depthLabel.setPixmap(QPixmap.fromImage(self.imgBlank).scaled(
										self.depthLabel.width(),
										self.depthLabel.height(),
										Qt.KeepAspectRatio))
	
		self.imageLabel.setPixmap(QPixmap.fromImage(self.imgBlank).scaled(
										self.depthLabel.width(),
										self.depthLabel.height(),
										Qt.KeepAspectRatio))
		
	def initCommLayerUI(self):
		self.imgKinectAvailable=QImage("./image/kinect_available.png")
		self.imgKinectDisable=QImage("./image/kinect_disable.png")
		self.imgRobotAvailable=QImage("./image/robot_available.png")
		self.imgRobotDisable=QImage("./image/robot_disable.png")
		self.imgMain=QImage("./image/microbot_long.png")
		self.commKinectLabel=QLabel()
		self.commMainLabel=QLabel()
		self.commRobotLabel=QLabel()
		self.commKinectLabel.setPixmap(QPixmap.fromImage(self.imgKinectAvailable))
		self.commMainLabel.setPixmap(QPixmap.fromImage(self.imgMain))
		self.commRobotLabel.setPixmap(QPixmap.fromImage(self.imgRobotDisable))
		#K Kinect
		#M Main
		#R Robot

		#self.commKMLabel=QLabel()
		#self.commMRLabel=QLabel()
		#self.imgConnected=QImage("./image/connected.png")
		#self.imgDisconnected=QImage("./image/disconnected.png")
		#self.commKMLabel.setPixmap(QPixmap.fromImage(self.imgDisconnected))
		#self.commMRLabel.setPixmap(QPixmap.fromImage(self.imgDisconnected))
		self.pmConnected=QPixmap("./image/connected.png")
		self.pmDisconnected=QPixmap("./image/disconnected.png")
		self.iconConnected=QIcon(self.pmConnected)
		self.iconDisconnected=QIcon(self.pmDisconnected)
		self.commKMButton=QPushButton()
		self.commMRButton=QPushButton()
		self.commKMButton.setIcon(self.iconDisconnected)
		self.commMRButton.setIcon(self.iconDisconnected)
		self.commKMButton.setIconSize(self.pmDisconnected.rect().size())
		self.commMRButton.setIconSize(self.pmDisconnected.rect().size())
		self.commKMButton.setDisabled(True)
		self.commMRButton.setDisabled(True)

		self.commLayerLayout=QHBoxLayout()
		self.commLayerLayout.addWidget(self.commKinectLabel)
		#self.commLayerLayout.addWidget(self.commKMLabel)
		self.commLayerLayout.addWidget(self.commKMButton)
		self.commLayerLayout.addWidget(self.commMainLabel)
		#self.commLayerLayout.addWidget(self.commMRLabel)
		self.commLayerLayout.addWidget(self.commMRButton)
		self.commLayerLayout.addWidget(self.commRobotLabel)
		self.commLayerLayout.setAlignment(Qt.AlignCenter)
		self.commLayerWidget=QWidget()
		self.commLayerWidget.setLayout(self.commLayerLayout)

		self.MRConnected=False
		self.KMConnected=False
		self.commMRButton.clicked.connect(self.MRButtonClick)
		self.commKMButton.clicked.connect(self.KMButtonClick)

	def disconnectKM(self):
		self.KMConnected=False
		self.angleInfo.KMConnectedV=False
		self.commKMButton.setIcon(self.iconDisconnected)

	def connectKM(self):
		self.KMConnected=True
		self.angleInfo.KMConnectedV=True
		self.commKMButton.setIcon(self.iconConnected)

	def disconnectMR(self):
		self.MRConnected=False
		self.commMRButton.setIcon(self.iconDisconnected)
	def connectMR(self):
		self.MRConnected=True
		self.commMRButton.setIcon(self.iconConnected)

	def KMButtonClick(self):
		if self.KMConnected:
			self.disconnectKM()
		else:
			self.connectKM()

	def MRButtonClick(self):
		if self.MRConnected:
			self.disconnectMR()
		else:
			self.connectMR()
		
	def initRefreshTimer(self):
		self.refreshThread=RefreshTimerThread()
		self.kstimer=QTimer()
		self.refreshThread.setup(self)
		self.refreshThread.start()
		self.kstimer.start(1000)


	def initKSCheckTimer(self):
		self.kschecktimer=QTimer()
		self.kschecktimer.timeout.connect(
			partial(self.KSCheck,trigger='timercheck'))
		self.kschecktimer.start(40)

	def initRobotTimer(self):
		self.robotTimer=QTimer()
		self.robotTimer.timeout.connect(self.Robot.checkAvailable)
		self.robotTimer.start(1000)
			
		self.refreshRobotThread=RefreshRobotThread(self)
		self.robottimer=QTimer()
		self.refreshRobotThread.start()

	def initUI(self):
		self.initSim()
		self.initRobot()
		self.initKinectUI()
		self.initCommLayerUI()
		#Construcet Left UI	
		self.leftLayout=QVBoxLayout()
		self.leftLayout.addWidget(self.commLayerWidget)
		self.leftLayout.addWidget(self.imageLabel)
		self.leftLayout.addWidget(self.depthLabel)
		self.leftSide=QWidget()
		self.leftSide.setLayout(self.leftLayout)
		self.leftSide.setWindowFlags(Qt.FramelessWindowHint)
		#Construct splitter	
		self.split=QSplitter(Qt.Horizontal)
		self.split.addWidget(self.leftSide)
		self.split.addWidget(self.simView)
		#Init timers
		self.initRefreshTimer()
		self.connectComm()
		self.initKSCheckTimer()
		self.initRobotTimer()
		#show
		self.split.show()
		#self.split.showFullScreen()

		self.commKinectLabel.setScaledContents(True)
	def kinectReady(self):
		self.commKinectLabel.setPixmap(QPixmap.fromImage(self.imgKinectAvailable))
		self.commKMButton.setEnabled(True)
	def kinectFail(self):
		self.commKinectLabel.setPixmap(QPixmap.fromImage(self.imgKinectDisable))
		self.disconnectKM()
		self.commKMButton.setDisabled(True)
	def robotReady(self):
		self.commRobotLabel.setPixmap(QPixmap.fromImage(self.imgRobotAvailable))
		self.commMRButton.setEnabled(True)
	def robotFail(self):
		self.commRobotLabel.setPixmap(QPixmap.fromImage(self.imgRobotDisable))
		self.disconnectMR()
		self.commMRButton.setDisabled(True)

	def connectComm(self):
		self.refreshThread.KinectReady.connect(self.kinectReady)
		self.refreshThread.KinectFail.connect(self.kinectFail)
		self.Robot.serReady.connect(self.robotReady)
		self.Robot.serFail.connect(self.robotFail)


	#Check kinect availability
	def KSCheck(self,trigger):
		if trigger=='timercheck':
			if self.KSAvailable!=True and KS.deviceAvailable():
				####Here may also fail
				KS.startAll()
				self.KSAvailable=True
				self.refreshThread.KinectReady.emit()
		elif trigger=='failurecheck':
			print "failurecheck"
			KS.reInit()
			if not KS.deviceAvailable():
				print "failurecheck failed"
				self.KSAvailable=False
				self.refreshThread.KinectFail.emit()


