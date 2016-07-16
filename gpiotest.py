# Run this as root...
# sudo python gpiotest.py

import gpio
import time
import logging

logger = logging.getLogger()
logger.setLevel(logging.WARNING)

gpio.setup(2, gpio.IN)
gpio.setup(3, gpio.OUT, initial=gpio.LOW)
gpio.setup(4, gpio.OUT, initial=gpio.LOW)
val = gpio.read(2) # To read value from gpio 2
gpio.set(3, 1) # To write 1 to gpio 3
gpio.set(4, 0) # To write 0 to gpio 4

print 'Enter gpio pin to use as input: '
inraw = raw_input()
inpin = int(inraw)
print 'Reading forever, everyone 0.5 seconds...'

gpio.setup(inpin, gpio.IN)

while False:
    value = gpio.read(inpin)
    print value
    time.sleep(0.5)

