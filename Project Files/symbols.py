#!/usr/bin/env python

'''
rotates the robot towards a symbol location provided by the camera

if the robot senses a colision while rotating it backs up
'''


import rospy
import time


from geometry_msgs.msg import Twist
from kobuki_msgs.msg import BumperEvent
from std_msgs.msg import String
from kobuki_msgs.msg import Led
from kobuki_msgs.msg import Sound

go = True


def symbolCallback(data):
	symbol = data.data
	time_stop = time.time() + 5
	time_move = time.time()
	if (symbol == 'spin') :
		move_cmd.linear.x = 0
		move_cmd.angular.z = -1
		time_move = time.time() + 8
		while(time.time() < time_move):
			move.publish(move_cmd)
		print("spin!")
	elif (symbol == 'H') :
		move_cmd.linear.x = 0
		move_cmd.angular.z = 0
		print("Halt!")
	elif (symbol == 'C') :
		move_cmd.linear.x = 0.2
		move_cmd.angular.z = 0
		print("Charge!")
		time_move = time.time() + 3
		while(time.time() < time_move):
			move.publish(move_cmd)
	elif (symbol == 'moon') :
		time_move = time.time() + 1
		move_cmd.linear.x = 0.2
		move_cmd.angular.z = 0.5
		print("dance!")
		while(time.time() < time_move):
			move.publish(move_cmd)
		time_move = time.time() + 1
		move_cmd.linear.x = -0.2
		move_cmd.angular.z = -0.5
		while(time.time() < time_move):
			move.publish(move_cmd)
		move_cmd.linear.x = 0.1
		move_cmd.angular.z = -0.5
	elif (symbol == 'A') :
		move_cmd.linear.x = -0.2
		move_cmd.angular.z = 0
		print("Avoid!")
		time_move = time.time() + 3
		while(time.time() < time_move):
			move.publish(move_cmd)
	elif (symbol == 'bolt') :
		move_cmd.linear.x = 0.2
		move_cmd.angular.z = 0
		print("bolt!")
	#print(data)
	#print(number)
	
	#while(time.time() < time_stop):
	move.publish(move_cmd)


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
rospy.Subscriber("symbols",String,symbolCallback)
#rospy.Subscriber("faces",Int32)


move_cmd = Twist ( )

light.publish(Led.GREEN)
rospy.on_shutdown(shutdown)
rospy.spin()

#goforward()

