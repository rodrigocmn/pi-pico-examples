from machine import I2C, Pin
# Import the WS_OLED_128X128 class from ssd1327 (This class set the right offset settings for this display)
from ssd1327 import WS_OLED_128X128
# Import the DS3231_I2C class from ds3231_i2c (This is light driver with limited functionalities)
from ds3231_i2c import DS3231_I2C 
import utime

# Set DS I2C ID, SDA, SCL respective pins and uses default frequency (freq=400000)
ds_i2c = I2C(0,sda=Pin(16), scl=Pin(17))
print("RTC I2C Address : " + hex(ds_i2c.scan()[0]).upper()) # Print the I2C device address in the command line
print("RTC I2C Configuration: " + str(ds_i2c))              # Display the basic parameters of I2C device in the command line
ds = DS3231_I2C(ds_i2c)

# Set OLED I2C ID, SDA, SCL respective pins and uses default frequency (freq=400000)
oled_i2c = I2C(1, sda=Pin(10), scl=Pin(11))
print("OLED I2C Address : " + hex(oled_i2c.scan()[0]).upper()) # Print the I2C device address in the command line
print("OLED I2C Configuration: " + str(oled_i2c))              # Display the basic parameters of I2C device in the command line
# Configure an WS_OLED_128X128 instance with automatic addr configuration.
oled = WS_OLED_128X128(oled_i2c, addr=int(hex(oled_i2c.scan()[0])))

# Uncomment the two lines below to set time.
# current_time = b'\x00\x57\x22\x04\x17\x02\x21' # sec min hour week day mout year
# ds.set_time(current_time)

# Define the name of week days list
w  = ["Sunday","Monday","Tuesday","Wednesday","Thurday","Friday","Saturday"];

while 1:
    # Retrun current time
    t = ds.read_time()

    # Clear Display
    oled.fill(0) 
    # Display the string at (x,x) position with 0-15 brightest.
    oled.text("Rod's Connection", 0, 10, 5)
    oled.text("    Strings", 0, 20, 5)
    oled.text("   OLED Clock",  0, 40, 10)
    oled.text("SSD1327 + DS3231",  0, 50, 10)
    oled.text("    Example",  0, 60, 10)
    oled.text("Date: %02x/%02x/20%x" %(t[4],t[5],t[6]), 0, 80, 15)
    oled.text(" Time: %02x:%02x:%02x" %(t[2],t[1],t[0]), 0, 100, 15)
    oled.text("    %s" %(w[t[3]-1]),0, 115, 15)
    # oled.text("Datetime: " + rtc, 0, 50, 10)
        
    oled.show() # Refresh OLED display
    utime.sleep(1)





