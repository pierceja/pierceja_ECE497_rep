#!/usr/bin/python

import curses

print("This is a simple etch-a-sketch program.")
print("Begin by entering a single digit for the horizontal and vertical grid size")
print("Use w to move up, s to move down, a to move left, and d to move right")
print("c clears the etch-a-sketch and q is used to quit")
print("Make sure your terminal screen is big eneough to accommmodate the grid size")
print("If it's too small, you will get errors when moving to a position off the terminal")

GRID_SIZE = int(input("size: ")) #The etch-a-sketch dimensions will be size x size
SPACING = 1 #Spacing between etch-a-sketch characters
stdscr = curses.initscr() #Initialization for the curses import
curses.noecho()
curses.cbreak()

position_x=10 #Keeps track of user position during game
position_y=0
xnum = 1 #Used for the etch-a-sketch boundaries
ynum = 1

stdscr.addstr(position_y,position_x,'X') #Used to add 
playGame=True #True until the user quits the game

while playGame:
	c=stdscr.getch() #Get keyboard input
	if c== ord('w'):
		if ynum!=1:
			position_y = position_y - SPACING
			stdscr.addstr(position_y, position_x, "X")
			ynum=ynum-1

	elif c==ord('a'):
		if xnum != 1:
			position_x=position_x-SPACING
			stdscr.addstr(position_y, position_x, "X")
			xnum = xnum-1

	elif c==ord('s'):
		if ynum != GRID_SIZE:
			position_y=position_y+SPACING
			stdscr.addstr(position_y, position_x, "X")
			ynum=ynum+1

	elif c==ord('d'):
		if xnum!=GRID_SIZE:
			position_x=position_x + SPACING
			stdscr.addstr(position_y, position_x, "X")
			xnum=xnum+1

	elif c== ord('q'):
		playGame=False

	elif c== ord('c'):
		stdscr.clear()
		position_x=10
		position_y=0
		xnum=1
		ynum=1
		stdscr.addstr(position_y, position_x, "X")

curses.endwin()
