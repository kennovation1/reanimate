'''
File: testaux.py

Quick and dirty utility to help debug wiring.

Author: Ken Robbins

'''
import pacdrive
import logging
import time
import random

# TODO: Onyl supports board number 1 for now
PinList = [1,2,4,5,6,7,8,9,10,11,12,13,14] # Current list of functioning lamps
# 3 is NC at the moment
# 15,16 are NC

Board = 1

def processUserInput():
    print '''
      Commands:
        q               Quit
        on              Turn all on
        on <pinlist>    Turn on all pins in the comma separated list (no spaces)
        board <board>   Set active board (for 'on' command)
        off             Turn all off
        even            Turn on even pins
        odd             Turn on odd pins
        chase           Rotate lamps
        rand            Random pattern
    '''
    while True:
        line = raw_input()
        cleanLine = line.rstrip(' \r\n\t')
        if len(cleanLine) == 0:
            continue

        parts = line.split(None, 2)
        command = parts[0]
        print 'Command: %s' % (command)
        if len(parts) == 2: # Assume a comma-separated list of pins
            pinStrs = parts[1].split(',')
        else:
            pinStrs = None

        if command == 'q':
            print 'Quitting'
            break
        elif command == 'on':
            handleOnCommand(pinStrs)
        elif command == 'off':
            pd.updatePattern('ALL_OFF')
        elif command == 'even':
            pd.updatePattern('EVEN_ONLY')
        elif command == 'odd':
            pd.updatePattern('ODD_ONLY')
        elif command == 'chase':
            handleChase()
        elif command == 'rand':
            handleRandom()
        elif command == 'board':
            Board = int(pinStrs[0]) # TODO: Fix overloading of pinsStrs var. Check board range.
            print 'Active board now: ' + str(Board)
        else:
            print 'Unknown command'

def handleOnCommand(pinStrs):
    if pinStrs and len(pinStrs) > 0:
        for pin in pinStrs:
            pd.updatePin(Board, int(pin), True)
    else:
        pd.updatePattern('ALL_ON')

def handleRandom():
    lastPin = 1

    for i in range(100):
        pin = random.choice(PinList)
        state = random.choice([True, True, False])
        pd.updatePin(Board, pin, state)
        time.sleep(0.25)
    pd.updatePattern('ALL_ON')
    time.sleep(2)
    pd.updatePattern('ALL_OFF')
    print 'Rand done'

def handleChase():
    lastPin = 1

    for i in range(4):
        for pin in PinList:
            pd.updatePin(Board, lastPin, False)
            pd.updatePin(Board, pin, True)
            lastPin = pin
            time.sleep(0.25)
    pd.updatePin(Board, lastPin, False)
    pd.updatePattern('ALL_ON')
    time.sleep(2)
    pd.updatePattern('ALL_OFF')
    print 'Chase done'

########
# MAIN #
########
if __name__ == '__main__':
    logFormat = '%(levelname)s:%(asctime)s:PACDRIVE:%(module)s-%(lineno)d: %(message)s'
    logLevel = logging.INFO
    logging.basicConfig(format=logFormat, level=logLevel)

    pd = pacdrive.PacDrive(dryRun=False)
    pd.initializeAllPacDrives()

    processUserInput()


