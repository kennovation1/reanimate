import spidev
import time
import os

'''
sudo raspi-config
    In advanced settings, enable SPI

    ls -l /dev/spidev* to see if it worked

TESTING:
    Channels 1-4 for pots 1-4 work and read 0-3.3v with easily 0.01V resolution
    Channel 5 is Auxiliary Control LAMPTEST. Pressed = 0.0V, open = 3.3V
    Channel 6 is Antenna Control LAMPTEST. Press = 0.0V, open = 3.3V
    Channel 7 is PUSH TO CALL. Press = 0.0V, open = 3.3V
    Channel 8 is Emergency Off and Key.
        S1/Key | S2/Emergency | Volts
        -------+--------------+------
        off    | Pressed      | 0.0
        off    | Not Pressed  | 1.65
        on     | Pressed      | 1.98
        on     | Not Pressed  | 2.48
'''

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
 
# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
 
# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def ConvertVolts(data,places):
  volts = (data * 3.3) / float(1023)
  volts = round(volts,places)
  return volts

# Define delay between readings
delay = 0.1
 
while True:
    for channel in range(8):
        level = ReadChannel(channel)
        volts = ConvertVolts(level, 2)
 
        print str(level) + '\t',
        #print str(volts) + '\t',
        #print '{}\t{}\t{}'.format(channel, level, volts)
       
    print ''
    time.sleep(delay)
