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
light = rospy.Publisher('/mobile_base/commands/led1', Led, queue_size=10)
light2 = rospy.Publisher('/mobile_base/commands/led2', Led, queue_size=10)
noise = rospy.Publisher('/mobile_base/commands/sound', Sound, queue_size=10)

def symbolCallback(data):
	symbol = data.data
	time_stop = time.time() + 5
	time_move = time.time()
	if (symbol == 'spin') :
		print("spin!")
		noise.publish(3)	
		light.publish(1)
		light2.publish(1)	
		move_cmd.linear.x = 0
		move_cmd.angular.z = -1
		time_move = time.time() + 8
		while(time.time() < time_move):
			move.publish(move_cmd)
		noise.publish(3)
		light.publish(0)
		light2.publish(0)
	elif (symbol == 'H') :
		print("Halt!")
		noise.publish(3)
		light.publish(2)
		light2.publish(2)
		move_cmd.linear.x = 0
		move_cmd.angular.z = 0
		time_move = time.time() + 3
		while(time.time() < time_move):
			move.publish(move_cmd)
		noise.publish(3)
		light.publish(0)
		light2.publish(0)
	elif (symbol == 'C') :
		print("Charge!")		
		move_cmd.linear.x = 0.8
		move_cmd.angular.z = 0
		noise.publish(2)		
		light.publish(1)
		light2.publish(1)
		time_move = time.time() + 3
		while(time.time() < time_move):
			move.publish(move_cmd)
		noise.publish(2)
		light.publish(0)
		light2.publish(0)
	elif (symbol == 'moon') :
		print("dance!")		
		noise.publish(5)
		light.publish(1)
		light2.publish(3)		
		time_move = time.time() + 3
		move_cmd.linear.x = 0.2
		move_cmd.linear.z = -0.5
		while(time.time() < time_move):
			move.publish(move_cmd)
		move_cmd.linear.x = -0.2
		move_cmd.linear.z = 0.5
		#move_cmd.angular.z = 0.5
		
		while(time.time() < time_move):
			move.publish(move_cmd)
		time_move = time.time() + 3
		light.publish(2)
		light2.publish(1)
		move_cmd.linear.x = 0
		move_cmd.angular.z = -1
		light.publish(3)
		light2.publish(2)
		while(time.time() < time_move):
			move.publish(move_cmd)
		light.publish(1)
		light2.publish(3)
		move_cmd.linear.x = 0.2
		#move_cmd.linear.y = -0.2
		move_cmd.angular.z = -0.5
		while(time.time() < time_move):
			move.publish(move_cmd)		
		light.publish(2)
		light2.publish(1)
		move_cmd.linear.x = 0
		move_cmd.angular.z = 1
		while(time.time() < time_move):
			move.publish(move_cmd)
		light.publish(3)
		light2.publish(2)
		move_cmd.linear.x = -0.2
		move_cmd.linear.z = 0.5
		while(time.time() < time_move):
			move.publish(move_cmd)
		time_move = time.time() + 2
		move_cmd.angular.z = -1.5
		light.publish(1)
		light2.publish(3)
		while(time.time() < time_move):
			move.publish(move_cmd)
		light.publish(0)
		light2.publish(0)
		noise.publish(6)
	elif (symbol == 'A') :
		print("Avoid!")
		move_cmd.linear.x = -0.3
		move_cmd.angular.z = 0
		noise.publish(4)
		light.publish(3)
		time_move = time.time() + 3
		while(time.time() < time_move):
			move.publish(move_cmd)
		noise.publish(4)
		light.publish(0)
	elif (symbol == 'bolt') :
		print("bolt!")	
		noise.publish(3)
		noise.publish(3)
		light.publish(2)	
		move_cmd.linear.x = 0.3
		move_cmd.angular.z = 0
		noise.publish(3)
		light.publish(2)

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
#moved light and noise
move = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
rospy.Subscriber("symbols",String,symbolCallback)
#rospy.Subscriber("faces",Int32)


move_cmd = Twist ( )

light.publish(Led.GREEN)
rospy.on_shutdown(shutdown)
rospy.spin()

#goforward()

