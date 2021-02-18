# Thermometer with Oled Display SSD1306
from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
import framebuf
import utime

WIDTH  = 128                                            # oled display width
HEIGHT = 32                                             # oled display height

i2c = I2C(0, scl=Pin(9), sda=Pin(8))                    # Init I2C using I2C0 defaults, SCL=Pin(GP9), SDA=Pin(GP8)
print("I2C Address      : "+hex(i2c.scan()[0]).upper()) # Display device address
print("I2C Configuration: "+str(i2c))                   # Display I2C config

oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)                  # Init oled display

# Thermometer logo as 32x32 bytearray
buffer = bytearray(b"\x00\x03\xc0\x00\x00\x07\xe0\x00\x00\x0e\x70\x00\x00\x0c\x30\x00\x00\x0c\x30\x00\x00\x0c\x30\x00\x00\x0c\x30\x00\x00\x0c\x30\x00\x00\x0c\x30\x00\x00\x0c\x30\x00\x00\x0c\x30\x00\x00\x0c\x30\x00\x00\x0d\xb0\x00\x00\x0d\xb0\x00\x00\x0d\xb0\x00\x00\x0d\xb0\x00\x00\x0d\xb0\x00\x00\x0d\xb0\x00\x00\x0d\xb0\x00\x00\x0d\xb0\x00\x00\x0d\xb0\x00\x00\x0d\xb0\x00\x00\x1d\xb8\x00\x00\x1b\xd8\x00\x00\x37\xec\x00\x00\x37\xec\x00\x00\x37\xec\x00\x00\x33\xcc\x00\x00\x19\x98\x00\x00\x1c\x38\x00\x00\x0f\xf0\x00\x00\x03\xc0\x00")

# Load the thermometer logo into the framebuffer (the image is 32x32)
fb = framebuf.FrameBuffer(buffer, 32, 32, framebuf.MONO_HLSB)

# Init internal temperature sensor
sensor_temp = ADC(4)

# Define the conversion factor
conversion_factor = 3.3 / (65535)

while True:

    # Read temperature from sensor
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706) / 0.001721

    # Clear the oled display in case it has junk on it.
    oled.fill(0)

    # Blit the image from the framebuffer to the oled display
    oled.blit(fb, 96, 0)

    # Add text with temperature
    oled.text(" This Room",5,2)
    oled.text("Temperature",5,13)
    oled.text("  is " + str(int(temperature)) +  " C",5,25)

    # Update the oled display so the image & text is displayed
    oled.show()

    # Sleep 2 seconds before measure again
    utime.sleep(2)
