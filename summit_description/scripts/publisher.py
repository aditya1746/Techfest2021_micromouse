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

def callback(msg):

    global x,y

    position_ = msg.pose.pose.position
    x,y = position_.x,position_.y

    print(" ======= received =============")

def main():

    rospy.init_node('publisher')

    pub = rospy.Publisher('/my_topic',Point,queue_size=1)

    sub = rospy.Subscriber('/odom',Odometry,callback)

    p = Point()
    p.x = x
    p.y = y

    rate = rospy.Rate(100)

    while not rospy.is_shutdown():

        pub.publish(p)

        print("published ",p.x,",",p.y)
        rate.sleep()

if __name__=='__main__':
    main()