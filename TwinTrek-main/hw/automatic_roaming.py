import time
import random
from buggyController  import BuggyController


bc = BuggyController()
bc.setup()
bc.gpsSetup()
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24



# bc.ultrasonicSetup()

bc.ultrasonicSetup(GPIO_TRIGGER,GPIO_ECHO) 

def roaming():
    directions=["Left","Right"]
        
    while True:         
        #keep moving till no obstacle encounter

        while(bc.getDistance()>80):
            print(bc.getDistance())
            bc.forward()
            time.sleep(2)
            direction = random.choice(directions)
            t = random.randrange(1,5)
            if(direction=="Left"):
                bc.left()
                time.sleep(t)
            else:
                bc.right()
                time.sleep(t)

            

        
        if(bc.getDistance()<=80):
            print("Stop")
            # rotate buggy right while ultrasonic.distance<0.2
            while(bc.getDistance()<=80):
                print(bc.getDistance())
                bc.right()
                time.sleep(1)
            # move buggy in that direction for 5 seconds
roaming()
            