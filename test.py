# importing the module
import screen_brightness_control as sbc

# get current brightness value
print(sbc.get_brightness())

# fade brightness from the current brightness to 50%
sbc.fade_brightness(50)
print(sbc.get_brightness())

# fade the brightness from 25% to 75%
sbc.fade_brightness(75, start=25)
print(sbc.get_brightness())

# fade the brightness from the current
# value to 100% in steps of 10%
sbc.fade_brightness(100, increment=10)
print(sbc.get_brightness())
