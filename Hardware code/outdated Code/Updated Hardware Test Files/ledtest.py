# Write your code here :-) gpio12pin32 and GNDpin25
import RPi.GPIO as GPIO
import time

def ledRun():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(12,GPIO.OUT)
    while True:
        print ("LED on")
        GPIO.output(12,GPIO.HIGH)
        time.sleep(1)
        print ("LED off")
        GPIO.output(12,GPIO.LOW)
        time.sleep(1)

ledRun()