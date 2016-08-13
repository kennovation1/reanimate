'''
Run the ALSA command aseqdump to print the midi commands to stdout
and then use the following to read the text as stdin and parse it
to catch Note commands and then drive the lamps corresponding to midi notes.

aseqdump -p 14:0 | python -u displaymidi.py # -u is required to prevent stdin buffering
aplaymidi -p 128:0 dialog.mid & timidity dialog.mid

cat dialog.txt | python displaymidi.py # For testing
'''
import sys
import pacdrive
import logging
import time

def mapChanAndNoteToLampId(chan, note):
    ''' Key is note '''
    noteToLampMap = {
            21: 'A1-AC',
            29: 'A2-AC',
            30: 'A3-AC',
            31: 'A4-AC',
            32: 'A5-AB',
            33: 'A5-CD',
            34: 'A6-AB',
            35: 'A6-CD',
            36: 'A7-AB',
            37: 'A7-CD',
            38: 'A8-AB',
            39: 'A8-CD',
            40: 'A9-AB',
            41: 'A9-CD',
            42: 'A10-AB',
            43: 'A10-CD',
            44: 'A11-AB',
            45: 'A11-CD',
            46: 'A12-AB',
            47: 'A12-CD',
            48: 'A13-AB',
            48: 'A13-CD',
            49: 'A14-AB',
            50: 'A14-CD',
            51: 'A15-AB',
            52: 'A15-CD',
            53: 'A16-AB',
            54: 'A16-CD',
            55: 'A17-AC',
            56: 'A18-AB',
            57: 'A18-CD',
            58: 'A19-AB',
            59: 'A19-CD',
            60: 'A20-AB',
            61: 'A20-CD',
            62: 'A21-AB',
            63: 'A21-CD',
            64: 'A22-AB',
            65: 'A22-CD',
            66: 'A23-AC',
            67: 'A24-AC',
            68: 'A25-AC',
            69: 'A26-AC',
            70: 'A27-AC',
            71: 'A28-AC',
            72: 'A29-AC',
            73: 'A30-AC',
            74: 'A31-AC',
            75: 'A32-AC',
            76: 'A33-AC',
            77: 'A34-AC',
            78: 'A35-AC',
            79: 'A36-AC',
            80: 'A9-AB',
            81: 'A9-CD',
            82: 'A10-AB',
            83: 'A10-CD',
            84: 'A11-AB',
            85: 'A11-CD',
            86: 'A12-AB',
            87: 'A12-CD',
            88: 'A13-AB',
            88: 'A13-CD',
            89: 'A14-AB',
            90: 'A14-CD',
            91: 'A15-AB',
            92: 'A15-CD',
            93: 'A16-AB',
            94: 'A16-CD',
            95: 'A17-AC',
            96: 'A18-AB',
            97: 'A18-CD',
            98: 'A19-AB',
            99: 'A19-CD',
            100: 'A20-AB',
            101: 'A20-CD',
            102: 'A21-AB',
            103: 'A21-CD',
            104: 'A22-AB',
            105: 'A22-CD',
            106: 'A23-AC',
            107: 'A24-AC',
            108: 'A25-AC',
            109: 'A26-AC',
            110: 'A27-AC',
            111: 'A28-AC',
            112: 'A29-AC',
            113: 'A30-AC',
            114: 'A31-AC',
            115: 'A32-AC',
            116: 'A33-AC',
            117: 'A34-AC',
            118: 'A35-AC',
            119: 'A36-AC',
            120: 'A5-AB',
            121: 'A5-CD',
            122: 'A6-AB',
            123: 'A6-CD',
            124: 'A7-AB',
            125: 'A7-CD',
            126: 'A8-AB',
            127: 'A8-CD'
        }
    return noteToLampMap[note]
 
def displayNote(chan, note, state):
    # print '{} {} {}'.format(state, chan, note)
    lampId = mapChanAndNoteToLampId(chan, note)
    print chan, note, lampId
    (board, pin) = pacdrive.mapLabelToBoardAndPin(lampId)
    pd.updatePin(board, pin, state)


########
# MAIN #
########
logFormat = '%(levelname)s:%(asctime)s:PACDRIVE:%(module)s-%(lineno)d: %(message)s'
logLevel = logging.INFO
logging.basicConfig(format=logFormat, level=logLevel)

pd = pacdrive.PacDrive(dryRun=False)
pd.initializeAllPacDrives()

#f = sys.stdin
#f = open('dialog.txt') # For testing
# for line in f:
while True:
    line = sys.stdin.readline()
    if line[8:12] == 'Note':
        if line[13:16] == 'off':
            state = False
        else:
            state = True
        chan = line[32:33]
        note = int(line[40:43].split(',')[0])
        displayNote(chan, note, state)
        # time.sleep(0.1) # For debugging only
