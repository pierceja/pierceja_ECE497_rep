#!/usr/bin/env python3
import Adafruit_BBIO.GPIO as GPIO
import time

input="GP1_3"
output="GP1_4"

# Set the GPIO pins:
GPIO.setup(input, GPIO.IN)
GPIO.setup(output, GPIO.OUT)

# Map buttons to LEDs
map = {input: output}

def updateLED(channel):
	state = GPIO.input(channel)
	GPIO.output(map[channel], state)

print("Running...")

GPIO.add_event_detect(input, GPIO.BOTH, callback=updateLED)

try:
	while True:
		time.sleep(100)

except KeyboardInterrupt:
	print("Cleaning Up")
	GPIO.cleanup()
