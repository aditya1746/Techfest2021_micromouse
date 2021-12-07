#! /usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist, Point
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion
import math
import time

dist_l,dist_r,dist_c = 0,0,0
x,y,i,j,orientation,state = 0,0,0,0,-1,0
dirn = "none"
visited = [[0 for i in range(16)] for j in range(16)]
path = []
position_ = Point()
pub = 0

def forward():

    global pub

    print("---------------- inside forward -------------------")

    v = Twist()
    v.linear.x, v.linear.y, v.linear.z = 0.16,0,0

    rate = rospy.Rate(10)
    n = 0

    while(n<10):

        pub.publish(v)
        n = n+1
        rate.sleep()

    v.linear.x = 0
    pub.publish(v)


def rotate(velocity_publisher, angular_speed_degree, relative_angle_degree, clockwise):

    print("---------------- inside rotate -------------------")

    v = Twist()
    angular_speed = math.radians(abs(angular_speed_degree))

    if (clockwise):
        v.angular.z = -abs(angular_speed)
    else:
        v.angular.z = abs(angular_speed)

    #angle_moved = 0.0
    #loop_rate = rospy.Rate(10) # we publish the velocity at 10 Hz (10 times a second)  
    '''
    t0 = rospy.Time.now().to_sec()

    while True :

        rospy.loginfo("======== rotating ============")
        velocity_publisher.publish(v)

        t1 = rospy.Time.now().to_sec()
        current_angle_degree = (t1-t0)*angular_speed_degree
        #loop_rate.sleep()
        
        if(current_angle_degree >= relative_angle_degree):
            rospy.loginfo("========= reached ===========")
            break
    '''

    n = 0
    rate = rospy.Rate(9)

    limit = 9

    if relative_angle_degree==180:
        limit=18

    while(n<limit):

        n=n+1
        velocity_publisher.publish(v)
        rate.sleep()
        
    v.angular.z =0
    velocity_publisher.publish(v)

def backward():

    global orientation,pub

    rotate(pub,90,180,True)
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

    global orientation,pub

    rotate(pub,90,90,False)
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

    global orientation,pub

    rotate(pub,90,90,True)
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

    print("---------------- inside decideDirection -------------------------")

    if(j<=7 and i<=7): # priority right-down-top-left  // 2nd quadrant 

        if(orientation==0):
        
            if(dist_l>0.15 and visited[i][j+1]==0): 
                dirn = "left"
            elif(dist_c>0.15 and visited[i+1][j]==0): 
                dirn = "front"
            elif(dist_r>0.15 and visited[i][j-1]==0): 
                dirn = "right"
            else: 
                backtrack()
        
        elif(orientation==1):
        
            if(dist_l>0.15 and visited[i][j+1]==0): 
                dirn = "left"
            elif(dist_c>0.15 and visited[i+1][j]==0): 
                dirn = "front"
            elif(dist_r>0.15 and visited[i][j-1]==0): 
                dirn = "right"
            else:
                backtrack()
        
        elif(orientation==2):
        
            if(dist_l>0.15 and visited[i][j+1]==0): 
                dirn = "left"
            elif(dist_c>0.15 and visited[i+1][j]==0): 
                dirn = "front"
            elif(dist_r>0.15 and visited[i][j-1]==0): 
                dirn = "right"            
            else: 
                backtrack()
        
        elif(orientation==3):
        
            if(dist_l>0.15 and visited[i][j+1]==0): 
                dirn = "left"            
            elif(dist_c>0.15 and visited[i+1][j]==0): 
                dirn = "front"
            elif(dist_r>0.15 and visited[i][j-1]==0): 
                dirn = "right"            
            else: 
                backtrack()
        
    elif(j>=8 and i<=7): #// priority left-down-top-right  // 1st quadrant

        if(orientation==0):
    
            if(dist_r>0.15 and visited[i][j-1]==0): 
                dirn = "right"            
            elif(dist_c>0.15 and visited[i+1][j]==0): 
                dirn = "front"
            elif(dist_l>0.15 and visited[i][j+1]==0): 
                dirn = "left"
            else:
                backtrack()
        
        elif(orientation==1):
        
            if(dist_l>0.15 and visited[i][j-1]==0): 
                dirn = "left"
            elif(dist_c>0.15 and visited[i-1][j]==0): 
                dirn = "front"
            elif(dist_r>0.15 and visited[i][j+1]==0): 
                dirn = "right"
            else:
                backtrack()
        
        elif(orientation==2):
        
            if(dist_r>0.15 and visited[i+1][j]==0): 
                dirn = "right"            
            elif(dist_l>0.15 and visited[i-1][j]==0): 
                dirn = "left"
            elif(dist_r>0.15 and visited[i][j+1]==0): 
                dirn = "front"            
            else:
                backtrack()
        
        elif(orientation==3):
        
            if(dist_c>0.15 and visited[i][j-1]==0): 
                dirn = "front"
            elif(dist_l>0.15 and visited[i+1][j]==0): 
                dirn = "left"
            elif(dist_r>0.15 and visited[i][j-1]==0): 
                dirn = "right"            
            else:
                backtrack()
        
    elif(j<=7 and i>=8): #// priority right-top-down-left  // 3rd quadrant
    
        if(orientation==0):
        
            if(dist_l>0.15 and visited[i][j+1]==0): 
                dirn = "left"
            elif(dist_c>0.15 and visited[i+1][j]==0): 
                dirn = "front"
            elif(dist_r>0.15 and visited[i][j-1]==0): 
                dirn = "right"            
            else:
                backtrack()
        
        elif(orientation==1):
        
            if(dist_r>0.15 and visited[i][j+1]==0): 
                dirn = "right"            
            elif(dist_c>0.15 and visited[i-1][j]==0): 
                dirn = "front"
            elif(dist_l>0.15 and visited[i][j-1]==0): 
                dirn = "left"            
            else:
                backtrack()
        
        elif(orientation==2):
        
            if(dist_c>0.15 and visited[i][j+1]==0): 
                dirn = "front"            
            elif(dist_l>0.15 and visited[i-1][j]==0): 
                dirn = "left"
            elif(dist_r>0.15 and visited[i+1][j]==0): 
                dirn = "right"            
            else:
                backtrack()
        
        elif(orientation==3):
        
            if(dist_r>0.15 and visited[i-1][j]==0): 
                dirn = "right"            
            elif(dist_l>0.15 and visited[i+1][j]==0): 
                dirn = "left"
            elif(dist_c>0.15 and visited[i][j+1]==0): 
                dirn = "front"            
            else:
                backtrack()
        
    elif(j>=8 and i>=8): #// priority left-top-down-right  // 4th quadrant 
    
        if(orientation==0):
        
            if(dist_r>0.15 and visited[i][j-1]==0): 
                dirn = "right"            
            elif(dist_c>0.15 and visited[i+1][j]==0): 
                dirn = "front"
            elif(dist_l>0.15 and visited[i][j+1]==0): 
                dirn = "left"            
            else:
                backtrack()
        
        elif(orientation==1):
        
            if(dist_l>0.15 and visited[i][j-1]==0): 
                dirn = "left"            
            elif(dist_c>0.15 and visited[i-1][j]==0): 
                dirn = "front"
            elif(dist_r>0.15 and visited[i][j+1]==0): 
                dirn = "right"            
            else:
                backtrack()
        
        elif(orientation==2):
        
            if(dist_l>0.15 and visited[i-1][j]==0): 
                dirn = "left"            
            elif(dist_r>0.15 and visited[i+1][j]==0): 
                dirn = "right"
            elif(dist_c>0.15 and visited[i][j+1]==0): 
                dirn = "front"            
            else:
                backtrack()
        
        elif(orientation==3):
        
            if(dist_c>0.15 and visited[i][j-1]==0): 
                dirn = "front"            
            elif(dist_r>0.15 and visited[i-1][j]==0): 
                dirn = "right"
            elif(dist_l>0.15 and visited[i+1][j]==0): 
                dirn = "left"            
            else:
                backtrack()

def clbk_laser(msg):

    global dist_l, dist_c, dist_r

    print( "---------------- inside callback_laser -------------------------")

    regions = [
        round(100*min(min(msg.ranges[0:71]), 100)),
        round(100*min(min(msg.ranges[72:143]), 100)),
        round(100*min(min(msg.ranges[144:215]), 100)),
        round(100*min(min(msg.ranges[216:287]), 100)),
        round(100*min(min(msg.ranges[288:359]), 100)),
    ]

    #print("l:  \t c:  \t r: ".format(regions[4], regions[2], regions[0]))
    
    dist_l,dist_c,dist_r = regions[4],regions[2],regions[0]

def clbk_odo(msg):

    global x,y,i,j,state,position_

    position_ = msg.pose.pose.position
    x,y = position_.x,position_.y
    state = 1

    if(x>0):
        i = int(round(abs(7 + ((x/0.085)+1)/2)))
    else:
        i = int(round(abs(7 - ((abs(x)/0.085)-1)/2)))

    if(y>0):
        j = int(round(abs(7 - ((y/0.085)-1)/2)))
    else:
        j = int(round(abs(7 + ((abs(y)/0.085)+1)/2)))
    
    print( "---------------- inside callback_odom -------------------------")
    print("x: ",x," y: ",y," i: ",i," j: ",j)
    print("---------------------------------------------------------------")

def setOrientation():
    
    global x,y,i,j,orientation

    print("----------------- inside setOrientation -------------------")
    print("x: ",x," y: ",y)
    print("---------------------------------------------------------------")

    if(x>0 and y>0):   # 1st quad

        forward()
        x1,y1 = x,y
        backward() 
        rotate(pub,90,180,True)

        if(x1 == x-1): 
            orientation=3 #//left facing
        else:
            orientation = 0
    
    elif(x<0 and y>0):   #2nd quad

        forward()
        x1,y1 = x,y
        backward() 
        rotate(pub,90,180,True)

        if(x1 == x+1):
            orientation = 2   #right facing
        else:
            orientation = 0

    elif(x<0 and y<0):    # 3rd quad
    
        forward()
        x1,y1 = x,y
        backward() 
        rotate(pub,90,180,True)

        if(x1 == x+1): 
            orientation = 2    #right facing
        else:
            orientation = 1
    
    elif(x>0 and y<0):            #4th quad
    
        forward()
        x1,y1 = x,y
        backward() 
        rotate(pub,90,180,True)

        if(x1 == x-1):
            orientation=3       #left facing
        else: 
            orientation = 1

def main():

    global pub,x,y,i,j,state

    rospy.init_node('final_runner', anonymous=True)
    sub_laser = rospy.Subscriber('/my_mm_robot/laser/scan', LaserScan, clbk_laser)
    sub_odom = rospy.Subscriber('/odom', Odometry, clbk_odo)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    rate = rospy.Rate(0.5)

    while(state==0):
        rate.sleep()
        print("----------------- inside state==0 -------------------")

    setOrientation()
        
    while not rospy.is_shutdown():

        print("----------------- inside not rospy.is_shutdown() -------------------")

        if(visited[i][j] == 0):
            path.append(i*16 + j)

        visited[i][j] = 1

        if((i==7 or i==8) and (j==7 or j==8)):
            break

        decideDirection()

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
