'''
File: pacdrive.py

Utility to control an Ultimarc PacDrive.

This is not written for general use, but can readily be modified.
At present, this is focused on my Auxiliary Control Panel project.
My use case is to control a set of 4 PacDrives on a single USB bus.
The devices were ordered to default to off and to have unique IDs.
This is meant to work on a Raspberry PI 3 model B and is not generalized beyond that.

Supports up to 4 boards at present.

Author: Ken Robbins

Thanks to Robert Abram and Katie Snow (Ultimarc-linux) whose source code provided insight into PacDrive
programming and for their #define values for PACDRIVE_*
'''
import usb.core
import usb.util
import unittest
import logging

# USB constants
PACDRIVE_VENDOR = 0xD209
PACDRIVE_PRODUCT = 0x1500
PACDRIVE_MESG_LENGTH = 4
PACDRIVE_VALUE = 0x0200
PACDRIVE_INDEX = 0
PACDRIVE_DATA_SIZE = 4
PACDRIVE_REPORT = 0x03
PACDRIVE_INTERFACE = 0
UM_REQUEST_TYPE = 0x21
UM_REQUEST = 9

# PacDrive characteristics
PACDRIVE_PINS = 16

MAX_BOARDS = 4

class PacDrive:
    def __init__(self, dryRun=True):
        self.dryRun = dryRun
        self.state = []
        for i in range(MAX_BOARDS+1):
            self.state.append([0, 0]) # LSB, MSB. N.B. Boards are numbered from 1. state[0] is unused.

    def getState(self):
        return self.state

    def initializeAllPacDrives(self):
        '''
        Iterate over all USB-attached PacDrives that are found and intialize each
        '''
        self.devs = {}
        if self.dryRun:
            for i in range(1, MAX_BOARDS+1):
                self.devs[i] = 'Dummy device ' + str(i)
	    return

        devsIter = usb.core.find(idVendor=PACDRIVE_VENDOR, idProduct=PACDRIVE_PRODUCT, find_all=True)
        if devsIter is None:
	    raise ValueError('No PacDrive devices found')

        for dev in devsIter: # Can only read this iter once
	    if dev.is_kernel_driver_active(0): # Okay to hardcode 0?
	        dev.detach_kernel_driver(0)
	    dev.set_configuration() # Assumes that the default is the right one
	    self.devs[dev.bcdDevice] = dev

    def updatePin(self, board, pin, state):
        ''' Set a single pin on or off '''
        (lowByte, highByte) = mapPin(pin)
        if state:
            self.state[board][0] |= lowByte 
            self.state[board][1] |= highByte
        else:
            self.state[board][0] &= ~lowByte & 0x0f
            self.state[board][1] &= ~highByte & 0x0f
        self.updatePacDrive(board)

    def updatePattern(self, pattern):
        ''' Set the output state according to a pattern command '''
        if pattern == 'ALL_ON':
            value = 0xff
        elif pattern == 'EVEN_ONLY':
            value = 0xaa
        elif pattern == 'ODD_ONLY':
            value = 0x55
        else: # 'ALL_OFF'
            value = 0x00

        for i in range(len(self.state)):
            self.state[i][0] = value
            self.state[i][1] = value

        # Block the buzzer from being set by this function (must use updatePin)
        self.state[3][1] &= 0x7f
        self.updateAllPacDrives()

    def updateAllPacDrives(self):
        ''' Send update to all attached hardware '''
        for board in self.devs:
            self.updatePacDrive(board)

    def updatePacDrive(self, board):
        ''' Send a command to update the output state of an attached PacDrive '''
        msg = [0x00, 0x00, 0x00, 0x00]
        msg[3] = self.state[board][0] # LSB
        msg[2] = self.state[board][1] # MSB
        if self.dryRun:
            print 'dryRun: 0x%02x 0x%02x' % (msg[2], msg[3])
        else:
            assert self.devs[board].ctrl_transfer(UM_REQUEST_TYPE, UM_REQUEST, PACDRIVE_VALUE, PACDRIVE_INDEX, msg) == PACDRIVE_MESG_LENGTH

# End class PacDrive

# Utility functions:

def mapPin(pin):
    '''
    Set bit to enable provided pin. Pin should be in the range 1-16.
    Returns a tuple (highByte, lowByte)
    '''
    if pin <= 8:
        lowByte = 0x1 << pin-1
        highByte = 0x0
    else:
        lowByte = 0x0
        highByte = 0x1 << pin-9

    return (lowByte, highByte)

def mapLogicalIdToBoardAndPin(logicalId):
    '''
    Maps a logical ID in the range of 1 to 64 to a board ID (1-4)
    and a pin number (1-16)
    Returns a tuple (boardId, pin)
    '''
    boardId = ((logicalId-1) / PACDRIVE_PINS) + 1
    pin  = ((logicalId-1) % PACDRIVE_PINS) + 1
    return (boardId, pin)

def mapLabelToBoardAndPin(label):
    '''
    Map a text label for a lamp to the board and pin that the is wired to that lamp
    Returns a tuple (boardId, pin)

    Label suffix meaning is the lamps within the labeled switch. (Buzzer is a special case).
    Looking at front of legend switch, the lamps are labeled as:
    A B
    D C

    Therefore, top row is suffix -AB, bottom is -CD, non divided is usually wired with diagnonals
    and therefore with a suffix of -CD.
    '''
    labelMap = {
            'DS1-Negative': (4,16),
            'A1-AC': (2,15),
            'A2-AC': (1,12),
            'A3-AC': (4,7),
            'A4-AC': (4,8),
            'A5-AB': (3,15),
            'A5-CD': (3,16),
            'A6-AB': (4,1),
            'A6-CD': (4,2),
            'A7-AB': (4,3),
            'A7-CD': (4,4),
            'A8-AB': (4,5),
            'A8-CD': (4,6),
            'A9-AB': (1,13),
            'A9-CD': (1,14),
            'A10-AB': (1,1),
            'A10-CD': (2,1),
            'A11-AB': (1,2),
            'A11-CD': (2,2),
            'A12-AB': (1,3),
            'A12-CD': (2,3),
            'A13-AB': (1,4),
            'A13-CD': (2,4),
            'A14-AB': (1,5),
            'A14-CD': (2,5),
            'A15-AB': (1,6),
            'A15-CD': (2,6),
            'A16-AB': (1,7),
            'A16-CD': (2,8),
            'A17-AC': (2,7),
            'A18-AB': (1,8),
            'A18-CD': (2,9),
            'A19-AB': (1,9),
            'A19-CD': (2,10),
            'A20-AB': (1,10),
            'A20-CD': (2,11),
            'A21-AB': (1,11),
            'A21-CD': (2,12),
            'A22-AB': (2,13),
            'A22-CD': (2,14),
            'A23-AC': (3,1),
            'A24-AC': (3,2),
            'A25-AC': (3,3),
            'A26-AC': (3,4),
            'A27-AC': (3,5),
            'A28-AC': (3,6),
            'A29-AC': (3,7),
            'A30-AC': (3,8),
            'A31-AC': (3,9),
            'A32-AC': (3,10),
            'A33-AC': (3,11),
            'A34-AC': (3,12),
            'A35-AC': (3,13),
            'A36-AC': (3,14)
            }
    return labelMap[label]


#############
# unittests #
#############
class TestController(unittest.TestCase):
    def setUp(self):
        self.dryRun = False

    @unittest.skip('Only run this if I change mapPin')
    def test_mapPin(self):
        print '\nTest of mapPin'
        for pin in range(1,17):
            (lowByte, highByte) = mapPin(pin)
            print '%d\t0x%02x\t0x%02x' % (pin, highByte, lowByte)
        # A few tests, but mostly just need to read the output when changing the code
        self.assertEqual(pin, 16, 'Unexpected pin value')
        self.assertEqual(highByte, 0x80, 'Unexpected highByte value')
        self.assertEqual(lowByte, 0x0, 'Unexpected lowByte value')

    @unittest.skip('Only run this if I change mapLogicalIdToBoardAndPin')
    def test_mapLogicalIdToBoardAndPin(self):
        print '\nTest of mapLogicalIdToBoardAndPin'
        # A few tests, but mostly just need to read the output when changing the code
        for logicalId in range(1,65):
            (boardId, pin) = mapLogicalIdToBoardAndPin(logicalId)
            print '%d\t%d\t%d' % (logicalId, boardId, pin)
        self.assertEqual(logicalId, 64, 'Unexpected logicalId value')
        self.assertEqual(boardId, 4, 'Unexpected boardId value')
        self.assertEqual(pin, 16, 'Unexpected pin value')

    @unittest.skip('Only run this if I change mapLabelToBoardAndPin')
    def test_mapLabelToBoardAndPin(self):
        # A few tests, but mostly just need to read the output when changing the code
        print '\nTest of mapLabelToBoardAndPin'
        (boardId, pin) = mapLabelToBoardAndPin('A1')
        print '%s\t%d\t%d' % ('A1', boardId, pin)
        (boardId, pin) = mapLabelToBoardAndPin('A2')
        print '%s\t%d\t%d' % ('A2', boardId, pin)
        self.assertEqual(boardId, 3, 'Unexpected boardId value')
        self.assertEqual(pin, 4, 'Unexpected boardId value')

    def test_initializeAllPacDrives(self):
        pd = PacDrive(dryRun=self.dryRun)
        pd.initializeAllPacDrives()
        self.assertEqual(len(pd.devs), MAX_BOARDS, 'Wrong number of PacDrives found')

        # TODO: Do I need to do this anywhere?
        # for dev in pd.devs:
        #    usb.util.dispose_resources(dev)

    def test_getState(self):
        pd = PacDrive(dryRun=self.dryRun)
        state = pd.getState()
        print 'getState returned:'
        print state
        self.assertEqual(len(state), MAX_BOARDS+1, 'Wrong length for state')

    def test_updatePinSet(self):
        pd = PacDrive(dryRun=self.dryRun)
        pd.initializeAllPacDrives()
        pd.updatePin(4, 16, True)
        state = pd.getState()
        self.assertEqual(state[4][0], 0x00, 'Pin update of LSB wrong')
        self.assertEqual(state[4][1], 0x80, 'Pin update of MSB wrong')

    def test_updatePinClear(self):
        pd = PacDrive(dryRun=self.dryRun)
        pd.initializeAllPacDrives()
        pd.updatePin(1, 1, True)
        state = pd.getState()
        self.assertEqual(state[1][0], 0x01, 'Pin clear prep of LSB wrong')
        self.assertEqual(state[1][1], 0x00, 'Pin clear prep of MSB wrong')
        pd.updatePin(1, 1, False)
        state = pd.getState()
        self.assertEqual(state[1][0], 0x00, 'Pin clear of LSB wrong')
        self.assertEqual(state[1][1], 0x00, 'Pin clear MSB wrong')

    def test_updatePattern(self):
        pd = PacDrive(dryRun=self.dryRun)
        pd.initializeAllPacDrives()
        pd.updatePattern('ODD_ONLY')
        state = pd.getState()
        self.assertEqual(state[4][0], 0x55, 'Pattern update wrong')
        self.assertEqual(state[4][1], 0x55, 'Pattern update wrong')

    def test_updateAllPacDrives(self):
        pd = PacDrive(dryRun=self.dryRun)
        pd.initializeAllPacDrives()
        pd.updateAllPacDrives()
        self.assertTrue(True, 'Visually inspect output to see that all board were updated')

    def test_updatePacDrive(self):
        pd = PacDrive(dryRun=self.dryRun)
        pd.initializeAllPacDrives()
        pd.updatePin(2, 8, True)
        pd.updatePacDrive(2)
        self.assertTrue(True, 'Visually inspect output to see that the board was updated')


########
# MAIN #
########
if __name__ == '__main__':
    logFormat = '%(levelname)s:%(asctime)s:PACDRIVE:%(module)s-%(lineno)d: %(message)s'
    logLevel = logging.INFO
    logging.basicConfig(format=logFormat, level=logLevel)

    unittest.main()

# TODO:
# Create utility to set a pattern, delay and then set another pattern until list of patterns is complete
# and then start over or end.
