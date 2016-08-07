'''
Read the state of all analog inputs that are connected to the RPi SPI from the ADC.

Must enable SPI first as follows:
    sudo raspi-config
        In advanced settings, enable SPI
'''
import spidev
import time
from panel_config import analogMap
from colors import bcolors

class analogIn:
    def __init__(self):
        ''' Open the first SPI bus on the RPi. This is connected to the ADC chip. '''
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
 
    def readChannel(self, channel):
        '''
        Read data from a single ADC channel from the MCP3008 chip
        Channel must be an integer 0-7.
        Data is a 10-bit integer.
        '''
        adc = self.spi.xfer2([1,(8+channel)<<4,0])
        data = ((adc[1]&3) << 8) + adc[2]
        return data
 
    def getState(self):
        '''
        Read the raw analog values from each ADC channel
        '''
        state = {}
        for channel in analogMap.keys():
            level = self.readChannel(channel)
            state[analogMap[channel]] = level

        self.convertAnalogSwitchStates(state)
        return state

    def convertAnalogSwitchStates(self, state):
        '''
        Convert analog switch values to digital state.
        There is some hard coding here, but that's okay.

        Manipulates input state dict in place.
        '''
        # Level is 0 when pressed, 1023 when not pressed
        maxLevel = 1024
        for key in ['A3', 'A4', 'S3']:
            if state[key] >= maxLevel/2:
                state[key] = False
            else:
                state[key] = True

        # Empirical Break levels are about 0, 510, 614, 768
        step1 = 250
        step2 = 560
        step3 = 700
        level = state['S1S2']
        if level < step1:
            state['S1'] = False
            state['S2'] = True
        elif level >= step1 and level < step2:
            state['S1'] = False
            state['S2'] = False
        elif level >= step2 and level < step3:
            state['S1'] = True
            state['S2'] = True
        elif level >= step3:
            state['S1'] = True
            state['S2'] = False
        del(state['S1S2'])

    def convertVolts(data, places):
        '''
        Convert raw level value to a voltage.
        Assumes that the analog reference voltage is 3.3V
        Round the the specified number of decimal places.
        '''
        arefVoltage = 3.3
        maxRawLevel = 1023 # Max value for a 10-bit converter
        volts = (data * arefVoltage) / float(maxRawLevel)
        volts = round(volts, places)
        return volts

    def printState(self, state):
        line = ''
        for device in ['R1','R2','R3','R4']:
            line += '{}={}\t'.format(device, state[device])
        line += '\t'
        for device in ['S1','S2','S3','A3','A4']:
            if state[device]:
                st = bcolors.BOLD + bcolors.FAIL + 'PRESSED   ' + bcolors.ENDC
            else:
                st = 'notpressed'
            line += '{}={}\t'.format(device, st)
        print line

########
# MAIN #
########
if __name__ == '__main__':
    analog = analogIn()

    delay = 0.1 # Delay between readings

    while(True):
        state = analog.getState()
        analog.printState(state)
        time.sleep(delay)
