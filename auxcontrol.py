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
                    self.edges[switch], actionMap[switch])

########
# MAIN #
########

delay = 0.1
panel = PanelController()

# TODO KLR: Set initial lamps based on absolute state. In particular, set on and off base on key switch.

while True:
    panel.getDigitalState()
    panel.getAnalogState()
    panel.detectEdges()
    panel.doActions()

    if delay > 0:
        time.sleep(delay)
