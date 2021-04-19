import RPi.GPIO as GPIO
import time
# LED function
def ledRun():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(12,GPIO.OUT)
    print ("LED on")
    GPIO.output(12,GPIO.HIGH)
  

def ledoff():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(12,GPIO.OUT)
    print ("LED off")
    GPIO.output(12,GPIO.LOW)
    

# GPS function
def parseGPS(data):
    if data[0:6] == "$GPGGA":
        s = data.split(",")
        if s[7] == '0' or s[7] == '00':
            print ("no satellite data available")
            return
        time = s[1][0:2] + ":" + s[1][2:4] + ":" + s[1][4:6]
        # print("-----------")
        lat = decode(s[2])
        lon = decode(s[4])
        return lat, lon

def decode(coord):
    l = list(coord)
    for i in range(0, len(l) - 1):
        if l[i] == ".":
            break
    base = l[0:i - 2]
    degi = l[i - 2:i]
    degd = l[i + 1:]
    baseint = int("".join(base))
    degiint = int("".join(degi))
    degdint = float("".join(degd))
    degdint = degdint / (10 ** len(degd))
    degs = degiint + degdint
    full = float(baseint) + (degs / 60)
    return full