#! /usr/bin/python
#Filename : KinectSensor.py
# Provide a kinect sensor module

from openni import *
import openni

post_to_use=''
ctx = openni.Context()
ctx.init()
depthNode=''
imageNode=''
userNode=''
skel_cap=''
pose_cap=''
initialized=False

def deviceAvailable():
	global ctx
	try:
		depth = openni.DepthGenerator()
		depth.create(ctx)
	except OpenNIError:
		return False
	return True
def reInit():
	global initialized
	ctx.shutdown()
	ctx.init()
	initialized=False
#declare callback function
def register_new_user(src,id):
	print "Step 1: User(id = {}) has been detected. Look for pose...".format(id)
	pose_cap.start_detection(pose_to_use, id)

def lost_user(src, id):
	print "User (id = {}) has been lost" .format(id)

def pose_detected(src, pose, id):
	print "Step 2: Detected pose {} in user {}.Request calibration"\
	.format(pose, id)
	pose_cap.stop_detection(id)
	skel_cap.request_calibration(id, True)

def calibration_start(src, id):
	print "Step 3: User(id = {}) calibration started" .format(id)

def calibration_complete(src, id, status):
	if status == CALIBRATION_STATUS_OK:
		print "Step 4: User (id = {}) calibrated successfully! Start to track" \
		.format(id)
		skel_cap.start_tracking(id)
	else:
		print "ERROR! User (id={}) failed to calibrate. Restarting process"\
		.format(id)
		register_new_user(userNode, id)



#def deviceAvaiable():
#	try:
#		depth = DepthGenerator()
#		depth.create(ctx)
#	except OpenNIError:
#		return False
#	return True
#
def startAll():
	global initialized
	if initialized!=True:
		init();
		initialized=True
	ctx.start_generating_all()
	print "start generating all"

def readDepth():
	#depthNode.wait_and_update_data()
	return depthNode.get_raw_depth_map_8()

def readImage():
	#imageNode.wait_and_update_data()
	return imageNode.get_synced_image_map_bgr()

def isTracking(id):
	print "tracking type",type(id)
	return skel_cap.is_tracking(id)

def readSkeleton(request_list, id):
	#userNode.wait_and_update_data()
	joint_list = []
	pro_joint_list = []
	for s in request_list:
		if s == 'head':
			req_joint = SKEL_HEAD 
		elif s == 'torso':
			req_joint = SKEL_TORSO
		elif s == 'right_hand':
			req_joint = SKEL_RIGHT_HAND
		elif s == 'right_elbow':
			req_joint = SKEL_RIGHT_ELBOW
		elif s == 'right_shoulder':
			req_joint = SKEL_RIGHT_SHOULDER
		elif s == 'left_hand':
			req_joint = SKEL_LEFT_HAND
		elif s == 'left_elbow':
			req_joint = SKEL_LEFT_ELBOW
		elif s == 'left_shoulder':
			req_joint = SKEL_LEFT_SHOULDER
		elif s == 'neck':
			req_joint = SKEL_NECK
		else:
			print "Not support",s
			continue
		if skel_cap.is_tracking(id):
			joint_info = skel_cap.get_joint_position(id, req_joint)
			joint_list.append(joint_info.point)
		else:
			pass
		#print "Not tracking now"
		pro_joint_list = depthNode.to_projective(joint_list)

	return pro_joint_list,joint_list

#ctx.start_generating_all()
#print "0"
#while True:
#	ctx.wait_and_update_all()
#	for id in userNode.users:
#		print id


def init():
	global pose_to_use
	pose_to_use='Psi'
	global ctx
	
	#set up all used Generator
	global depthNode, imageNode, userNode
	depthNode = openni.DepthGenerator()
	imageNode = openni.ImageGenerator()
	userNode  = openni.UserGenerator()
	userNode.create(ctx)
	depthNode.create(ctx)
	imageNode.create(ctx)
	
	#extract pose_capalibity and skeleton_capability
	global skel_cap, pose_cap
	skel_cap = userNode.skeleton_cap
	pose_cap = userNode.pose_detection_cap
	
	#register call back
	userNode.register_user_cb(register_new_user, lost_user)
	pose_cap.register_pose_detected_cb(pose_detected)
	skel_cap.register_c_start_cb(calibration_start)
	skel_cap.register_c_complete_cb(calibration_complete)
	skel_cap.set_profile(SKEL_PROFILE_ALL)
	
