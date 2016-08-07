'''
Read the state of all switches that are connected to RPi GPIO digital inputs.
'''
import RPi.GPIO as GPIO
from panel_config import switchMap

class digitalIn:
    def __init__(self):
        ''' Set up GPIO input inputs '''
        GPIO.setmode(GPIO.BCM)

        for pin in switchMap.keys():
            if pin in [2,3]: # Pins 2 and 3 have physical pull-ups. Skip adding one to avoid warning.
                GPIO.setup(pin, GPIO.IN)
            else:
                GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def getState(self):
        '''
        Read all input pins and return dict where keys are switch IDs and value is state.
        Set polarity so that state is True when a key is pressed and False when not.
        '''
        state = {} # Keys will be swtich ID
        for pin in switchMap.keys():
            value = GPIO.input(pin)
            state[switchMap[pin]] = not value
        return state

    def printState(self, state):
        print 'DIGITAL INPUT SWITCH STATE:'
        for switch in state.keys():
            print '{} {}'.format(switch, state[switch])

########
# MAIN #
########
if __name__ == '__main__':
    dig = digitalIn()
    state = dig.getState()
    dig.printState(state)
