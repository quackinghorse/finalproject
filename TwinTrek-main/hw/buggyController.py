import RPi.GPIO as GPIO 
import py_qmc5883l
import serial
import pynmea2

import time
from time import *
import threading
 

class BuggyController(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(BuggyController, cls).__new__(cls)
        return cls.instance
    
    def setDestination(self,lat,long):
        self.destination = (lat,long)
        
    def getDestination(self):
        return self.destination
        

    def magnetoSetup(self):
        self.sensor = py_qmc5883l.QMC5883L()
        # self.sensor.calibration = [[1.0270995979508475, -0.020248684731951426, 1902.8581272409879], [-0.020248684731951454, 1.0151297164672932, -2031.7481674046921], [0.0, 0.0, 1.0]]
        self.sensor.set_calibration = [[1.0489967470879635, -0.02151759396585279, 1259.6704669094697], [-0.021517593965852795, 1.0094497467198806, -3009.4396690704766], [0.0, 0.0, 1.0]]
    def setup(self,in1=19,in2=13,en=26,in3=5,in4=6,enb=0):
        if not hasattr(self,'runSetup'):
            self.runSetup = False
            try:
                self.cleanup()
            except:
                print("cleaned")
            
            self.destination = None
            
            
            
            try:
                self.sensor = py_qmc5883l.QMC5883L()
                self.sensor.set_calibration = [[1.0489967470879635, -0.02151759396585279, 1259.6704669094697], [-0.021517593965852795, 1.0094497467198806, -3009.4396690704766], [0.0, 0.0, 1.0]]

                # self.sensor.calibration = [[1.0270995979508475, -0.020248684731951426, 1902.8581272409879], [-0.020248684731951454, 1.0151297164672932, -2031.7481674046921], [0.0, 0.0, 1.0]]
            except:
                print("magneto setup error")
            self.in1 = in1
            self.in2 = in2
            self.en = en
            self.in3 = in3
            self.in4 = in4
            self.enb = enb

            GPIO.setmode(GPIO.BCM)
            GPIO.setup(in1,GPIO.OUT)
            GPIO.setup(in2,GPIO.OUT)
            GPIO.setup(en,GPIO.OUT)
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.LOW)
            self.p=GPIO.PWM(en,1000)

            GPIO.setup(in3,GPIO.OUT)
            GPIO.setup(in4,GPIO.OUT)
            GPIO.setup(enb,GPIO.OUT)
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.LOW)
            self.q=GPIO.PWM(enb,1000)
            self.q.start(40)
            self.p.start(40)
            self.dc = 40

    
    
    def forward(self):
        print("f")
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.HIGH)
        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.HIGH)
    
    def backward(self):
        print("b")
        GPIO.output(self.in1,GPIO.HIGH)
        GPIO.output(self.in2,GPIO.LOW)
        GPIO.output(self.in3,GPIO.HIGH)
        GPIO.output(self.in4,GPIO.LOW)
        
    
    def setSpeed(self,s):
        print("set: ",s)
        self.dc = s
        self.p.ChangeDutyCycle(s)
        self.q.ChangeDutyCycle(s)
    

    
    # def left(self):
    #     print("l")
    #     self.p.ChangeDutyCycle(0)
    #     self.q.ChangeDutyCycle(50)

    def left(self):
        print("l")
        # self.p.ChangeDutyCycle(45)
        # self.q.ChangeDutyCycle(45)
        GPIO.output(self.in1,GPIO.HIGH)
        GPIO.output(self.in2,GPIO.LOW)
        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.HIGH)
    
    def right(self):
        print("r")
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.HIGH)
        GPIO.output(self.in3,GPIO.HIGH)
        GPIO.output(self.in4,GPIO.LOW)

        
    def mark(self):
        print("marked")
        
    def setAngle(self,angle,arm,pwm):
        duty = angle/18 + 2
        GPIO.output(arm, True)
        pwm.ChangeDutyCycle(duty)
        sleep(1)
        GPIO.output(arm, False)
        pwm.ChangeDutyCycle(0)
        
        
    def pickDropSetup(self,a1=21,a2=20):
        if not hasattr(self,"arm1"):
            self.arm1 = a1
            self.arm2 = a2
            
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.arm1, GPIO.OUT)
            self.pwm1=GPIO.PWM(self.arm1, 50)
            self.pwm1.start(0)
            
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.arm2, GPIO.OUT)
            self.pwm2=GPIO.PWM(self.arm2, 50)
            self.pwm2.start(30)
            
        
    
    def pick(self):
        threading.Thread(target=self.setAngle,args=(0,self.arm1,self.pwm1)).start()
        self.setAngle(60,self.arm2,self.pwm2)
    
    def drop(self):
        threading.Thread(target=self.setAngle,args=(30,self.arm1,self.pwm1)).start()
        self.setAngle(30,self.arm2,self.pwm2)
        
    def stop(self):
        
        print("s")
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)
        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.LOW)
     
    def gpsSetup(self,port="/dev/ttyS0",baud = 9600,timeout=0.5):
        if not hasattr(self,'gpsSerial'):
            self.gpsSerial=serial.Serial(port=port,baudrate=baud,timeout=timeout)
            dataout = pynmea2.NMEAStreamReader()
        
    def getLatLong(self):
        while True:
            newdata=self.gpsSerial.readline()
            newdata = newdata.decode()
            if newdata[0:6] == "$GPGLL":
                newmsg=pynmea2.parse(newdata)
                lat=newmsg.latitude
                lng=newmsg.longitude
                return (lat,lng)
                
    

    
    def getSmokeLevel(self):
        return 1.234
    
    def get_current_direction(self):
       
        heading = ""
        # while True:
        m = self.sensor.get_magnet()
        bearing = self.sensor.get_bearing()
        # x=m[0]
        # y=m[1]
        # print(x,y)
        # heading = ""

        if(bearing>=54 and bearing<=66):
            heading="West"
        elif(bearing>66 and bearing<86.5):
            heading="North-West"
        elif(bearing>=86.5 and bearing<=107):
            heading="North"
        elif(bearing>107 and bearing<136):
            heading="North-East"
        elif(bearing>=136 and bearing<=157):
            heading="East"
        elif(bearing>157 and bearing<184):
            heading="South-East"
        elif(bearing>=184 and bearing<=210):
            heading="South"
        else:
            heading="South-West"
        # if(x<80 and x>-700 and y>=1700 and y<=2150):
        #     heading = "North"
        # elif(x>-1700 and x<-700 and  y>480 and y<1800):
        #     heading = "North-East"
        # elif(x<-1600 and x>-2000 and y<500 and y>-600):
        #     heading = "East"
        # elif(x>-1600 and x<-300 and  y>-1800 and y<400):
        #     heading = "South-East"
        # elif(x>-300 and x<700 and y>-1800 and y<-1400):
        #     heading = "South"
        # elif(x>690 and x<1800 and y<270 and y>-1700):
        #     heading = "South-West"
        # elif(x<1850 and x>1550 and y>=-50 and y<=790):
        #     heading = "West"
        # elif(x>110 and x<1550 and y>790 and y<2000):
        #     heading = "North-West"
        # else:
        #     heading = "Need Calibration!"

        # print("x = "+str(x)+" y= "+str(y)+" heading = "+heading)
        return heading
        
    def ultrasonicSetup(self,trig=18,ech=24):
        if not hasattr(self,"trigger"):
            self.trigger = trig
            self.echo = ech
            GPIO.setmode(GPIO.BCM)
            # self.setup()
            GPIO.setup(trig, GPIO.OUT)
            GPIO.setup(ech, GPIO.IN)    
        
    def getDistance(self):      # return distance in cm
        # set Trigger to HIGH
        GPIO.output(self.trigger, True)
    
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.trigger, False)
    
        StartTime = time.time()
        StopTime = time.time()
    
        # save StartTime
        while GPIO.input(self.echo) == 0:
            StartTime = time.time()
    
        # save time of arrival
        while GPIO.input(self.echo) == 1:
            StopTime = time.time()
    
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
    
        return distance
    
    def cleanup(self):
        print("c")
        GPIO.cleanup()
        
    # def __del__(self):
    #     self.cleanup()
