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
                 Emergency off is a normally closed switch, but is still reported as press/released like any other
                 (once decoded).
                 The On/Off key switch is a stateful toggle (since it has two stable positions)
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

'''
Define the actions to take when a button is pressed or released
'''
actionMap = {
        'S1': {'action': 'noop'},
        'S2': {'action': 'noop'},
        'S3': {'action': 'noop'},
        'A1': {'action': 'momentaryLamp', 'lampId': 'A1-AC'},
        'A2': {'action': 'momentaryLamp', 'lampId': 'A1-AC'},
        'A3': {'action': 'noop'},
        'A4': {'action': 'noop'},
        'A5': {'action': 'noop'},
        'A6': {'action': 'noop'},
        'A7': {'action': 'noop'},
        'A8': {'action': 'noop'},
        'A9': {'action': 'noop'},
        'A22': {'action': 'noop'},
        'A23': {'action': 'toggleLamp', 'lampId': 'A23-AC'},
        'A24': {'action': 'toggleLamp', 'lampId': 'A24-AC'},
        'A25': {'action': 'toggleLamp', 'lampId': 'A25-AC'},
        'A26': {'action': 'toggleLamp', 'lampId': 'A26-AC'},
        'A27': {'action': 'toggleLamp', 'lampId': 'A27-AC'},
        'A28': {'action': 'toggleLamp', 'lampId': 'A28-AC'},
        'A29': {'action': 'toggleLamp', 'lampId': 'A29-AC'},
        'A30': {'action': 'toggleLamp', 'lampId': 'A30-AC'},
        'A31': {'action': 'toggleLamp', 'lampId': 'A31-AC'},
        'A32': {'action': 'toggleLamp', 'lampId': 'A32-AC'},
        'A33': {'action': 'toggleLamp', 'lampId': 'A33-AC'},
        'A34': {'action': 'toggleLamp', 'lampId': 'A34-AC'},
        'A35': {'action': 'toggleLamp', 'lampId': 'A35-AC'},
        'A36': {'action': 'toggleLamp', 'lampId': 'A36-AC'}
        }

########
# MAIN #
########
if __name__ == '__main__':
    import json

    print 'switchMap:'
    for pin in switchMap.keys():
        print '{}:\t{}'.format(pin, switchMap[pin])

    print '\nanalogMap:'
    for channel in analogMap:
        print '{}:\t{}'.format(channel, analogMap[channel])

    print '\nactionMap:'
    for switch in actionMap:
        print '{}:\t{}'.format(switch, json.dumps(actionMap[switch]))
