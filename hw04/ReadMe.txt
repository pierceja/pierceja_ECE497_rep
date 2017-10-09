The files to look at for this homework assignment are the beaglebone memory map pdf, GPIO_mem_map, gpioThru, and etch_a_sketch_withgpio.py.

THe beaglebone memory map is for the first homework section and is a system memory map of the AM335x showing things such as the addresses and size for EMIF0 SDRAM and the GPIO registers.

The GPIO_mem_map is a c script the makes use of the mmap function. This script maps to two GPIO registers, GPIO1 and GPIO3. It uses two buttons connected to the GPIO1_25 and GPIO3_20 to control two of the internal LEDs on the beagleboard

The gpioThru script was modified to read from a switch connected to GPIO1_25 and use it to control an internal LED.

The etch_a_sketch_withgpio.py uses two rotary encoders connected to ports 2 and 3 to control the etch a sketch program. Directions on how to use the etch a sketch are printed to the terminal when you run the script. 

# Comments from Prof. Yoder
# Found your memory map file, nice diagram.
# Looks good.
# Grade:  10/10