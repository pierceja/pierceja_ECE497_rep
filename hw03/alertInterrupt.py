#!/usr/bin/env python3
import Adafruit_BBIO.GPIO as GPIO
import smbus
import time

print("This program waits for an interrupt caused from one of the TMP101 devices")
print("The temperature is printed in Fahrenheit after each interrupt")

bus = smbus.SMBus(1)
address1 = 0x48
address2 = 0x49

alert1 = "GP0_6"
alert2 = "GP0_4"

GPIO.setup(alert1, GPIO.IN)
GPIO.setup(alert2, GPIO.IN)

def intHandler(channel):
	if channel == alert1:
		print(bus.read_byte_data(address2,0x00)*(9/5)+32)

	else:
		print(bus.read_byte_data(address1, 0x00)*(9/5)+32)


print("Running...")

GPIO.add_event_detect(alert1, GPIO.BOTH, callback=intHandler)
GPIO.add_event_detect(alert2, GPIO.BOTH, callback=intHandler)

while 1:
	time.sleep(20)
