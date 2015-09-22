Install OpenNI
===

OpenNI is the library developed by PrimeSense, that intent to provide standard interface for 3D sensor data processing algorithms.  The current newest version is OpenNI 2 but this one doesn’t work with Kinect so the only choice is OpenNI 1.5.4, which is proven to be friendly with Kinect.



Before compiling, please make sure all following modules are available in your environment:

GCC 4.x,  Python 2.6+, libusb 1.0.x, freeglut3, JDK 6.0

Get the source: git clone https://github.com/OpenNI/OpenNI.git

If you could't find it online, please find in the delivered tarball OpenNI.zip

Building OpenNI:
===

1. Go into the directory: "Platform/Linux/CreateRedist".   
	Run the script: "./RedistMaker".    
	This will compile everything and create a redist package in the "Platform/Linux/Redist" directory.      
	It will also create a distribution in the "Platform/Linux/CreateRedist/Final" directory.     

2. Go into the directory: "Platform/Linux/Redist".  
	Run the script: "sudo ./install.sh" (needs to run as root)   
	The install script copies key files to the following location:   

	Libs into: /usr/lib
	Bins into: /usr/bin
	Includes into: /usr/include/ni
	Config files into: /var/lib/ni



To build the package manually, you can run "make" in the "Platform\Linux\Build" directory.

Install avin2 Kinect driver SensorKinect
===

Get the source: https://github.com/avin2/SensorKinect.git

If you can't find the code online, please check the delivered tarball
SensorKinect.zip

Building Sensor:
---

1. Go into the directory: "Platform/Linux/CreateRedist".  
   Run the script: "./RedistMaker".   
   This will compile everything and create a redist package in the "Platform/Linux/Redist" directory.   
   It will also create a distribution in the "Platform/Linux/CreateRedist/Final" directory.

2. Go into the directory: "Platform/Linux/Redist".   
   Run the script: "sudo ./install.sh" (needs to run as root)   
   The install script copies key files to the following location:   

	Libs into: /usr/lib
	Bins into: /usr/bin
	Config files into: /usr/etc/primesense
	USB rules into: /etc/udev/rules.d
	Logs will be created in: /var/log/primesense



To build the package manually, you can run "make" in the "Platform\Linux\Build" directory.

Install Qt and PyQt
===

If you are using some kind of  package manager like zypper in OpenSUSE or pip for python, you can install PyQt5 module for Python easily by doing:

pip install PyQt5

Or you can build from source.

Install PyOpenNI and NiTE
===

Get the source: git clone  https://github.com/jmendeth/PyOpenNI.git

Build the source:

i.     In the work directory where the source is, mkdir

ii.     cmake ../##

iii.      

e.     Install NiTE



NiTE is not an open source project. It is provided to do some higher level programming with computer vision algorithms inside it. And it can cooperate with OpenNI perfectly.

We provide the tarball delivery for the code, please check nite.zip


