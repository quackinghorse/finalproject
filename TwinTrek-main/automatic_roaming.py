import math
import time
import random
from buggyController  import BuggyController


bc = BuggyController()
bc.gpsSetup()
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24

directions=["Left","Right"]


bc.ultrasonicSetup(GPIO_TRIGGER,GPIO_TRIGGER) 

def roaming():
    
        
    while True:         
        #keep moving till no obstacle encounter

        while(bc.getDistance()>80):
            bc.forward()
            time.sleep(4)
            direction = random.choice(directions)
            t = random.random(1,5)
            if(direction=="Left"):
                bc.left()
                time.sleep(t)
            else:
                bc.right()
                time.sleep(t)

            

        
        if(bc.getDistance()<=80):
            print("Stop")
            # rotate buggy right while ultrasonic.distance<0.2
            while(bc.getDistance()<=20):
                bc.right()
            # move buggy in that direction for 5 seconds
            