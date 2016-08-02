import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

pin = 22
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

i = 0
while True:
    input_state = GPIO.input(pin)
    if input_state == False:
        print('1 Pressed ' + str(i))
    else:
        print('0 Released ' + str(i))
    i += 1
    time.sleep(0.2)
