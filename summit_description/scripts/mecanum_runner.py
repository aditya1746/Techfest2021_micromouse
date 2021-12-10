#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist, Point
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion
from tf import transformations
import math
import time

dist_l,dist_r,dist_f,dist_b = 0.0,0.0,0.0,0.0
x,y,i,j,state = 0,0,0,0,0
dirn = "none"
visited = [[0 for i in range(16)] for j in range(16)]
path = []
pub = 0
unitDistance = 0.178
th = 0.15
n1 = 0
n2 = 0

def front():
    #print("---------------- inside front -------------------")

    global pub,i

    v = Twist()
    v.linear.x = unitDistance
    v.linear.y,v.linear.z  = 0.0,0.0
    v.angular.z,v.angular.x,v.angular.y = 0.0,0.0,0.0

    y1 = y

    i = i+1
    '''
    while (y1-y <= unitDistance):
        print("y1: ",y1," y: ",y)
        pub.publish(v)
        '''
    t = rospy.get_time()

    while(rospy.get_time()<=t+1.0):
        pub.publish(v)

    v.linear.x = 0.0
    pub.publish(v)

    v.linear.y,v.linear.x,v.linear.z = 0.0,0.0,0.0
    pub.publish(v)

def back():

    global pub,i

    #print("---------------- inside back -------------------------")

    v = Twist()
    v.linear.x = -unitDistance
    v.linear.y,v.linear.z  = 0.0,0.0
    v.angular.z,v.angular.x,v.angular.y = 0.0,0.0,0.0

    y1 = y
    '''
    while (y-y1 <= unitDistance):
        pub.publish(v)'''
    t = rospy.get_time()

    while(rospy.get_time()<=t+1.0):
        pub.publish(v)

    v.linear.y,v.linear.x,v.linear.z = 0.0,0.0,0.0
    pub.publish(v)

    i = i-1

def left():

    global pub,j

    #print("---------------- inside left -------------------------")

    v = Twist()
    v.linear.y = -unitDistance
    v.linear.x,v.linear.z  = 0.0,0.0
    v.angular.z,v.angular.x,v.angular.y = 0.0,0.0,0.0

    x1 = x

    '''while (x1-x <= unitDistance):
        pub.publish(v)'''
    t = rospy.get_time()

    while(rospy.get_time()<=t+1.0):
        pub.publish(v)

    v.linear.y,v.linear.x,v.linear.z = 0.0,0.0,0.0
    pub.publish(v)

    j = j-1

def right():

    global pub,j

    #print("---------------- inside right -------------------------")

    v = Twist()
    v.linear.y = unitDistance
    v.linear.x,v.linear.z  = 0.0,0.0
    v.angular.z,v.angular.x,v.angular.y = 0.0,0.0,0.0

    x1 = x
    '''
    while (x-x1 <= unitDistance):
        pub.publish(v)'''
    
    t = rospy.get_time()

    while(rospy.get_time()<=t+1.0):
        pub.publish(v)

    v.linear.y,v.linear.x,v.linear.z = 0.0,0.0,0.0
    pub.publish(v)

    j = j+1

def backtrack():

    global path,orientation,pub
    path.pop()

    previ,prevj = path[-1]/16,path[-1]%16

    if(previ == i+1):
        print("from backtrack going front")
        front()
    elif(previ == i-1):
        print("from backtrack going back")
        back()
    elif(prevj == j+1):
        print("from backtrack going right")
        right()
    elif(prevj == j-1):
        print("from backtrack going left")
        left()
    
def decideDirection():

    global dirn,visited,orientation,i,j

    print("---------------- inside decideDirection -------------------------")

    if(j<=7 and i<=7): # priority right-down-top-left  // 2nd quadrant

        if(dist_r>=th and visited[i][j+1]==0):
            dirn = "right"
        elif(dist_f>=th and visited[i+1][j]==0):
            dirn = "front"
        elif(dist_b>=th and visited[i-1][j]==0):
            dirn = "back"
        elif(dist_l>=th and visited[i][j-1]==0):
            dirn = "left"
        else:
            backtrack()
            dirn = "none"
        
    elif(j>=8 and i<=7): #// priority left-down-top-right  // 1st quadrant

        if(dist_l>=th and visited[i][j-1]==0):
            dirn = "left"
        elif(dist_f>=th and visited[i+1][j]==0):
            dirn = "front"
        elif(dist_b>=th and visited[i-1][j]==0):
            dirn = "back"
        elif(dist_r>=th and visited[i][j+1]==0):
            dirn = "right"
        else:
            backtrack()
            dirn = "none"
        
    elif(j<=7 and i>=8): #// priority right-top-down-left  // 3rd quadrant
    
        if(dist_r>=th and visited[i][j+1]==0):
            dirn = "right"
        elif(dist_b>=th and visited[i-1][j]==0):
            dirn = "back"
        elif(dist_f>=th and visited[i+1][j]==0):
            dirn = "front"
        elif(dist_l>=th and visited[i][j-1]==0):
            dirn = "left"
        else:
            backtrack()
            dirn = "none"

    elif(j>=8 and i>=8): #// priority left-top-down-right  // 4th quadrant 
    
        if(dist_l>=th and visited[i][j-1]==0):
            dirn = "left"
        elif(dist_b>=th and visited[i-1][j]==0):
            dirn = "back"
        elif(dist_f>=th and visited[i+1][j]==0):
            dirn = "front"
        elif(dist_r>=th and visited[i][j+1]==0):
            dirn = "right"
        else:
            backtrack()
            dirn = "none"

def clbk_laser(msg):

    global dist_l, dist_f, dist_r, dist_b,n2,state

    #print( "---------------- inside callback_laser -------------------------")

    dist_l,dist_b,dist_f,dist_r = msg.ranges[180],msg.ranges[90],msg.ranges[270],msg.ranges[0]

    if(n2==0):
        state = state+1
        n2 = 1

def clbk_odo(msg):

    global x,y,i,j,state,n1

    position_ = msg.pose.pose.position
    x,y = position_.x,position_.y

    #print( " ============== inside odom  ===============")
    #print("x: ",x," y: ",y)

    if(n1==0):
        state = state+1
        n1 = 1

def callback(msg):

    global x,y,n1,state
    x = msg.x
    y = msg.y

    if(n1==0):
        state = state+1
        n1 = 1

    #print("====== received =========")

def findij():

    global i,j

    #print(" ============ inside find =================")

    if(x>0 and y>0):
        i,j = 0,15
    elif(x<0 and y>0):
        i,j = 0,0
    elif(x<0 and y<0):
        i,j = 15,0
    elif(x>0 and y<0):
        i,j = 15,15
    
def main():

    global pub,x,y,i,j,state,visited,path

    rospy.init_node('final_runner', anonymous=True)
    sub_laser = rospy.Subscriber('/my_mm_robot/laser/scan', LaserScan, clbk_laser)
    #sub_odom = rospy.Subscriber('/odom', Odometry, clbk_odo)
    sub = rospy.Subscriber('/my_topic',Point,callback)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    rate = rospy.Rate(0.5)

    v = Twist()
    v.linear.x,v.linear.y,v.linear.z,v.angular.x,v.angular.y,v.angular.z = 0.0,0.0,0.0,0.0,0.0,0.0

    while(state!=2):
        state = state
        print("============ waiting =====================")

    print("========== started ======")

    findij()

    #print("i: ",i," j: ",j," dist_l: ",dist_l," dist_f: ",dist_f," dist_r: ",dist_r," dist_b: ",dist_b)
        
    while not rospy.is_shutdown():

        #print("----------------- inside not rospy.is_shutdown() -------------------")

        if(visited[i][j] == 0):
            path.append(i*16 + j)
            #print(path)

        visited[i][j] = 1

        print("I am at: ",i, " ", j)

        if((i==7 or i==8) and (j==7 or j==8)):
            break

        decideDirection()

        print("i am going ", dirn)

        if(dirn=="left"):
            left()
        elif(dirn=="right"):
            right()
        elif(dirn=="front"):
            front()
        elif(dirn=="back"):
            back()

        #prin(" ")

        #rate.sleep()
    
    idx = len(path and visited[i][j]==0)-1

    print("--------------- going back to start by using shortest path and visited[i][j]==0 ------------------")

    while(idx>=0):

        previ,prevj = path[idx]/16, path[idx]%16

        if(previ == i+1):
            front()
        elif(previ == i-1):
            back()
        elif(prevj == j+1):
            right()
        elif(prevj == j-1):
            left()

        idx = idx-1

    idx = 0

    print("--------------- going back to end by using shortest path and visited[i][j]==0 ------------------")

    while(idx<len(path and visited[i][j]==0)):

        previ,prevj = path[idx]/16, path[idx]%16

        if(previ == i+1):
            front()
        elif(previ == i-1):
            back()
        elif(prevj == j+1):
            right()
        elif(prevj == j-1):
            left()
        
        idx = idx+1

if __name__ == '__main__':

    main()
