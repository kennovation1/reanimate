'''
Data structures that define the specific panel configuration
'''

'''
Pairs of GPIO signal #, switch ID label

S1, S2, S3, A3, A4 are read via the ADC and SPI interface and not here.
A9 and A22 are toggles. The rest are momentary and normally open.

Each should be configured with an internal pull up. When switch closes,
the input pin is pulled to ground. Therefore, when reading the GPIO
True represents the unpressed state and False represents a pressed state.
'''
switchMap = {
        2:   'A5',
        3:   'A6',
        4:   'A7',
        5:   'A26',
        6:   'A25',
        7:   'A28',
        12:  'A29',
        13:  'A24',
        14:  'A35',
        15:  'A36',
        16:  'A30',
        17:  'A8',
        18:  'A1',
        19:  'A23',
        20:  'A31',
        21:  'A32',
        22:  'A34',
        23:  'A2',
        24:  'A9',
        25:  'A27',
        26:  'A22',
        27:  'A33'
        }

########
# MAIN #
########
if __name__ == '__main__':
    print 'switchMap:'
    for pin in switchMap.keys():
        print '{}:\t{}'.format(pin, switchMap[pin])
