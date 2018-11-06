# Fall-2018-ECE-478-578-Robotics1-TurtleBot
Intelligent Robotics Lab

Portland State University

Project Name:TurtleBot

Project Description:


Project Status:

Project Goals:
Programming one of the robotics lab’s turtlebots for our project. <br /> The robot was expected to be able to have basic directional movements, simple gestural movements, and vision capabilities such as facial detection. 

ex: Build robot base - 10.10.2018 (done)
ex : Face Detection with OpenCv - 20.10.2018 (in progress)
ex: ROS Implementation . .
List of Hardware and Software (Tools, Libraries etc) :
Software:
ex: OpenCv3 - https://opencv.org/opencv-3-3.html
ex: ROS Indigo - http://wiki.ros.org/indigo

Hardware:
Kobuki Turtle Bot Base:
The base is a Turtlebot 2i built upon a Kobuki base which has two motorized wheels for mobility. <br /> It also has several built-in sensors including a bumper along the front half of the robot which alerts the robot of collisions, drop sensors in both wheels to signal changes in terrain, cliff sensors to signal when the robot is about to drop off a ledge, and a gyro sensor for navigation.
These sensors serve as inputs to the Bot and can be intergated together.

Kinect Camera:
Apart from the Kobuki base, the Turtlebot system also includes a 3D camera with built in depth perception mounted to the front of the base. This can be interfaced using premade ROS software to provide vision to the robot. For our purposes, this will be integrated using 

To run the robot, a computer must be connected to it via a USB3 cable. To allow for mobility of the base, a battery is required to run the computer wirelessly. From there another computer can SSH into the computer for remote execution of code

Dynamixel Servos:
HR OS1
The HR-OS1 is a small humanoid robot which utilizes several Dynamic Cell servos as its joints. The upper portion of the HR-OS1 was attached to the Turtlebot due to the Turtlebot having a higher stability than the HR-OS1’s servo legs. The integration of this torso also allows for gestural interactions with the turtlebot system.


Other Notes:
. . Notes . .

Project Team : <br />
Team Member 1 Kanna Lakshmanan <br />
Team Member 2 Jennifer Lara <br />
Team Member 3 Lauren Voepel <br />
Team Member 4 Rahul Marathe
