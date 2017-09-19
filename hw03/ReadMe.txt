The homework files for this assignment are "temp_read.sh", "tempLimitSetup.sh", 
"alertInterrupt.py", "tmp006_read.sh" and "etch_a_sketch_withgpio.py"

The "temp_read.sh" file reads the temperature sensors at address 0x48
and 0x49 (these addresses come from how I wired the address pins for each
sensor) and converts the temperature to Fahrenheit.

The "tempLimitSetup.sh" file configures Thigh and Tlow of each temperature
sensor. This file goes with "alertInterrupt.py" and should be run before
this python program is run.

The "alertInterrupt.py" program waits for interrupts caused by the alert pins
on the temperature sensors and prints out the temperature currently being read
by whichever sensor caused the interrupt. The alert pins are hooked up to GP06
and GPO4. More details are shown in the python script. 

The "tmp006_read.sh" simply reads the temperature and voltage value from the
tmp006 sensor and prints them out.

The "etch_a_sketch_withgpio.py" program interfaces the etch_a_sketch code with
the LED display. I demoed this in classes, but have added a few things since.
Added after the demo:
The users current position on the display is yellow now to keep track of where
they are. The Mode button on the beaglebone clears the display while the Pause
button quits the program.
