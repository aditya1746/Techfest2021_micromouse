#! /usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist, Point
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion
from tf import transformations
import math
import time

dist_l,dist_r,dist_c = 0,0,0
x,y,i,j,orientation,state = 0,0,0,0,-1,0
dirn = "none"
visited = [[0 for i in range(16)] for j in range(16)]
path = []
position_ = Point()
pub = 0
yaw_ = 0
th = 0.15
th_yaw = 0.0125
forward_dist = 0.17

def forward():
    #print("---------------- inside forward -------------------")

    global pub,i,j
    x1,y1 = x,y

    v = Twist()
    v.linear.x = 0.16
    v.linear.y,v.linear.z  = 0.0,0.0
    v.angular.z,v.angular.x,v.angular.y = 0.0,0.0,0.0
    
    yaw1 = yaw_
    while True:

        if(abs(x-x1)>=forward_dist or abs(y-y1)>=forward_dist):
            break
        
        pub.publish(v)

    v.linear.y,v.linear.x,v.linear.z = 0.0,0.0,0.0
    pub.publish(v)
    yaw2 = yaw_

    if(orientation==0):
        i = i+1
    elif(orientation==1):
        i = i-1
    elif(orientation==2):
        j = j+1
    elif(orientation==3):
        j = j-1

    '''print("xinital: ",x1," xfinal: ",x, " yinitial: ",y1, " yfinal: ",y, " err: ",abs(y-y1)-0.16, " erryaw: ",yaw_-yaw1)
    print("======================================================================")'''


def rotate(A, clockwise):

    #print("---------------- inside rotate -------------------")

    global pub

    v = Twist()
    #angular_speed = math.radians(abs(angular_speed_degree))
    angular_speed = math.pi/6

    if (clockwise):
        v.angular.z = -abs(angular_speed)
    else:
        v.angular.z = abs(angular_speed)

    v.linear.x,v.linear.y,v.linear.z = 0.0,0.0,0.0

    x1,y1 = x,y

    yaw1 = yaw_

    while(abs(yaw_-yaw1) < A):
        pub.publish(v)

    v.angular.z = 0
    pub.publish(v)

    x2,y2 = x,y
    
    print("reached ====================== yawinitial: ", math.degrees(yaw1)," yawfinal: ",math.degrees(yaw_), " err: ",abs(yaw1-yaw_)-A, " errx: ",x-x1," erry: ",y-y1)
    

def backward():

    global orientation,pub,i,j

    rotate(math.pi,True)

    if(orientation==0):
        orientation=1
    elif(orientation==1):
        orientation=0
    elif(orientation==2):
        orientation=3
    elif(orientation==3):
        orientation=2

    forward()

def left():

    global orientation,pub,i,j

    rotate(math.pi/2 - th_yaw,False)

    if(orientation==0): 
        orientation=2
    elif(orientation==1): 
        orientation=3
    elif(orientation==2): 
        orientation=1
    elif(orientation==3): 
        orientation=0
    
    forward()

def right():

    global orientation,pub,i,j

    rotate(math.pi/2 - th_yaw,True)

    if(orientation==0): 
        orientation=3
    elif(orientation==1):
        orientation=2
    elif(orientation==2):
        orientation=0
    elif(orientation==3):
        orientation=1

    forward()

def backtrack():

    global path,orientation,pub
    path.pop()

    previ,prevj = path[-1]/16,path[-1]%16

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

    global dirn,visited,orientation,i,j

    #print("---------------- inside decideDirection -------------------------")

    if(j<=7 and i<=7): # priority right-down-top-left  // 2nd quadrant 

        if(orientation==0):
        
            if(dist_l>th and visited[i][j+1]==0): 
                dirn = "left"
            elif(dist_c>th and visited[i+1][j]==0): 
                dirn = "front"
            elif(dist_r>th and visited[i][j-1]==0): 
                dirn = "right"
            else: 
                backtrack()
        
        elif(orientation==1):
        
            if(dist_r>th and visited[i][j+1]==0): 
                dirn = "right"
            elif(dist_c>th and visited[i-1][j]==0): 
                dirn = "front"
            elif(dist_l>th and visited[i][j-1]==0): 
                dirn = "left"
            else:
                backtrack()
        
        elif(orientation==2):
        
            if(dist_c>th and visited[i][j+1]==0): 
                dirn = "front"
            elif(dist_r>th and visited[i+1][j]==0): 
                dirn = "right"
            elif(dist_l>th and visited[i-1][j]==0): 
                dirn = "left"            
            else: 
                backtrack()
        
        elif(orientation==3):
        
            if(dist_l>th and visited[i+1][j]==0): 
                dirn = "left"            
            elif(dist_r>th and visited[i-1][j]==0): 
                dirn = "right"
            elif(dist_c>th and visited[i][j-1]==0): 
                dirn = "front"            
            else: 
                backtrack()
        
    elif(j>=8 and i<=7): #// priority left-down-top-right  // 1st quadrant

        if(orientation==0):
    
            if(dist_r>th and visited[i][j-1]==0): 
                dirn = "right"            
            elif(dist_c>th and visited[i+1][j]==0): 
                dirn = "front"
            elif(dist_l>th and visited[i][j+1]==0): 
                dirn = "left"
            else:
                backtrack()
        
        elif(orientation==1):
        
            if(dist_l>th and visited[i][j-1]==0): 
                dirn = "left"
            elif(dist_c>th and visited[i-1][j]==0): 
                dirn = "front"
            elif(dist_r>th and visited[i][j+1]==0): 
                dirn = "right"
            else:
                backtrack()
        
        elif(orientation==2):
        
            if(dist_r>th and visited[i+1][j]==0): 
                dirn = "right"            
            elif(dist_l>th and visited[i-1][j]==0): 
                dirn = "left"
            elif(dist_c>th and visited[i][j+1]==0): 
                dirn = "front"            
            else:
                backtrack()
        
        elif(orientation==3):
        
            if(dist_c>th and visited[i][j-1]==0): 
                dirn = "front"
            elif(dist_l>th and visited[i+1][j]==0): 
                dirn = "left"
            elif(dist_r>th and visited[i-1][j]==0): 
                dirn = "right"            
            else:
                backtrack()
        
    elif(j<=7 and i>=8): #// priority right-top-down-left  // 3rd quadrant
    
        if(orientation==0):
        
            if(dist_l>th and visited[i][j+1]==0): 
                dirn = "left"
            elif(dist_c>th and visited[i+1][j]==0): 
                dirn = "front"
            elif(dist_r>th and visited[i][j-1]==0): 
                dirn = "right"            
            else:
                backtrack()
        
        elif(orientation==1):
        
            if(dist_r>th and visited[i][j+1]==0): 
                dirn = "right"            
            elif(dist_c>th and visited[i-1][j]==0): 
                dirn = "front"
            elif(dist_l>th and visited[i][j-1]==0): 
                dirn = "left"            
            else:
                backtrack()
        
        elif(orientation==2):
        
            if(dist_c>th and visited[i][j+1]==0): 
                dirn = "front"            
            elif(dist_l>th and visited[i-1][j]==0): 
                dirn = "left"
            elif(dist_r>th and visited[i+1][j]==0): 
                dirn = "right"            
            else:
                backtrack()
        
        elif(orientation==3):
        
            if(dist_r>th and visited[i-1][j]==0): 
                dirn = "right"            
            elif(dist_l>th and visited[i+1][j]==0): 
                dirn = "left"
            elif(dist_c>th and visited[i][j-1]==0): 
                dirn = "front"            
            else:
                backtrack()
        
    elif(j>=8 and i>=8): #// priority left-top-down-right  // 4th quadrant 
    
        if(orientation==0):
        
            if(dist_r>th and visited[i][j-1]==0): 
                dirn = "right"            
            elif(dist_c>th and visited[i+1][j]==0): 
                dirn = "front"
            elif(dist_l>th and visited[i][j+1]==0): 
                dirn = "left"            
            else:
                backtrack()
        
        elif(orientation==1):
        
            if(dist_l>th and visited[i][j-1]==0): 
                dirn = "left"            
            elif(dist_c>th and visited[i-1][j]==0): 
                dirn = "front"
            elif(dist_r>th and visited[i][j+1]==0): 
                dirn = "right"            
            else:
                backtrack()
        
        elif(orientation==2):
        
            if(dist_l>th and visited[i-1][j]==0): 
                dirn = "left"            
            elif(dist_r>th and visited[i+1][j]==0): 
                dirn = "right"
            elif(dist_c>th and visited[i][j+1]==0): 
                dirn = "front"            
            else:
                backtrack()
        
        elif(orientation==3):
        
            if(dist_c>th and visited[i][j-1]==0): 
                dirn = "front"            
            elif(dist_r>th and visited[i-1][j]==0): 
                dirn = "right"
            elif(dist_l>th and visited[i+1][j]==0): 
                dirn = "left"            
            else:
                backtrack()

def clbk_laser(msg):

    global dist_l, dist_c, dist_r

    #print( "---------------- inside callback_laser -------------------------")

    regions = [
        round(100*min(min(msg.ranges[0:71]), 100)),
        round(100*min(min(msg.ranges[72:143]), 100)),
        round(100*min(min(msg.ranges[144:215]), 100)),
        round(100*min(min(msg.ranges[216:287]), 100)),
        round(100*min(min(msg.ranges[288:359]), 100)),
    ]

    #print("l:  \t c:  \t r: ".format(regions[4], regions[2], regions[0]))
    dist_l,dist_c,dist_r = msg.ranges[359],msg.ranges[180],msg.ranges[0]
    
    #dist_l,dist_c,dist_r = regions[4]/100,regions[2]/100,regions[0]/100

def clbk_odo(msg):

    global x,y,i,j,state,position_,yaw_

    position_ = msg.pose.pose.position
    x,y = position_.x,position_.y
    state = 1

    quaternion = (msg.pose.pose.orientation.x,msg.pose.pose.orientation.y,msg.pose.pose.orientation.z,msg.pose.pose.orientation.w)

    euler = transformations.euler_from_quaternion(quaternion)
    yaw_ = euler[2]


def setOrientation():
    
    global x,y,i,j,orientation

    '''print("----------------- inside setOrientation -------------------")
    print("x: ",x," y: ",y)
    print("---------------------------------------------------------------")'''

    if(x>0 and y>0):   # 1st quad

        forward()
        x1,y1 = x,y
        i,j = 0,15

        if(x1 == x-1): 
            orientation = 3 #//left facing
            j = j-1
        else:
            orientation = 0
            i = i+1
    
    elif(x<0 and y>0):   #2nd quad

        forward()
        x1,y1 = x,y
        i,j = 0,0

        if(x1 == x+1):
            orientation = 2   #right facing
            j = j+1
        else:
            orientation = 0
            i = i+1

    elif(x<0 and y<0):    # 3rd quad
    
        forward()
        x1,y1 = x,y
        i,j = 15,0

        if(x1 == x+1): 
            orientation = 2    #right facing
            j = j+1
        else:
            orientation = 1
            i = i-1
    
    elif(x>0 and y<0):            #4th quad
    
        forward()
        x1,y1 = x,y
        i,j = 15,15

        if(x1 == x-1):
            orientation=3       #left facing
            j = j-1
        else: 
            orientation = 1
            i = i-1

def main():

    global pub,x,y,i,j,state,visited,path

    rospy.init_node('final_runner', anonymous=True)
    sub_laser = rospy.Subscriber('/my_mm_robot/laser/scan', LaserScan, clbk_laser)
    sub_odom = rospy.Subscriber('/odom', Odometry, clbk_odo)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    rate = rospy.Rate(0.5)

    while(state==0):
        rate.sleep()

    setOrientation()

    visited[i][j] = 1

    if(i>7 and j>7):
        visited[15][15] = 1
        path.append(15*16 + 15)
    elif(i<=7 and j<=7):
        visited[0][0] = 1
        path.append(0)
    elif(i<=7 and j>7):
        visited[0][15] = 1
        path.append(0*16 + 15)
    elif(i>7 and j<=7):
        visited[15][0] = 1
        path.append(15*16 + 0)
        
    while not rospy.is_shutdown():

        #print("----------------- inside not rospy.is_shutdown() -------------------")

        if(visited[i][j] == 0):
            path.append(i*16 + j)

        visited[i][j] = 1

        if((i==7 or i==8) and (j==7 or j==8)):
            break

        decideDirection()

        print("i: ",i," j: ",j," orientation: ",orientation," dirn: ",dirn)
        print("dist_l: ",dist_l,"dist_c: ",dist_c,"dist_r: ",dist_r)

        if(dirn=="left"):
            left()
        elif(dirn=="right"):
            right()
        elif(dirn=="front"):
            forward()

        rate.sleep()
    
    idx = len(path)-1

    print("--------------- going back to start by using shortest path ------------------")

    while(idx>=0):

        previ,prevj = path[idx]/16, path[idx]%16

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

        idx = idx-1

    idx = 0

    print("--------------- going back to end by using shortest path ------------------")

    while(idx<len(path)):

        previ,prevj = path[idx]/16, path[idx]%16

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

        idx = idx+1

if __name__ == '__main__':

    main()
