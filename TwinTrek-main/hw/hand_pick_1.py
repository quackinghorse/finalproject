import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
pwm=GPIO.PWM(21, 50)
pwm.start(0)

def SetAngle(angle):
	duty = angle/18 + 2
	GPIO.output(21, True)
	pwm.ChangeDutyCycle(duty)
	sleep(1)
	GPIO.output(21, False)
	pwm.ChangeDutyCycle(0)
	
SetAngle(0)
sleep(2)
SetAngle(30)
pwm.stop()
