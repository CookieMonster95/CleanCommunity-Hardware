#!/usr/bin/python

import time
import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD
import serial

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

lcd_rs = 4
lcd_en = 17
lcd_d4 = 18
lcd_d5 = 22
lcd_d6 = 23
lcd_d7 = 24
mport = "/dev/ttyAMA0"  # for Raspberry Pi pins
lcd_backlight = 4
lcd_columns = 16
lcd_rows    = 2
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

lcd.show_cursor(True)
time.sleep(2.0)
lcd.clear()
lcd.show_cursor(False)
lcd.clear()

ser = serial.Serial(mport, 9600, timeout=2)
prevlat = 1.0
prevlon = 1.0
while True:
    try:
        dat = ser.readline().decode()
        mylat, mylon = parseGPS(dat)
        mylat = float("{:.5f}".format(mylat))
        mylon = float("{:.5f}".format(mylon))

        if float("{:.4f}".format(mylon)) == prevlon and float("{:.4f}".format(mylat)) == prevlat:
            lcd.clear()
            lcd.message("Lat:{0:0.3f}\nLong:{1:0.3f}".format(mylat, mylon))
            time.sleep(10.0)


        else:
            print(prevlat, " e ", prevlon)
            prevlon = float("{:.4f}".format(mylon))
            prevlat = float("{:.4f}".format(mylat))
            lcd.clear()
            lcd.message("Lat:{0:0.3f}\nLong:{1:0.3f}".format(mylat, mylon))
            time.sleep(10.0)
            # firbase connect
            # closest circles
            # check if
    except:
        x = 1

