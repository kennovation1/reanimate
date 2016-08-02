'''
Fixed display logic...
value is False when key is pressed (since pulled up)

All digital switches work except for A5-A8

Implement ADC for pots and switches

'''
import RPi.GPIO as GPIO
import time

'''
Pairs of GPIO signal #, switch ID
S1, S2, S3, A3, A4 are read via the ADC and SPI interface
A9 and A22 are toggles. The rest are momentary and normally open
Each should be confired with an internal pull up. When switch closes,
the input pin is pulled to ground.
'''
switchMap = {
        2:   'A5',
        3:   'A6',
        4:   'A7',
        5:   'A26',
        6:   'A25',
        7:   'A28',
        12:  'A29',
        13:  'A24',
        14:  'A35',
        15:  'A36',
        16:  'A30',
        17:  'A8',
        18:  'A1',
        19:  'A23',
        20:  'A31',
        21:  'A32',
        22:  'A34',
        23:  'A2',
        24:  'A9',
        25:  'A27',
        26:  'A22',
        27:  'A33'
        }

def initialize():
    ''' Set up GPIO input inputs '''
    GPIO.setmode(GPIO.BCM)

    for pin in switchMap.keys():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        print '{} {}'.format(pin, switchMap[pin])

def getState():
    ''' Read all input pins and return dict where keys are switch IDs and value is state '''
    state = {} # Keys will be swtich ID
    for pin in switchMap.keys():
        value = GPIO.input(pin)
        state[switchMap[pin]] = value
        if value == False:
            print 'Key pressed: {}'.format(switchMap[pin])
    return state

def printState(state):
    for switch in state.keys():
        print '{} {}'.format(switch, state[switch])

def detectEdges(oldState, newState):
    '''
    Returns a dict indexed by swith ID where the values is:
    0 if nothing changes since last poll iteration
    1 for an up edge
    -1 for a down edge
    '''

    edges = {}
    for switch in newState.keys():
        edges[switch] = newState[switch] - oldState[switch]

########
# MAIN #
########
initialize()
oldState = {}

while True:
    newState = getState()
    #diffs = detectEdges(oldState, newState)
    oldState = newState
    time.sleep(0.2)
