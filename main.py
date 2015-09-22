import sys,os
from PyQt5.QtWidgets import	QApplication
from MicRobotMain import MicRobotMain 

def main():
	app=QApplication(sys.argv)
	micRobot=MicRobotMain()
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
