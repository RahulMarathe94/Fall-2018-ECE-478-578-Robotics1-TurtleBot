#!/usr/bin/env python
from __future__ import print_function

import roslib
#roslib.load_manifest('my_package')
import sys
import rospy
import numpy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

#Converts Image from ROS to OpenCV 
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

class face_detect:
	
	def __init__(self):
		self.pub = rospy.Publisher("faces",int, queue_size=10)
		
		self.image_sub = rospy.Subscriber("cv_image",Image,self.callback)

	def callback(self,data):
		try:
			cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
		except CvBridgeError as e:
			print(e)

		(rows,cols,channels) = cv_image.shape
		#if cols > 60 and rows > 60 :
			#cv2.circle(cv_image, (50,50), 10, 255)
		gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
		faces = faceCascade.detectMultiScale(
			gray, scaleFactor=1.1,
			minNeighbors=5,
			minSize=(30,30)
			#flags = cv2.CV_HAAR_SCALE_IMAGE
			)
		print("found {0} faces!".format(len(faces)))
		self.pub.publish
		# Draw a rectangle around the faces
		for (x, y, w, h) in faces:
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

			if displayPresent is True:
				cv2.imshow("Faces found", frame)
			if cv2.waitKey(10) == 27:
				# Hit esc
				break
			else:
				pass    # no display

		cv2.imshow("gray window", gray)
		#faces = faceCascade.detectMultiScale(
		#	gray, scaleFactor=1.1,
		#	minNeighbors=5,
		#	minSize=(30,30)
			#flags = cv2.CV_HAAR_SCALE_IMAGE
		#	)
		#print("found {0} faces!".format(len(faces)))
		cv2.waitKey(3)

		try:
			self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
		except CvBridgeError as e:
			print(e)

def main(args):
	ic = image_converter()
	rospy.init_node('image_converter', anonymous=True)
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting down")
	cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
