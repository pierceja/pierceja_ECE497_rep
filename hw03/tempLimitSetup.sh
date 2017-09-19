#Set the Thigh and Tlow values of each device
`i2cset -y 1 0x48 0x03 0x19`
`i2cset -y 1 0x48 0x02 0x18`
`i2cset -y 1 0x49 0x03 0x1a`
`i2cset -y 1 0x49 0x02 0x19`

#Set POL bit value to 1 to make the alert pin active high
`i2cset -y 1 0x48 0x01 0x84`
`i2cset -y 1 0x49 0x01 0x84`

#Convert each value to Fahrenheit
Thigh1=$(($((`i2cget -y 1 0x48 0x03`))*9/5+32))
Thigh2=$(($((`i2cget -y 1 0x49 0x03`))*9/5+32))
Tlow1=$(($((`i2cget -y 1 0x48 0x02`))*9/5+32))
Tlow2=$(($((`i2cget -y 1 0x49 0x02`))*9/5+32))

echo "Thigh for TMP101 at 0x48 is" $Thigh1 "F"
echo "Tlow for TMP101 at 0x48 is" $Tlow1 "F"
echo "Thigh for TMP101 at 0x49 is" $Thigh2 "F"
echo "Tlow for TMP101 at 0x49 is" $Tlow2 "F"
