#!/usr/bin/python
import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD
import time
from time import sleep

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
testvar = 52

lcd.show_cursor(True)
time.sleep(1.0)
lcd.clear()
lcd.show_cursor(False)
lcd.message("LCD TEST")
time.sleep(1.0)
lcd.clear()
lcd.message("LCD var test \n {0:0.2f}".format(testvar))
time.sleep(1.0)
lcd.clear()
lcd.message("Done")
time.sleep(3.0)
lcd.clear()
