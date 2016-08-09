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
from panel_config import actionMap
import json

# TODO KLR: These are for lamps. Move or keep?
import pacdrive
import logging

# TODO KLR: Move this elsewhere...
def mometaryLamp(lampId, state):
    print 'LAMP momentary: lamp={} state={}'.format(lampId, state)
    (board, pin) = pacdrive.mapLabelToBoardAndPin(lampId)
    pd.updatePin(board, pin, state)
    # TODO KLR: pd is global for the moment

def toggleLamp(lampId):
    print 'LAMP toggle: {}'.format(lampId)
    (board, pin) = pacdrive.mapLabelToBoardAndPin(lampId)
    pd.updatePin(board, pin, True)
    # TODO KLR: pd is global for the moment


class PanelController:
    def __init__(self):
        self.lastState = None
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
        for switch in ['A3','A4','S1','S2','S3']:
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
        if self.lastState is not None:
            for switch in self.digitalState.keys():
                if self.digitalState[switch] != self.lastState[switch]:
                    self.edges[switch] = self.digitalState[switch]
        self.lastState = copy.copy(self.digitalState)

    def doActions(self):
        '''
        For each edge on a digital swtich, take an appropriate action.
        Action should return immediately or spawn an asynchronous activity.
        For each analog input (not switches), execute an appropriate update action.
        '''
        for switch in self.edges.keys():
            print 'Action for switch={} pressedNotRelease={} action={}'.format(switch,
                    self.edges[switch], json.dumps(actionMap[switch]))
            actionDetails = actionMap[switch]
            action = actionDetails['action']
            if action == 'toggleLamp':
                toggleLamp(actionDetails['lampId'])
            elif action == 'momentaryLamp':
                mometaryLamp(actionDetails['lampId'], self.edges[switch])

########
# MAIN #
########

logFormat = '%(levelname)s:%(asctime)s:PACDRIVE:%(module)s-%(lineno)d: %(message)s'
logLevel = logging.INFO
logging.basicConfig(format=logFormat, level=logLevel)

# TODO KLR: I'm not sure this should be here directly. Move?
pd = pacdrive.PacDrive(dryRun=False)
pd.initializeAllPacDrives()

delay = 0
panel = PanelController()

# Assumes that S1 key switch is in the off state when program is started
while True:
    panel.getDigitalState()
    panel.getAnalogState()
    panel.detectEdges()
    panel.doActions()

    if delay > 0:
        time.sleep(delay)
