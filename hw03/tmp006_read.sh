#!/bin/bash

#Read the sensor temperature and voltage
temp=`i2cget -y 1 0x40 0x01`
volt=`i2cget -y 1 0x40 0x00`

temp=$((temp*9/5+32))

echo "The detected temperature is" $temp
echo "The sensor voltage is" $volt
