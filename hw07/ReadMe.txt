These are the deliverables for homework 7. The important items to look at are "ledBLINK.py", "GPIO_mem_map.c", "gpio_test.c" in the gpio_test folder, and "Homework 7 report".
The "ledBLINK.py" program maps a gpio input to an output and uses interrupts. The "GPIO_mem_map.c" program uses mmap() and maps a gpio input to an output. 
The "gpio_test.c" file is used by the kernel to map a gpio input to an output. "Homework 7 report" is my report on the findings.

// Comments from Prof. Yoder
// Results look good.  The number of cores on your VM shouldn't impact the speed of the Bone.  Something else could have been running while you were doing the python test which delayed python in responding.
// Project page needs updating
// Grade:  9/10