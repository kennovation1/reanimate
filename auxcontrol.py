'''
Operate the Auxiliary Control panel.

In a continuous loop, read all switches and analog inputs and
take action on each input. A common action will be to toggle the
state of the corresponding switch. However, a list of Python function may be assigned
to any input.
'''
import digital_in
import analog_in
import time
import copy
from panel_config import actionMap, potentiometers, analogSwitches, statusLamps, dcPowerMonitorLamps
import json
from signal import *
import sys

# TODO KLR: These are for lamps. Move or keep?
import pacdrive
import logging

# TODO KLR: Move this elsewhere...
def setLamps(switch, action):
    ''' Turn off the list of offLmaps and then turn on the list of onLamps '''
    for lampId in action['offLamps']:
        (board, pin) = pacdrive.mapLabelToBoardAndPin(lampId)
        pd.updatePin(board, pin, False)
    for lampId in action['onLamps']:
        (board, pin) = pacdrive.mapLabelToBoardAndPin(lampId)
        pd.updatePin(board, pin, True)
    # TODO KLR: pd is global for the moment

def toggleLamps(switch, action):
    ''' Toggle the state of each lamp in the lamps list '''
    for lampId in action['lamps']:
        (board, pin) = pacdrive.mapLabelToBoardAndPin(lampId)
        state = not pd.getLampState(board, pin)
        pd.updatePin(board, pin, state)
    # TODO KLR: pd is global for the moment


class PanelController:
    def __init__(self):
        self.lastPrint = 0
        self.lastDigitalState = None
        self.lastAnalogState = None
        self.digitalState = {}
        self.analogState = {}
        self.edges = {}
        self.digitalIn = digital_in.digitalIn()
        self.analogIn = analog_in.analogIn()

    def getDigitalState(self):
        ''' Read the state of all switches that are connected to RPi GPIO digital inputs '''
        self.digitalState = self.digitalIn.getState()

    def getAnalogState(self):
        '''
        Read the state of all analog inputs that are connected to the RPi SPI from the ADC.
        For the analog inputs that are really digital switches, normalize these to look like digital switches.
        '''
        self.analogState = self.analogIn.getState()

        # Copy the analog switch states to the digital state dict
        for switch in analogSwitches:
            self.digitalState[switch] = self.analogState[switch]

    def detectEdges(self):
        '''
        Compare the current switch state to the previous and create a list of
        edge transitions (button pressed or released).

        Returns a dict indexed by switch ID where the values is:
            True for an up edge (pressed)
            False for a down edge (released)
        '''
        self.edges = {}
        if self.lastDigitalState is not None:
            for switch in self.digitalState.keys():
                if self.digitalState[switch] != self.lastDigitalState[switch]:
                    self.edges[switch] = self.digitalState[switch]
        self.lastDigitalState = copy.copy(self.digitalState)

    def doPotAction(self, pot, current, delta):
        '''
        Just a crude function to show that pots can affect something.
        For the given pot, first turn off all assoiciate lamps and then
        turn on the number of lamps in its list proportional to the pot value.
        '''
        lampMap = {
                'R1': ['off', 'A10-AB', 'A10-CD', 'A11-AB', 'A11-CD'],
                'R2': ['off', 'A12-AB', 'A12-CD', 'A13-AB', 'A13-CD'],
                'R3': ['off', 'A14-AB', 'A14-CD', 'A15-AB', 'A15-CD'],
                'R4': ['off', 'A16-AB', 'A16-CD', 'A17-AC']
                }
        for lampId in lampMap[pot]:
            if lampId != 'off':
                setLampById(lampId, False)

        lamps = len(lampMap[pot])
        bandSize = 1024/lamps
        maxLamp = current/bandSize
        if maxLamp >= lamps:
            maxLamp = lamps - 1

        for lampIdIndex in range(maxLamp+1):
            lampId = lampMap[pot][lampIdIndex]
            if lampId != 'off':
                setLampById(lampId, True)

    def handleAnalogStateChanges(self):
        '''
        If an analog value has changed by more than thresh, print the potentiometer ID and the new value.
        There are some issues with noise which may relate to how fast the ADC is sampled.
        For now, apply a threshold to filter some and only print at a certain frequency. This is just
        a debug function. When we have a real purpose, we may need to apply a moving window average or something
        else.

        This was originally just a print function. Now called a handler each time something is printed.
        '''
        interval = 0.1
        now = time.clock()
        if now - self.lastPrint > interval:
            threshold = 5
            if self.lastAnalogState is not None:
                for pot in potentiometers:
                    current = self.analogState[pot]
                    last = self.lastAnalogState[pot]
                    if abs(current - last) > threshold:
                        print '{}: {} ({})'.format(pot, current, current-last)
                        self.doPotAction(pot, current, current-last)
            self.lastAnalogState = copy.copy(self.analogState)
            self.lastPrint = now

    def doActions(self):
        '''
        For each edge on a digital swtich, take an appropriate action.
        Action should return immediately or spawn an asynchronous activity.
        For each analog input (not switches), execute an appropriate update action.
        '''
        for switch in self.edges.keys():
            print 'Action for switch={} pressedNotRelease={} action={}'.format(switch,
                    self.edges[switch], json.dumps(actionMap[switch]))

            if self.edges[switch]:
                actionType = 'press_action'
            else:
                actionType = 'release_action'

            actionDetails = actionMap[switch]
            action = actionDetails[actionType]
            actionFunction = action['function']
            if actionFunction == 'setLamps':
                setLamps(switch, action)
            elif actionFunction == 'toggleLamps':
                toggleLamps(switch, action)
            else:
                pass

def setLampById(lampId, state):
    ''' TODO KLR: Put this elsewhere and refactor calls to mapLabel... '''
    (board, pin) = pacdrive.mapLabelToBoardAndPin(lampId)
    pd.updatePin(board, pin, state)

def cleanExit(*args):
    pd.updatePattern('ALL_OFF')
    print 'Exiting on signal'
    sys.exit(0)


########
# MAIN #
########
logFormat = '%(levelname)s:%(asctime)s:PACDRIVE:%(module)s-%(lineno)d: %(message)s'
logLevel = logging.INFO
logging.basicConfig(format=logFormat, level=logLevel)

# TODO KLR: I'm not sure this should be here directly. Move?
pd = pacdrive.PacDrive(dryRun=False)
pd.initializeAllPacDrives()

for sig in (SIGABRT, SIGINT, SIGQUIT, SIGTERM):
    signal(sig, cleanExit)

delay = 0
panel = PanelController()
for lampId in dcPowerMonitorLamps:
    setLampById(lampId, True)

setLampById('A1-AC', True)

# A9 and A22 are stateful toggle switches
setLampById('A9-CD', True)
setLampById('A22-AB', True)
setLampById('A23-AC', True)
setLampById('A28-AC', True)
setLampById('A33-AC', True)

setLampById('A5-AB', True)
setLampById('A6-AB', True)
setLampById('A7-AB', True)
setLampById('A8-AB', True)

# Assumes that S1 key switch is in the off state when program is started
while True:
    panel.getDigitalState()
    panel.getAnalogState()
    panel.handleAnalogStateChanges()
    panel.detectEdges()
    panel.doActions()

    if delay > 0:
        time.sleep(delay)
