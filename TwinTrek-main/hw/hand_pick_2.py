import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.OUT)
pwm=GPIO.PWM(20, 50)
pwm.start(30)

def SetAngle(angle):
	duty = angle/18 + 2
	GPIO.output(20, True)
	pwm.ChangeDutyCycle(duty)
	sleep(1)
	GPIO.output(20, False)
	pwm.ChangeDutyCycle(0)
	

SetAngle(60)
sleep(2)
SetAngle(30)
pwm.stop()
