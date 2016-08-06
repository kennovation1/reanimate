'''
File: testaux.py

Quick and dirty utility to help debug wiring.

Author: Ken Robbins

'''
import pacdrive
import logging
import time
import random

PinList = [
        [0],
        [1,2,3,4,5,6,7,8,9,10,11,12,13,14],       # Board 1
        [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],    # Board 2
        [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16], # Board 3
        [1,2,3,4,5,6,7,8]                         # Board 4. Pin 16 is buzzer
    ]

def processUserInput():
    print '''
      Commands:
        q               Quit
        on <pinlist>    Turn on all pins in the comma separated list (no spaces). All on if no args.
        board <board>   Set active board (for 'on' command)
        off <pinlist>   Turn of pins in list. All off if no args.
        even            Turn on even pins
        odd             Turn on odd pins
        chase <boardlist>  Rotate lamps in the specified boards in board list order. 1,2,3,4 if no args.
        rand <boardlist>   Random pattern in the specified boards in board. All boards if no args.
    '''
    board = 1
    while True:
        line = raw_input()
        cleanLine = line.rstrip(' \r\n\t')
        if len(cleanLine) == 0:
            continue

        parts = line.split(None, 2)
        command = parts[0]
        print 'Command: %s' % (command)
        if len(parts) == 2: # Assume a comma-separated list of pins
            args = parts[1].split(',')
        else:
            args = None

        if command == 'q':
            print 'Quitting'
            break
        elif command == 'off':
            handleOnOffCommand(board, args, False)
        elif command == 'on' or command == 'o':
            handleOnOffCommand(board, args, True)
        elif command == 'even':
            pd.updatePattern('EVEN_ONLY')
        elif command == 'odd':
            pd.updatePattern('ODD_ONLY')
        elif command == 'chase':
            handleChase(args)
        elif command == 'rand':
            handleRandom(args)
        elif command == 'board' or command == 'b':
            board = int(args[0])
            print 'Active board now: ' + str(board)
        else:
            print 'Unknown command'

def handleOnOffCommand(board, args, state):
    if args and len(args) > 0:
        for pin in args:
            pd.updatePin(board, int(pin), state)
    else:
        if state:
            pd.updatePattern('ALL_ON')
        else:
            pd.updatePattern('ALL_OFF')

def handleRandom(args):
    lastPin = 1

    if args and len(args) > 0:
        boards = args
    else:
        boards = [1,2,3,4]

    for i in range(100):
        state = random.choice([True, True, False])
        board = int(random.choice(boards))
        pin = random.choice(PinList[board])
        pd.updatePin(board, pin, state)
        time.sleep(0.25)
    pd.updatePattern('ALL_OFF')
    print 'Rand done'

def handleChase(args):
    lastBoard = 1
    lastPin = 1

    if args and len(args) > 0:
        boards = args
    else:
        boards = [1,2,3,4]

    for i in range(4):
        for b in boards:
            board = int(b)
            for pin in PinList[board]:
                pd.updatePin(lastBoard, lastPin, False)
                pd.updatePin(board, pin, True)
                lastBoard = board
                lastPin = pin
                time.sleep(0.25)
    pd.updatePin(lastBoard, lastPin, False)
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


