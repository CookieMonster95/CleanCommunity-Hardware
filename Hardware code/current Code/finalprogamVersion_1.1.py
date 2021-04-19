#!/usr/bin/python

#import
import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD
import serial
import time
import smbus
import board
import busio
import firebase
import adafruit_sgp30

#froms 
from time import sleep
from cleancommunityfunction import *

#LCD pin setup
lcd_rs = 4
lcd_en = 17
lcd_d4 = 18
lcd_d5 = 22
lcd_d6 = 23
lcd_d7 = 24
lcd_backlight = 4
lcd_columns = 16
lcd_rows  = 2
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
lcd.show_cursor(False)
lcd.clear()
#Neo6m(gps) setup
mport = "/dev/ttyAMA0"
ser = serial.Serial(mport, 9600, timeout=2)

#si7021(temp&hum sensor) setup
bus = smbus.SMBus(1)
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


i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
sgp30.iaq_init()
sgp30.set_iaq_baseline(0x8973, 0x8AAE)

#main function 
if __name__ == "__main__":
#main loop 
    while True:
        try:
		#reading gps data and decoding it afterwords formating it to a float with 5 postions 
            dat = ser.readline().decode()
            mylat, mylon = parseGPS(dat)
            mylat = float("{:.5f}".format(mylat))
            mylon = float("{:.5f}".format(mylon))
		#display lat and lon on LCD screen
            lcd.message("Lat:{0:0.4f}\nLon:{1:0.4f}".format(mylat, mylon))
            time.sleep(2.0)
		#after waiting 2 seconds clear lcd screen
            lcd.clear()
		#checks if devices moved if not just display lat and lon on lcd screen
            if float("{:.5f}".format(mylon)) == prevlon and float("{:.5f}".format(mylat)) == prevlat:
                lcd.clear()
                lcd.message("Lat:{0:0.4f}\nLong:{1:0.4f}".format(mylat, mylon))
                time.sleep(5.0)
                lcd.clear()
		#save your current long and lat in a varaible to hold the perivus lon and lat used in the if above
                prevlon = mylon
                prevlat = mylat
            else:
                print (mylon)
                print (mylat)
				#checks if current lon and lat are in the firebase
                checkLocation = firebase.checkLocation(mylon, mylat)
				#checks to see if checkLocation isnt 0 which happens if mylon and mylat are not points in the database
                if checkLocation != 0:
					#checkLocation into gpsLocation 
                    gpsLocation = checkLocation[0]
                    print (gpsLocation)
					#spliting gpsLocation lat and lng into circleLatitude and circleLongitude
                    circleLatitude = gpsLocation['lat']
                    circleLongitude = gpsLocation['lng']
					#using checkCircledata to see if circle form dataase holds old sensor data using (datacheck as a flag 1 has data 0 doesnt not)
                    datacheck = firebase.checkCircledata(circleLongitude, circleLatitude)
                    if datacheck == 1:
						#if data exists
                        print ("if")
						#grab the data for the circle (found with circleLongitude,circleLatitude)
						#then display daya on lcd screen
                        sensorData=firebase.grabdatareadings(circleLongitude, circleLatitude)
                        lcd.message("Lat:{0:0.3f}\nLong:{1:0.3f}".format(circleLatitude, circleLongitude))
                        time.sleep(1.0)
                        lcd.clear()
                        lcd.message("CO2: {0:0.3f}\ntVOC: {1:0.3f}".format(sensorData['CO2'], sensorData['tVOC']))
                        time.sleep(1.0)
                        lcd.clear()
                        lcd.message("Humidity :{0:0.3f}\nTemp :{1:0.3f}".format(sensorData["Humidity"], sensorData["temp"]))
                    else:
						#
                        print ("else")
                        #grab datas and will also display it on the lcd screen
                        lcd.clear()
                        eCO2, tVoc = sgp30.iaq_measure()
                        lcd.message("Lat:{0:0.3f}\nLong:{1:0.3f}".format(circleLatitude, circleLongitude))
                        time.sleep(1.0)
                        lcd.clear()
                        lcd.message("CO2: {0:0.3f}\ntVOC: {1:0.3f}".format(CO2,tVoc))
                        time.sleep(1.0)
                        lcd.clear()
                        lcd.message("Humidity :{0:0.3f}\nTemp :{1:0.3f}".format(humidity,celsTemp))
                        time.sleep(1.0)
                        lcd.clear()
						#send the grabed data to firebase
                        firebase.senddata (circleLongitude, circleLatitude, celsTemp, humidity, CO2, tVoc)
                time.sleep(3.0)
                lcd.clear()
        except:
            x = 1

