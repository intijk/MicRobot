This project is written in Python and html.

Library used listed below:
OpenNI -- for Kinect and Skeleton
PyQt   -- GUI
PySerial -- Serial access


Program Files
-------
MicRobotMain.py
This is the main file for program logic, including the refresh of GUI, skeleton
retrieving and robot. 

MicRobot.py
Code for control the robot.

KinectSensor.py
This part is the code to call OpenNI library.

html/
In thif folder, it is the interface for 3D robot simulator. WebGL is used for
quick 3D view.



Thread Models
-------
We use 3 threads to process the logic of program, for fully use the hardware and
avoid any stuck of GUI..

1. Main thread
   This is the main GUI thread.

2. KinectRefresh thread
   This thread will update the skeleton information and refresh image frame and
depth image frame. 

3. RobotRefresh thread
   This thread read data written by KinectRefresh thread or by user manully
dragging of simulator angles, and write angle infromation to serail.


Robot and Firmware
----
Robot is a 3D printing project, started by Ben-Tommy Eriksen on Thingiverse and
rebuild by Holger O., mine work http://www.thingiverse.com/thing:234482 is based
on their great effort and made my own modification. The firmware is totally
rewritten by us:

https://github.com/intijk/armrobot
