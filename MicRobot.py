import serial,time
import sys
from serial.tools import list_ports

from PyQt5 import QtCore
from PyQt5.QtCore import QObject
'''
class ReadThread(QtCore.QThread):
	def __init__(self,m):
		super(ReadThread,self).__init__()
		self.m=m
	def run(self):
		self.m.connected

class WriteThread(QtCore.QThread):
	def __init__(self,m):
		super(WriteThread,self).__init__()
		self.m=m
	def run(self):
		self.m.connected
'''
class CheckThread(QtCore.QThread):
	def __init__(self,m):
		super(CheckThread,self).__init__()
		self.m=m
	def run(self):
		pl=self.m.listActivePorts()
		buffer=''
		lines=[]
		find=False
		for p in pl:
			print "checking",p
			self.m.disconnect()
			self.m.setPar(p,self.m.baudrate)
			try:
				self.m.connectTouch()
				time.sleep(1)	
			except OSError:
				self.m.disconnect()
				self.m.serFail.emit()
				self.found=False
				break
			while True:
				try:
					b=self.m.ser.read()
					print b
				except serial.serialutil.SerialException:
					break
				if len(b)==0:
					if len(buffer)>0:
						lines.append(buffer)
						buffer=''
					break
				else:
					print "type(b)",type(b)
					print "ord(b)",ord(b)
					print "b",b
					#break;
					buffer+=b
					if b=='\n':
						lines.append(buffer)
						buffer=''
				print lines
	
			for l in lines:
				print l
				if "ArmRobot" in l:
					find=True
					print "Found Robot on",p
					self.m.found=True
					self.m.connected=True
					break
			if not find:
				self.m.disconnect()
		self.m.checking=False
		
		
class MicRobot(QtCore.QObject):
	'''Class for robot'''
	port=''
	baudrate=0
	ser=''
	connected=False
	found=False
	checking=False

	serReady=QtCore.pyqtSignal()
	serFail=QtCore.pyqtSignal()

	def __init__(self):
		super(MicRobot, self).__init__()
		self.port=''
		self.baudrate=115200
		self.ser=serial.Serial(port=None,baudrate=self.baudrate,timeout=0.5)
		self.lastWriteTime=-1
		self.initCheckThread()

	def checkAvailable(self):
		if self.connected==True:
			try:
				self.write("T test")
				self.serReady.emit()
			except serial.serialutil.SerialException:
				self.connected=False
				self.disconnect()
				print "writ T fail, emit fail"
				self.serFail.emit()
			#self.serFail.emit()
		else:
			if self.found==True:
				self.serReady.emit()
				self.found=False
			else:
				if not self.checking:
					self.checking=True
					self.serFail.emit()
					self.checkThread.start()

	def initCheckThread(self):
		self.checkThread=CheckThread(self)
		
	def listActivePorts(self):
		pl=list_ports.comports()
		ports=[x[0] for x in pl if x[2]!='n/a']
		return ports

	def setPar(self, port, baudrate=115200):
		self.port=port
		self.ser.port=port
		self.baudrate=baudrate
		#if self.ser!='' and self.ser.isOpen():
		#	self.reconnect();
		#print 'Set parameter to %s, %s' % (self.port, self.baudrate)
				
	def connect(self):
		self.ser.port=self.port
		if self.connected!=True:
			self.ser.open()
			self.ser.flushInput()
			self.ser.flushOutput()
			self.connected=True

	def connectTouch(self):
		print "connectTouch"
		self.ser.close()
		self.ser.open()
		self.ser.flushInput()
		self.ser.flushOutput()

	def disconnect(self):
		#if self.ser.isOpen():
		self.ser.close()
		self.connected=False

	def reconnect(self):
		self.disconnect()
		self.connect()
		print '%s connected' % self.port

	def write(self, cmd):
		if time.time()-self.lastWriteTime>0.04:
			print "time interval ok , start write"
			#self.ser.read()
			self.ser.write(cmd)
			self.lastWriteTime=time.time()
			self.ser.flush()
#r=MicRobot()
#pl=r.listActivePorts()
#print pl[1]
#r.setPar(pl[1]);
#
#r.connect()
#r.write("A 0 0 0 0 180")
#print "start waiting"
#time.sleep(110)
