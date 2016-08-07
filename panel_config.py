'''
Data structures that define the specific panel configuration
'''

'''
Digial switch map

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

'''
Analog device map
    Channels 1-4 for pots R1-R4. Covers full range from 0-1023 (0-3.3V) with bettern than 0.01V resolution.
    Channel 5 is LAMPTEST/Auxiliary Control. Pressed = 0.0V, open = 3.3V
    Channel 6 is LAMPTEST/Antenna Control. Pressed = 0.0V, open = 3.3V
    Channel 7 is PUSH TO CALL. Pressed = 0.0V, open = 3.3V
    Channel 8 is Emergency Off and Key. These are wired in an R2R ladder to produce the following:
        S1/Key | S2/Emergency | Volts
        -------+--------------+------
        OFF    | Pressed      | 0.0
        OFF    | Not Pressed  | 1.65
        ON     | Pressed      | 1.98
        ON     | Not Pressed  | 2.48

Pairs of channel and device label. Value will contain a raw level.
'''
analogMap = {
        0: 'R1',
        1: 'R2',
        2: 'R3',
        3: 'R4',
        4: 'A3',
        5: 'A4',
        6: 'S3',
        7: 'S1S2'
        }

########
# MAIN #
########
if __name__ == '__main__':
    print 'switchMap:'
    for pin in switchMap.keys():
        print '{}:\t{}'.format(pin, switchMap[pin])

    print '\nanalogMap:'
    for channel in analogMap:
        print '{}:\t{}'.format(channel, analogMap[channel])

