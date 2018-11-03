#!/usr/bin/env python
from __future__ import print_function

import roslib
#roslib.load_manifest('my_package')
import sys
import rospy
import numpy
import cv2
from std_msgs.msg import String
from std_msgs.msg import Int32
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

'''
Converts camera feed to OpenCV format, performs face detection then outputs number of faces and face location to 
Rostopics "faces" and "face_location"
'''
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

class image_converter:
	
	def __init__(self):
		self.image_pub = rospy.Publisher("cv_image",Image, queue_size=10)
		self.face_pub = rospy.Publisher("faces",Int32, queue_size=10)
		self.loc_pub = rospy.Publisher("face_location", Int32, queue_size=10)  
		#self.image_pub = rospy.Publisher("gray_image", Image, queue_size=10)

		self.bridge = CvBridge()
		self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.callback)

	def callback(self,data):
		try:
			cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
		except CvBridgeError as e:
			print(e)

		(rows,cols,channels) = cv_image.shape
		
		gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
		#cv2.imshow("gray window", gray)
		faces = faceCascade.detectMultiScale(
			gray, scaleFactor=1.1,
			minNeighbors=5,
			minSize=(30,30)
			#flags = cv2.CV_HAAR_SCALE_IMAGE
			)
		print("found {0} faces!".format(len(faces)))
		face_num = int(len(faces))
		self.face_pub.publish(face_num)

		# Draw a rectangle around the faces
		for (x, y, w, h) in faces:
			cv2.rectangle(cv_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
			self.loc_pub.publish(x)

			#if displayPresent is True:
		#		cv2.imshow("Faces found", cv_image)
		#	if cv2.waitKey(10) == 27:
				# Hit esc
		#		break
		#	else:
		#		pass    # no display
		cv2.waitKey(3)
		cv2.imshow("Image window", cv_image)
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
