#! /usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist, Point
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion
from tf import transformations
import math
import time

x,y = -1.35,1.35
pub = 0

n = 0
i = 0

def front():
    print("---------------- inside front -------------------")

    global pub,i

    v = Twist()
    v.linear.x = 0.16
    v.linear.y,v.linear.z  = 0.0,0.0
    v.angular.z,v.angular.x,v.angular.y = 0.0,0.0,0.0

    y1 = y

    i = i+1

    while (y1-y <= 0.165):
        print("y1: ",y1," y: ",y)
        pub.publish(v)

    v.linear.y,v.linear.x,v.linear.z = 0.0,0.0,0.0
    pub.publish(v)

def callback(msg):

    global x,y,n
    x = msg.x
    y = msg.y

    if(n==0):
        n = 1

def main():

    rospy.init_node('subscriber')

    global pub

    pub = rospy.Publisher('/cmd_vel',Twist,queue_size=1)

    sub = rospy.Subscriber('/my_topic',Point,callback)

    while(n==0):
        print(" ======== waiting ============")
    
    front()

if __name__=='__main__':
    main()
