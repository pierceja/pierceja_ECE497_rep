#!/usr/bin/env python3
import Adafruit_BBIO.GPIO as GPIO
import time

Button1="GP0_6"
Button2="GP0_5"
Button3="GP0_4"
Button4="GP0_3"
LED1 ="GREEN"
LED2="RED"
LED3="GP1_4"
LED4="GP1_3"

gpios=[Button1, Button2, Button3, Button4, LED1, LED2, LED3, LED4]

# Set the GPIO pins:
for i in range(len(gpios)):
	if(gpios[i][2]=='0'):
		GPIO.setup(gpios[i], GPIO.IN)
	else:
		GPIO.setup(gpios[i], GPIO.OUT)

# Map buttons to LEDs
map = {Button1: LED1, Button2: LED2, Button3: LED3, Button4: LED4}

def updateLED(channel):
	print("channel = " + channel)
	state = GPIO.input(channel)
	GPIO.output(map[channel], state)
	print(map[channel] + " Toggled")

print("Running...")

for i in range(len(gpios)):
	 if(gpios[i][2]=='0'):
                GPIO.add_event_detect(gpios[i], GPIO.BOTH, callback=updateLED)

try:
	while True:
		time.sleep(100)

except KeyboardInterrupt:
	print("Cleaning Up")
	GPIO.cleanup()
