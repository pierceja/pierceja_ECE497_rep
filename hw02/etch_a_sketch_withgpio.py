#!/usr/bin/env python3
import Adafruit_BBIO.GPIO as GPIO
import curses
import time

print("This is a simple etch-a-sketch program.")
print("Begin by entering a single number for the horizontal and vertical grid size")
print("Use the push buttons to move position")
print("Button 1 moves up, Button 2 moves down, Button 3 moves left, Button 4 moves right")
print("c clears the etch-a-sketch and q is used to quit")
print("Make sure your terminal screen is big eneough to accommmodate the grid size")
print("If it's too small, you will get errors when moving to a position off the terminal")

GRID_SIZE = int(input("size: "))  #The etch-a-sketch dimensions will be size x size

#GPIOs
Button1="GP0_6"
Button2="GP0_5"
Button3="GP0_4"
Button4="GP0_3"

gpios=[Button1, Button2, Button3, Button4]

#Set the GPIO pins:
for i in range(len(gpios)):
	GPIO.setup(gpios[i], GPIO.IN)

#Map buttons to LEDs

SPACING = 1 #Spacing between etch-a-sketch characters
stdscr = curses.initscr() #Initialization for the curses import
curses.noecho()
curses.cbreak()

position_x=10 #Keeps track of user position during game
position_y=0
xnum = 1 #Used for the etch-a-sketch boundaries
ynum = 1

stdscr.addstr(position_y,position_x,'X') #Used to add an X to current position
playGame=True #True until the user quits the game

#Detect button pushes and change curser position accordingly
def updateBoard(channel):
	global Button1
	global Button2
	global Button3
	global Button4
	global ynum
	global xnum
	global GRID_SIZE
	global position_y
	global position_x
	global SPACING

	if channel == Button1:
		if ynum!=1:
			position_y = position_y - SPACING
			stdscr.addstr(position_y, position_x, "X")
			stdscr.refresh()
			ynum=ynum-1

	elif channel == Button2:
		if ynum != GRID_SIZE:
			position_y=position_y+SPACING
			stdscr.addstr(position_y, position_x, "X")
			ynum=ynum+1
			stdscr.refresh()

	elif channel == Button3:
		if xnum != 1:
			position_x=position_x-SPACING
			stdscr.addstr(position_y, position_x, "X")
			xnum = xnum-1
			stdscr.refresh()

	elif channel == Button4:
		if xnum!=GRID_SIZE:
			position_x=position_x + SPACING
			stdscr.addstr(position_y, position_x, "X")
			stdscr.refresh()
			xnum=xnum+1

print("Running...")

for i in range(len(gpios)):
	GPIO.add_event_detect(gpios[i], GPIO.RISING, callback=updateBoard)

try:
	while playGame:
		c=stdscr.getch() #Get keyboard input

		if c== ord('q'):
			playGame=False

		elif c== ord('c'):
			stdscr.clear()
			position_x=10
			position_y=0
			xnum=1
			ynum=1	
			stdscr.addstr(position_y, position_x, "X")

except KeyboardInterrupt:
	print("Cleaning Up")
	GPIO.cleanup()

curses.endwin()

