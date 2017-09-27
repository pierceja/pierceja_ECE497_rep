#!/usr/bin/env python3
import Adafruit_BBIO.GPIO as GPIO
import curses
import time
import smbus
import math
import rcpy
import rcpy.encoder as encoder

print("This is a simple etch-a-sketch program that uses rotary encoders and an LED matrix")
print("Use the rotary encoders to change position")
print("The encoder in port 2 changes the horizontal position")
print("The encoder in port 3 changes the vertical position")
print("The Mode button clears the game and the Pause button quits")

bus = smbus.SMBus(1)
matrix=0x70
bus.write_byte_data(matrix, 0x0000, 1)

#Matrix setup
bus.write_byte_data(matrix, 0x21, 0)
bus.write_byte_data(matrix, 0x81, 0)
bus.write_byte_data(matrix, 0xe7, 0)

board=[0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
bus.write_i2c_block_data(matrix, 0, board)

#Keep track of the current index (or current column in the LED matrix)
currentIndex=1

#Vertical position in the current column on the display
yPos=1

yp1=1
yp2=2
yp3=3
yp4=4
yp5=5
yp6=6
yp7=7
yp8=8
yp9=9

blk1=1
blk2=2
blk3=4
blk4=8
blk5=16
blk6=32
blk7=64
blk8=128
blk9=256

#Keep track of the previous rotary encoder values
currentEncoder2=0
currentEncoder3=0
rcpy.set_state(rcpy.RUNNING)

#This maps column positions to binary values so that the correct pixels will light up as you move around the display
map={yp1:blk1,yp2:blk2,yp3:blk3,yp4:blk4,yp5:blk5,yp6:blk6,yp7:blk7,yp8:blk8,yp9:blk9}

#GPIOs
Button1="MODE"
Button2="PAUSE"

gpios=[Button1, Button2]

#Set the GPIO pins:
for i in range(len(gpios)):
	GPIO.setup(gpios[i], GPIO.IN)

playGame=True #True until the user quits the game

#Detect button pushes and change the i2c data accordingly
def updateBoard(channel):
	global Button1
	global Button2
	global board
	global currentIndex
	global yPos
	global playGame

	#Clears the LED matrix
	if channel == Button1:
		board=[0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        		0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
		bus.write_i2c_block_data(matrix, 0, board)
		currentIndex=1
		yPos=1
	
	#Stops the script
	elif channel == Button2:
		playGame=False


print("Running...")

for i in range(len(gpios)):
	GPIO.add_event_detect(gpios[i], GPIO.FALLING, callback=updateBoard)


while playGame:
	#Compare the current encoder values with the previous values. If the values are different, change the i2c data for the matrix accordingly
	if rcpy.get_state()==rcpy.RUNNING:
		time.sleep(0.3)
		e2=encoder.get(2)
		e3=encoder.get(3)
		if e2<currentEncoder2:
			currentEncoder2=e2
			if currentIndex!=1:
				board[currentIndex-1]=0
				currentIndex-=2 #Change the current index of the i2c data matrix. This changes the column you are in
				board[currentIndex-1]=map[yPos]
				board[currentIndex]=board[currentIndex] | map[yPos]
				bus.write_i2c_block_data(matrix, 0, board)


		elif e2>currentEncoder2:
			currentEncoder2=e2
			if currentIndex!=15:
				board[currentIndex-1]=0
				currentIndex+=2
				board[currentIndex-1]=map[yPos]
				board[currentIndex]=board[currentIndex] | map[yPos]
				bus.write_i2c_block_data(matrix, 0, board)

		elif e3<currentEncoder3:
			currentEncoder3=e3
			if yPos!=8:
				yPos+=1 #This increases to keep track of your vertical position
				board[currentIndex-1]=map[yPos] #Changes the users current position to yellow
				board[currentIndex]=board[currentIndex] | map[yPos] #Or the correct binary value with the i2c data to change vertical position and keep your trail
				bus.write_i2c_block_data(matrix, 0, board)

		elif e3>currentEncoder3:
			if yPos!=1:
				yPos-=1
				currentEncoder3=e3
				board[currentIndex-1]=map[yPos]
				board[currentIndex-1]=board[currentIndex-1] & map[yPos]
				board[currentIndex]=board[currentIndex] | map[yPos]
				bus.write_i2c_block_data(matrix, 0, board)

		
