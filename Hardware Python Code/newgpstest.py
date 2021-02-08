#!/usr/bin/python

import time
import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD
import serial
import time
from si7021 import *
#from CCS811run import *
from time import sleep
from ccs811 import *
from cleancommunityfunction import *
import smbus

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
data0 = bus.read_byte(0x40)
data1 = bus.read_byte(0x40)
humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6
time.sleep(0.3)
bus.write_byte(0x40, 0xF3)
time.sleep(0.3)
data0 = bus.read_byte(0x40)
data1 = bus.read_byte(0x40)
celsTemp = ((data0 * 256 + data1) * 175.72 / 65536.0) - 49.85
fahrTemp = celsTemp * 1.8 + 32
prevlat = 1.0
prevlon = 1.0
ccs811Begin(CCS811_driveMode_1sec)

while True:
    ledoff()
    try:
        dat = ser.readline().decode()
        mylat, mylon = parseGPS(dat)
        mylat = float("{:.5f}".format(mylat))
        mylon = float("{:.5f}".format(mylon))
        lcd.message("Lat:{0:0.4f}\nLon:{1:0.4f}".format(mylat, mylon))
        time.sleep(5.0)
        lcd.clear()
        if float("{:.3f}".format(mylon)) == prevlon and float("{:.3f}".format(mylat)) == prevlat:
            lcd.clear()
            lcd.message("Lat:{0:0.3f}\nLong:{1:0.3f}".format(mylat, mylon))
            time.sleep(5.0)
            lcd.clear()
            
        else:

            if ccs811CheckDataAndUpdate():
                ledRun()
                CO2 = ccs811GetCO2()
                tVOC = ccs811GetTVOC()
                lcd.clear()
                print ("checkupdate: CO2 : %d ppm" % CO2)
                print ("checkupdate: tVOC : %d ppb \n" % tVOC)
                print ("checkupdate: Relative Humidity is : %.2f %% \n" % humidity)
                print ("checkupdate: Temperature in Celsius is : %.2f C \n" % celsTemp)
                print ("checkupdate:Temperature in Fahrenheit is : %.2f F \n" % fahrTemp)
                lcd.message("CO2:{0:0.2f}\ntVOC:{1:0.2f}".format(CO2, tVOC))
                time.sleep(2.0)
                lcd.clear()
                lcd.message("Humidity:{0:0.2f}\nTemp:{1:0.2f}C".format(humidity,celsTemp))
                time.sleep(5.0)
                time.sleep(1.0)
                lcd.clear()
                

            elif ccs811CheckForError():
                ccs811PrintError()
                lcd.message(ccs811PrintError())
                ledRun()
                time.sleep(10.0)
                lcd.clear()

            else:
                CO2 = ccs811GetCO2()
                tVOC = ccs811GetTVOC()
                lcd.clear()
                print("CO2 : %d ppm" % CO2)
                print ("tVOC : %d ppb \n" % tVOC)
                print ("Relative Humidity is : %.2f %% \n" % humidity)
                print ("Temperature in Celsius is : %.2f C \n" % celsTemp)
                print ("Temperature in Fahrenheit is : %.2f F \n" % fahrTemp)
                lcd.message("CO2:{0:0.2f}\ntVOC:{1:0.2f}".format(CO2, tVOC))
                time.sleep(2.0)
                lcd.clear()
                lcd.message("Humidity:{0:0.2f}\nTemp:{1:0.2f}C".format(humidity,celsTemp))
                ledRun()
                time.sleep(10.0)
                ledoff()
                lcd.clear()
    except:
        x = 1

