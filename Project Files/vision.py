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
Program for image processing on robot.
Converts camera image to OpenCV format
Detects faces and symbols in image
'''
kernelOpen=numpy.ones((5,5))
kernelClose=numpy.ones((20,20))

global lowerBound, upperBound
lowerBound=numpy.array([33,80,40])
upperBound=numpy.array([102,255,255])

found = (0,0,0,0,0,0)
found = list(found)
names = ("moon", "spin", "C", "bolt", "A", "H")
names = list(names)

#load and mask templates
#crecent shape
moon = cv2.imread('moon.png')
moonHSV = cv2.cvtColor(moon,cv2.COLOR_BGR2HSV)
moonTemplate=cv2.inRange(moonHSV,lowerBound,upperBound)
moonTemplate = cv2.morphologyEx(moonTemplate,cv2.MORPH_OPEN,kernelOpen)
moonTemplate = cv2.morphologyEx(moonTemplate,cv2.MORPH_CLOSE,kernelClose)

#u-turn arrow
spin = cv2.imread('spin.png')
spinHSV = cv2.cvtColor(spin,cv2.COLOR_BGR2HSV)
spinTemplate = cv2.inRange(spinHSV,lowerBound,upperBound)
spinTemplate = cv2.morphologyEx(spinTemplate,cv2.MORPH_OPEN,kernelOpen)
spinTemplate = cv2.morphologyEx(spinTemplate,cv2.MORPH_CLOSE,kernelClose)

#lightning bolt shaped arrow
bolt = cv2.imread('bolt.png')
boltHSV = cv2.cvtColor(bolt,cv2.COLOR_BGR2HSV)
boltTemplate = cv2.inRange(boltHSV,lowerBound,upperBound)
boltTemplate = cv2.morphologyEx(boltTemplate,cv2.MORPH_OPEN,kernelOpen)
boltTemplate = cv2.morphologyEx(boltTemplate,cv2.MORPH_CLOSE,kernelClose)

#A for Anger
anger = cv2.imread('anger.png')
angerHSV = cv2.cvtColor(anger,cv2.COLOR_BGR2HSV)
angerTemplate = cv2.inRange(angerHSV,lowerBound,upperBound)
angerTemplate = cv2.morphologyEx(angerTemplate,cv2.MORPH_OPEN,kernelOpen)
angerTemplate = cv2.morphologyEx(angerTemplate,cv2.MORPH_CLOSE,kernelClose)

#C for cry
cry = cv2.imread('cry.png')
cryHSV = cv2.cvtColor(cry,cv2.COLOR_BGR2HSV)
cryTemplate = cv2.inRange(cryHSV,lowerBound,upperBound)
cryTemplate = cv2.morphologyEx(cryTemplate,cv2.MORPH_OPEN,kernelOpen)
cryTemplate = cv2.morphologyEx(cryTemplate,cv2.MORPH_CLOSE,kernelClose)

#H for happy
happy = cv2.imread('happy.png')
happyHSV = cv2.cvtColor(happy,cv2.COLOR_BGR2HSV)
happyTemplate = cv2.inRange(happyHSV,lowerBound,upperBound)
happyTemplate = cv2.morphologyEx(happyTemplate,cv2.MORPH_OPEN,kernelOpen)
happyTemplate = cv2.morphologyEx(happyTemplate,cv2.MORPH_CLOSE,kernelClose)

#make contour maps of templates
moonIm,moonConts,h=cv2.findContours(moonTemplate.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
spinTemp,spinConts,h=cv2.findContours(spinTemplate.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
boltTemp,boltConts,h=cv2.findContours(boltTemplate.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
angerTemp,angerConts,h=cv2.findContours(angerTemplate.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
cryTemp,cryConts,h=cv2.findContours(cryTemplate.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
happyTemp,happyConts,h=cv2.findContours(happyTemplate.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)


#load the cascade files for face detection
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)



class image_converter:

    def __init__(self):

        self.image_pub = rospy.Publisher("cv_image",Image, queue_size=10)
        self.face_pub = rospy.Publisher("faces",Int32, queue_size=10)
        self.loc_pub = rospy.Publisher("face_location", Int32, queue_size=10)  
        self.symbol_pub = rospy.Publisher("symbols", String, queue_size=10)  
        #self.image_pub = rospy.Publisher("gray_image", Image, queue_size=10)

        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.callback)

    def callback(self,data):
        global found, names
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
        #print("found {0} faces!".format(len(faces)))
        face_num = int(len(faces))
        self.face_pub.publish(face_num)

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(cv_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            self.loc_pub.publish(x)

            #if displayPresent is True:
        #       cv2.imshow("Faces found", cv_image)
        #   if cv2.waitKey(10) == 27:
                # Hit esc
        #       break
        #   else:
        #       pass    # no display

           #convert BGR to HSV
        imgHSV= cv2.cvtColor(cv_image,cv2.COLOR_BGR2HSV)
        
        # create the Mask
        mask=cv2.inRange(imgHSV,lowerBound,upperBound)
        cv2.imshow("mask",mask)
        
        
        #morphology to reduce noice
        maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
        maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)
        maskFinal=maskClose

        
        cv2.imshow("maskFinal",maskFinal)
        
        
        #RETR_EXTERNAL Retrieves only the extreme outer contour
        #CHAIN_APPROX_NONE Translates all the points from the chain code into points.
        img2,conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

        moonCont = moonConts[0]
        spinCont = spinConts[0]
        angerCont = angerConts[0]
        happyCont = happyConts[0]
        boltCont = boltConts[0]
        cryCont = cryConts[0]
        
        
        for i in range(1, len(conts)):
        
            moonFound = cv2.matchShapes(conts[i], moonCont, 1, 0.0)
            spinFound = cv2.matchShapes(conts[i], spinCont, 1, 0.0)
            cryFound = cv2.matchShapes(conts[i], cryCont, 1, 0.0)
            happyFound = cv2.matchShapes(conts[i], happyCont, 1, 0.0)
            angerFound = cv2.matchShapes(conts[i], angerCont, 1, 0.0)
            boltFound = cv2.matchShapes(conts[i], boltCont, 1, 0.0)

            values = (moonFound, spinFound, cryFound, boltFound, angerFound, happyFound)
            ret = min(values)
            #check if item with highest match is at least within 0.1 similarity
            if(ret < 0.1):
                #if yes then increment the occurances for the item with the highest similarity
                smallest = values.index(ret)
                found[smallest] = found [smallest] + 1
                j = 0
                #set all other items to 0 to prevent false detections
                while(j < smallest):
                    found[j] = 0
                    j = j + 1
                j = smallest + 1
                while(j < len(values)):
                    found[j] = 0
                    j = j + 1

                #draw contours around item that looks like it may be a fit
                cnt = conts[i]
                cv2.drawContours(cv_image, [cnt], 0, (0,255,0), 6)
                

        
        #To know we have a match for sure we check if we've seen item 50 times
        #this also prevents the log from being spammed with 500 outputs
        largest = max(found)
        if(largest > 10):
            print("we found: ", names[found.index(largest)])
            self.symbol_pub.publish(names[found.index(largest)])
            found = (0,0,0,0,0,0)
            found = list(found)     
        
        
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
