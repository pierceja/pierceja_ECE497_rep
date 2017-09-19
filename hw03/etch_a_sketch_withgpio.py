#!/usr/bin/env python3
import Adafruit_BBIO.GPIO as GPIO
import curses
import time
import smbus
import math

print("This is a simple etch-a-sketch program.")
print("Use the push buttons to move position")
print("Button 1 moves down, Button 2 moves up, Button 3 moves left, Button 4 moves right")
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

#This maps column positions to binary values so that the correct pixels will light up as you move around the display
map={yp1:blk1,yp2:blk2,yp3:blk3,yp4:blk4,yp5:blk5,yp6:blk6,yp7:blk7,yp8:blk8,yp9:blk9}

#GPIOs
Button1="GP0_6"
Button2="GP0_5"
Button3="GP0_4"
Button4="GP0_3"
Button5="MODE"
Button6="PAUSE"

gpios=[Button1, Button2, Button3, Button4, Button5, Button6]

#Set the GPIO pins:
for i in range(len(gpios)):
	GPIO.setup(gpios[i], GPIO.IN)

playGame=True #True until the user quits the game

#Detect button pushes and change the i2c data accordingly
def updateBoard(channel):
	global Button1
	global Button2
	global Button3
	global Button4
	global Button5
	global Button6
	global board
	global currentIndex
	global yPos
	global playGame

	time.sleep(0.3)
	if channel == Button1:
		if yPos!=8:
			yPos+=1 #This increases to keep track of where you are in the column
			board[currentIndex-1]=map[yPos] #Changes the users current position to yellow
			board[currentIndex]=board[currentIndex] | map[yPos] #Or the correct binary value with the i2c data for the current column. Oring this value allows the users trail to be left 
			bus.write_i2c_block_data(matrix, 0, board)

	elif channel == Button2:
		if yPos!=1:
			yPos-=1
			board[currentIndex-1]=map[yPos]
			board[currentIndex-1]=board[currentIndex-1] & map[yPos]
			board[currentIndex]=board[currentIndex] | map[yPos]
			bus.write_i2c_block_data(matrix, 0, board)

	elif channel == Button3:
		if currentIndex!=15:
			board[currentIndex-1]=0
			currentIndex+=2
			board[currentIndex-1]=map[yPos]
			board[currentIndex]=board[currentIndex] | map[yPos]
			bus.write_i2c_block_data(matrix, 0, board)

	elif channel == Button4:
		if currentIndex!=1:
			board[currentIndex-1]=0
			currentIndex-=2
			board[currentIndex-1]=map[yPos]
			board[currentIndex]=board[currentIndex] | map[yPos]
			bus.write_i2c_block_data(matrix, 0, board)

	elif channel == Button5:
		board=[0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        		0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
		bus.write_i2c_block_data(matrix, 0, board)
		currentIndex=1
		yPos=1
	
	elif channel == Button6:
		playGame=False


print("Running...")

for i in range(len(gpios)):
	GPIO.add_event_detect(gpios[i], GPIO.FALLING, callback=updateBoard)


while playGame:
	time.sleep(0.3)


