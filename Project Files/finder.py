#!/usr/bin/env python

'''
rotates the robot towards a face location provided by the camera

if the robot senses a colision while rotating it backs up
'''


import rospy
import time


from geometry_msgs.msg import Twist
from kobuki_msgs.msg import BumperEvent
from std_msgs.msg import Int32
from kobuki_msgs.msg import Led
from kobuki_msgs.msg import Sound

go = True

def BumperEventCallback(data):
	bumper = "released"
	if ( data.state == BumperEvent.RELEASED ) :
		bumper = "released"
		light.publish(Led.ORANGE)
		
		time.sleep(1)
		move_cmd.linear.x = 0.1
		move_cmd.angular.z = 0
		move.publish(move_cmd)
	else:
		state = "pressed"  
		if ( data.bumper == BumperEvent.LEFT ) :
			bumper = "Left"
			move_cmd.linear.x = -0.2
			move_cmd.angular.z = 0.5
		elif ( data.bumper == BumperEvent.CENTER ) :
			bumper = "Center"
			move_cmd.linear.x = -0.2
			move_cmd.angular.z = 0
		else:
			bumper = "Right"
			move_cmd.linear.x = -0.2
			move_cmd.angular.z = -0.5
# Twist is a datatype for velocity
		#if it was bumped then back up
		rospy.loginfo(bumper)
		light.publish(Led.RED)
		noise.publish(3)
		move.publish(move_cmd)

def faceCallback(data):
	number = data.data
	if (number > 350) :
		move_cmd.linear.x = 0
		move_cmd.angular.z = -0.5
		#print("turning left!")
	elif (number <= 150) :
		move_cmd.linear.x = 0
		move_cmd.angular.z = 0.5
		#print("turning right!")
	else:
		move_cmd.linear.x = 0
		move_cmd.angular.z = 0
		#print("Stationary!")
	print(data)
	print(number)
	move.publish(move_cmd)

def goforward():
	#while(go):
	
	
	r = rospy.Rate(10);

	# let's go forward at 0.2 m/s
        move_cmd.linear.x = 0.2
	# let's turn at 0 radians/s
	move_cmd.angular.z = 0
	move_cmd.linear.x = 0.1

	while not rospy.is_shutdown():
	    # publish the velocity
            move.publish(move_cmd)
	    # wait for 0.1 seconds (10 HZ) and publish again
            r.sleep()

def shutdown():
        # stop turtlebot
        rospy.loginfo("Stop TurtleBot")
	# a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop TurtleBot
        move.publish(Twist())
	# sleep just makes sure TurtleBot receives the stop command prior to shutting down the script
        rospy.sleep(1)


rospy.init_node("test_events")
light = rospy.Publisher('/mobile_base/commands/led1', Led, queue_size=10)
noise = rospy.Publisher('/mobile_base/commands/sound', Sound, queue_size=10)
move = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
rospy.Subscriber("/mobile_base/events/bumper",BumperEvent,BumperEventCallback)
rospy.Subscriber("face_location",Int32,faceCallback)
#rospy.Subscriber("faces",Int32)


move_cmd = Twist ( )

light.publish(Led.GREEN)
rospy.on_shutdown(shutdown)
rospy.spin()

#goforward()

