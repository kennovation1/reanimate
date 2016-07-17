'''
File: testaux.py

Quick and dirty utility to help debug wiring.

Author: Ken Robbins

'''
import pacdrive
import logging
def processUserInput():
    print '''
      Commands:
        q               Quit
        on              Turn all on
        on <pinlist>    Turn on all pins in the comma separated list (no spaces)
        off             Turn all off
        even            Turn on even pins
        odd             Turn on odd pins
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
        else:
            print 'Unknown command'

def handleOnCommand(pinStrs):
    # TODO: Onyl supports board number 1 for now
    if pinStrs and len(pinStrs) > 0:
        board = 1
        for pin in pinStrs:
            pd.updatePin(board, int(pin), True)
    else:
        pd.updatePattern('ALL_ON')

########
# MAIN #
########
if __name__ == '__main__':
    logFormat = '%(levelname)s:%(asctime)s:PACDRIVE:%(module)s-%(lineno)d: %(message)s'
    logLevel = logging.INFO
    logging.basicConfig(format=logFormat, level=logLevel)

    pd = pacdrive.PacDrive(dryRun=True)
    pd.initializeAllPacDrives()

    processUserInput()


