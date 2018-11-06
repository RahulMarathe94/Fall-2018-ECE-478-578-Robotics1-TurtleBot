import rospy
import time
from dynamixel_msgs.msg import JointState
from std_msgs.msg import Float64
from std_msgs.msg import String
import os

global in_action
in_action = 0

pub1  = rospy.Publisher('/head_controller/command', Float64)
pub2  = rospy.Publisher('/neck_controller/command', Float64)
pub3  = rospy.Publisher('/right_shoulder_controller/command', Float64)
pub4  = rospy.Publisher('/left_shoulder_controller/command', Float64)
pub5  = rospy.Publisher('/left_upper_controller/command', Float64)
pub6  = rospy.Publisher('/left_lower_controller/command', Float64)
pub7  = rospy.Publisher('/left_elbow_controller/command', Float64)
pub8  = rospy.Publisher('/right_upper_controller/command', Float64)
pub9  = rospy.Publisher('/right_lower_controller/command', Float64)
pub10 = rospy.Publisher('/right_elbow_controller/command', Float64)

def motion_play():
    global in_action
    if in_action == 0:
        in_action = 1

        homedir = os.environ['HOME']
        filepath = homedir + "/catkin_ws_new/src/jimmy/motions/" + data.data + ".txt"

        try:
            with open(filepath) as f:
                content = f.readlines()
                # you may also want to remove whitespace characters like `\n` at the end of each line
                content = [x.strip('\n') for x in content]

                print
                "playing " + data.data + " motion"
                for i in range(0, len(content)):
                    joint_positions = content[i].split(",")
                    delay = 5

                    pub1.publish(float(joint_positions[0]))
                    pub2.publish(float(joint_positions[1]))
                    pub3.publish(float(joint_positions[2]))
                    pub4.publish(float(joint_positions[3]))
                    pub5.publish(float(joint_positions[4]))
                    pub6.publish(float(joint_positions[5]))
                    pub7.publish(float(joint_positions[6]))
                    pub8.publish(float(joint_positions[7]))
                    pub9.publish(float(joint_positions[8]))
                    pub10.publish(float(joint_positions[9]))
                    # delay between motions
                    rospy.sleep(float(delay))
                in_action = 0
                print
                "motion is done"
        except:
            in_action = 0
            print
            "motion file doesn't exist"
    else:
        print
        "The robot can't play this motion because it is playing another motion. Wait until the motion is done."



if __name__ == '__main__':
    try:
        rospy.init_node('head_controller', anonymous=True)
        motion_play()

    except rospy.ROSInterruptException:
        pass