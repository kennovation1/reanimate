'''
Operate the Auxiliary Control panel.

In a continuous loop, read all switches and analog inputs and
take action on each input. A common action will be to toggle the
state of the corresponding switch. However, a list of Python function may be assigned
to any input.
'''
import digital_in
import analog_in
#import digital_out
import time

class PanelController:
    def __init__(self):
        self.oldState = {}
        self.currentState = {}
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

    def detectEdges(self):
        '''
        Compare the current switch state to the previous and create a list of
        edge transitions (button pressed or released).

        Returns a dictionary of switch labels and edges.
        '''
        print 'DETECT EDGES'

        '''
        Returns a dict indexed by swith ID where the values is:
        0 if nothing changes since last poll iteration
        1 for an up edge
        -1 for a down edge
        edges = {}
        for switch in newState.keys():
            edges[switch] = newState[switch] - oldState[switch]
        '''

    def doActions(self):
        '''
        For each edge on a digital swtich, take an appropriate action.
        Action should return immediately or spawn an asynchronous activity.
        For each analog input (not switches), execute an appropriate update action.
        '''
        print 'DO ACTIONS'

########
# MAIN #
########

delay = 0.1
panel = PanelController()

while True:
    panel.getDigitalState()
    panel.getAnalogState()
    panel.detectEdges()
    panel.doActions()

    if delay > 0:
        time.sleep(delay)
