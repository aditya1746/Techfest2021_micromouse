#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion
import math

dist_l,dist_r,dist_c = 0,0,0
x,y,i,j = 0,0,0,0:
orientation = -1
dirn = ""
visited = [[0 for i in range(16)] for j in range(16)]
path = []

def forward():

    v = Twist()
    v.linear.x, v.linear.y, v.linear.z = 1,0,0
    pub.publish(v)

def rotate180():

def rotateCW():
    
def rotateCCW():

def backward():

    global orientation

    rotate180()
    forward()

    if(orientation==0):
        orientation=1
    elif(orientation==1):
        orientation=0
    elif(orientation==2):
        orientation=3
    elif(orientation==3):
        orientation=2

def left():

    global orientation

    rotateCCW()
    forward()

    if(orientation==0): 
        orientation=2
    elif(orientation==1): 
        orientation=3
    elif(orientation==2): 
        orientation=1
    elif(orientation==3): 
        orientation=0

def right():

    global orientation

    rotateCW()
    forward()

    if(orientation==0): 
        orientation=3
    elif(orientation==1):
        orientation=2
    elif(orientation==2):
        orientation=0
    elif(orientation==3):
        orientation=1

def backtrack():

    global path
    path.pop()

    previ = path[path.size()-1]/16, prevj = path[path.size()-1]%16

    if(previ == i+1):

        if(orientation==0): 
            forward()
        elif(orientation==1): 
            backward()
        elif(orientation==2): 
            right()
        elif(orientation==3): 
            left()
    
    elif(previ == i-1):
    
        if(orientation==1): 
            forward()
        elif(orientation==0): 
            backward()
        elif(orientation==2): 
            left()
        elif(orientation==3): 
            right()
    
    elif(prevj == j+1):
    
        if(orientation==2): 
            forward()
        elif(orientation==3): 
            backward()
        elif(orientation==1): 
            right()
        elif(orientation==0): 
            left()
    
    elif(prevj == j-1):
    
        if(orientation==3): 
            forward()
        elif(orientation==2): 
            backward()
        elif(orientation==0): 
            right()
        elif(orientation==1): 
            left()
    

def decideDirection():

    if(j<=7 and i<=7): # priority right-down-top-left  // 2nd quadrant 

        if(orientation==0):
        
            if(dist_l>0.15 and visited[i][j+1]==0): 
                dirn = "left"
            elif(dist_c>0.15 and visited[i+1][j]==0): 
                dirn = "front"
            elif(dist_r>0.15 and visited[i][j-1]==0): 
                dirn = "right"
            else: 
                backtrack(path,i,j,o)
        
        elif(orientation==1):
        
            if(dist_l>0.15 and visited[i][j+1]==0): 
                dirn = "left"
            elif(dist_c>0.15 and visited[i+1][j]==0): 
                dirn = "front"
            elif(dist_r>0.15 and visited[i][j-1]==0): 
                dirn = "right"
            else:
                backtrack(path,i,j,o)
        
        elif(orientation==2):
        
            if(dist_l>0.15 and visited[i][j+1]==0): 
                dirn = "left"
            elif(dist_c>0.15 and visited[i+1][j]==0): 
                dirn = "front"
            elif(dist_r>0.15 and visited[i][j-1]==0): 
                dirn = "right"            
            else: 
                backtrack(path,i,j,o)
        
        elif(orientation==3):
        
            if(dist_l>0.15 and visited[i][j+1]==0): 
                dirn = "left"            
            elif(dist_c>0.15 and visited[i+1][j]==0): 
                dirn = "front"
            elif(dist_r>0.15 and visited[i][j-1]==0): 
                dirn = "right"            
            else: 
                backtrack(path,i,j,o)
        
    elif(j>=8 and i<=7): #// priority left-down-top-right  // 1st quadrant

        if(orientation==0):
    
            if(dist_r>0.15 and visited[i][j-1]==0): 
                dirn = "right"            
            elif(dist_c>0.15 and visited[i+1][j]==0): 
                dirn = "front"
            elif(dist_l>0.15 and visited[i][j+1]==0): 
                dirn = "left"
            else:
                backtrack(path,i,j,o)
        
        elif(orientation==1):
        
            if(dist_l>0.15 and visited[i][j-1]==0): 
                dirn = "left"
            elif(dist_c>0.15 and visited[i-1][j]==0): 
                dirn = "front"
            elif(dist_r>0.15 and visited[i][j+1]==0): 
                dirn = "right"
            else:
                backtrack(path,i,j,o)
        
        elif(orientation==2):
        
            if(dist_r>0.15 and visited[i+1][j]==0): 
                dirn = "right"            
            elif(dist_l>0.15 and visited[i-1][j]==0): 
                dirn = "left"
            elif(dist_r>0.15 and visited[i][j+1]==0): 
                dirn = "front"            
            else:
                backtrack(path,i,j,o)
        
        elif(orientation==3):
        
            if(dist_c>0.15 and visited[i][j-1]==0): 
                dirn = "front"
            elif(dist_l>0.15 and visited[i+1][j]==0): 
                dirn = "left"
            elif(dist_r>0.15 and visited[i][j-1]==0): 
                dirn = "right"            
            else:
                backtrack(path,i,j,o)
        
    elif(j<=7 and i>=8): #// priority right-top-down-left  // 3rd quadrant
    
        if(orientation==0):
        
            if(dist_l>0.15 and visited[i][j+1]==0): 
                dirn = "left"
            elif(dist_c>0.15 and visited[i+1][j]==0): 
                dirn = "front"
            elif(dist_r>0.15 and visited[i][j-1]==0): 
                dirn = "right"            
            else:
                backtrack(path,i,j,o)
        
        elif(orientation==1):
        
            if(dist_r>0.15 and visited[i][j+1]==0): 
                dirn = "right"            
            elif(dist_c>0.15 and visited[i-1][j]==0): 
                dirn = "front"
            elif(dist_l>0.15 and visited[i][j-1]==0): 
                dirn = "left"            
            else:
                backtrack(path,i,j,o)
        
        elif(orientation==2):
        
            if(dist_c>0.15 and visited[i][j+1]==0): 
                dirn = "front"            
            elif(dist_l>0.15 and visited[i-1][j]==0): 
                dirn = "left"
            elif(dist_r>0.15 and visited[i+1][j]==0): 
                dirn = "right"            
            else:
                backtrack(path,i,j,o)
        
        elif(orientation==3):
        
            if(dist_r>0.15 and visited[i-1][j]==0): 
                dirn = "right"            
            elif(dist_l>0.15 and visited[i+1][j]==0): 
                dirn = "left"
            elif(dist_c>0.15 and visited[i][j+1]==0): 
                dirn = "front"            
            else:
                backtrack(path,i,j,o)
        
    elif(j>=8 and i>=8): #// priority left-top-down-right  // 4th quadrant 
    
        if(orientation==0)
        
            if(dist_r>0.15 and visited[i][j-1]==0): 
                dirn = "right"            
            elif(dist_c>0.15 and visited[i+1][j]==0): 
                dirn = "front"
            elif(dist_l>0.15 and visited[i][j+1]==0): 
                dirn = "left"            
            elbacktrack(path,i,j,o)
        
        elif(orientation==1):
        
            if(dist_l>0.15 and visited[i][j-1]==0): 
                dirn = "left"            
            elif(dist_c>0.15 and visited[i-1][j]==0): 
                dirn = "front"
            elif(dist_r>0.15 and visited[i][j+1]==0): 
                dirn = "right"            
            else:
                backtrack(path,i,j,o)
        
        elif(orientation==2):
        
            if(dist_l>0.15 and visited[i-1][j]==0): 
                dirn = "left"            
            elif(dist_r>0.15 and visited[i+1][j]==0): 
                dirn = "right"
            elif(dist_c>0.15 and visited[i][j+1]==0): 
                dirn = "front"            
            else:
                backtrack(path,i,j,o)
        
        elif(orientation==3):
        
            if(dist_c>0.15 and visited[i][j-1]==0): 
                dirn = "front"            
            elif(dist_r>0.15 and visited[i-1][j]==0): 
                dirn = "right"
            elif(dist_l>0.15 and visited[i+1][j]==0): 
                dirn = "left"            
            else:
                backtrack(path,i,j,o)

    #else:
    #    dirn = "unknown" #// a number different from 0,1,-1 , 17 => just stay there

def clbk_laser(msg):

    global dist_l, dist_c, dist_r

    regions = [
        round(100*min(min(msg.ranges[0:71]), 100)),
        round(100*min(min(msg.ranges[72:143]), 100)),
        round(100*min(min(msg.ranges[144:215]), 100)),
        round(100*min(min(msg.ranges[216:287]), 100)),
        round(100*min(min(msg.ranges[288:359]), 100)),
    ]

    #rospy.loginfo(regions)
    #print("l: {} \t c: {} \t r: {}".format(regions[4], regions[2], regions[0]))
    
    dist_l = regions[4],dist_c = regions[2],dist_r = regions[0]

def clbk_odo(msg):

    global x,y

    x = msg.x, y = msg.y

    #i = 
    #j = 

def setOrientation():

    global orientation

    if(x>0 and y>0): #//=> 1st quad
    
        forward()

        x1,y1 = x,y

        backward() 
        rotate180()

        if(x1 == x-1): 
            orientation=3 #//left facing
        else:
            orientation = 0
    
    elif(x<0 and y>0): #// 2nd quad
    
        forward(0)

        x1,y1 = x,y

        backward() 
        rotate180()

        if(x1 == x+1):
            orientation = 2 #//right facing
        else:
            orientation = 0

    elif(x<0 and y<0): #// 3rd quad
    
        forward()

        x1,y1 = x,y

        backward() 
        rotate180()

        if(x1 == x+1): 
            orientation = 2 #//right facing
        else:
            orientation = 1
    
    else: #// 4th quad
    
        forward()

        x1,y1 = x,y

        backward() 
        rotate180()

        if(x1 == x-1):
            orientation=3 #//left facing
        else: 
            orientation = 1

def main():

    sub_laser = rospy.Subscriber('/my_mm_robot/laser/scan', LaserScan, clbk_laser)
    sub_odom = rospy.Subscriber('/odom', Quaternion, clbk_odo)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

    setOrientation()

    while(True):

        visited[i][j] = 1

        path.append(i*16 + j)

        if((i==7 or i==8) and (j==7 or j==8)):
            break

if __name__ == '__main__':
    main()