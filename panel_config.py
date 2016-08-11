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

# Handy groups
analogSwitches = ['A3','A4','S1','S2','S3']
potentiometers = ['R1', 'R2', 'R3', 'R4']
statusLamps = [
            'A10-AB',
            'A10-CD',
            'A11-AB',
            'A11-CD',
            'A12-AB',
            'A12-CD',
            'A13-AB',
            'A13-CD',
            'A14-AB',
            'A14-CD',
            'A15-AB',
            'A15-CD',
            'A16-AB',
            'A16-CD',
            'A17-AC',
            'A18-AB',
            'A18-CD',
            'A19-AB',
            'A19-CD',
            'A20-AB',
            'A20-CD',
            'A21-AB',
            'A21-CD'
            ]

'''
Define the actions to take when a button is pressed or released
'''
actionMap = {
        'S1': {"press_action": {"function": "setLamps", "offLamps": [], "onLamps": ["A2-AC"]},
               "release_action": {"function": "setLamps", "offLamps": ["A2-AC"], "onLamps": []}},
        'S2': {"press_action": {"function": "setLamps", "offLamps": [], "onLamps": ["A1-AC"]}, 
               "release_action": {"function": "setLamps", "offLamps": ["A1-AC"], "onLamps": []}},
        'S3': {"press_action": {"function": "setLamps", "offLamps": [], "onLamps": ["DS1-Negative"]}, 
               "release_action": {"function": "setLamps", "offLamps": ["DS1-Negative"], "onLamps": []}},
        'A1': {"press_action": {"function": "setLamps", "offLamps": [], "onLamps": ["A1-AC"]}, 
               "release_action": {"function": "setLamps", "offLamps": ["A1-AC"], "onLamps": []}},
        'A2': {"press_action": {"function": "setLamps", "offLamps": [], "onLamps": ["A2-AC"]}, 
               "release_action": {"function": "setLamps", "offLamps": ["A2-AC"], "onLamps": []}},
        'A3': {"press_action": {"function": "setLamps", "offLamps": [], "onLamps": ["A3-AC"]}, 
               "release_action": {"function": "setLamps", "offLamps": ["A3-AC"], "onLamps": []}},
        'A4': {"press_action": {"function": "setLamps", "offLamps": [], "onLamps": ["A4-AC"]}, 
               "release_action": {"function": "setLamps", "offLamps": ["A4-AC"], "onLamps": []}},
        'A5': {"press_action": {"function": "setLamps", "offLamps": ["A5-CD"], "onLamps": ["A5-AB"]}, 
               "release_action": {"function": "setLamps", "offLamps": ["A5-AB"], "onLamps": ["A5-CD"]}},
        'A6': {"press_action": {"function": "setLamps", "offLamps": [], "onLamps": ["A6-AB"]}, 
               "release_action": {"function": "setLamps", "offLamps": ["A6-AB"], "onLamps": ["A6-CD"]}},
        'A7': {"press_action": {"function": "setLamps", "offLamps": ["A6-CD"], "onLamps": ["A7-AB"]}, 
               "release_action": {"function": "setLamps", "offLamps": ["A7-AB"], "onLamps": ["A7-CD"]}},
        'A8': {"press_action": {"function": "setLamps", "offLamps": ["A7-CD"], "onLamps": ["A8-AB"]}, 
               "release_action": {"function": "setLamps", "offLamps": ["A8-AB"], "onLamps": ["A8-CD"]}},
        'A9': {"press_action": {"function": "setLamps", "offLamps": ["A9-CD"], "onLamps": ["A9-AB"]}, 
               "release_action": {"function": "setLamps", "offLamps": ["A9-AB"], "onLamps": ["A9-CD"]}},
        'A22': {"press_action": {"function": "setLamps", "offLamps": ["A22-CD"], "onLamps": ["A22-AB"]}, 
               "release_action": {"function": "setLamps", "offLamps": ["A22-AB"], "onLamps": ["A22-CD"]}},
        'A23': {"press_action": {"function": "setLamps", "offLamps": [], "onLamps": ["A23-AC"]}, 
               "release_action": {"function": "setLamps", "offLamps": ["A23-AC"], "onLamps": []}},
        'A24': {"press_action": {"function": "setLamps", "offLamps": [], "onLamps": ["A24-AC"]}, 
               "release_action": {"function": "setLamps", "offLamps": ["A24-AC"], "onLamps": []}},
        'A25': {"press_action": {"function": "setLamps", "offLamps": [], "onLamps": ["A25-AC"]}, 
               "release_action": {"function": "setLamps", "offLamps": ["A25-AC"], "onLamps": []}},
        'A26': {"press_action": {"function": "setLamps", "offLamps": [], "onLamps": ["A26-AC"]}, 
               "release_action": {"function": "setLamps", "offLamps": ["A26-AC"], "onLamps": []}},
        'A27': {"press_action": {"function": "setLamps", "offLamps": [], "onLamps": ["A27-AC"]}, 
               "release_action": {"function": "setLamps", "offLamps": ["A27-AC"], "onLamps": []}},
        'A28': {"press_action": {"function": "setLamps", "offLamps": [], "onLamps": ["A28-AC"]}, 
               "release_action": {"function": "setLamps", "offLamps": ["A28-AC"], "onLamps": []}},
        'A29': {"press_action": {"function": "setLamps", "offLamps": [], "onLamps": ["A29-AC"]}, 
               "release_action": {"function": "setLamps", "offLamps": ["A29-AC"], "onLamps": []}},
        'A30': {"press_action": {"function": "setLamps", "offLamps": [], "onLamps": ["A30-AC"]}, 
               "release_action": {"function": "setLamps", "offLamps": ["A30-AC"], "onLamps": []}},
        'A31': {"press_action": {"function": "setLamps", "offLamps": [], "onLamps": ["A31-AC"]}, 
               "release_action": {"function": "setLamps", "offLamps": ["A31-AC"], "onLamps": []}},
        'A32': {"press_action": {"function": "setLamps", "offLamps": [], "onLamps": ["A32-AC"]}, 
               "release_action": {"function": "setLamps", "offLamps": ["A32-AC"], "onLamps": []}},
        'A33': {"press_action": {"function": "setLamps", "offLamps": [], "onLamps": ["A33-AC"]}, 
               "release_action": {"function": "setLamps", "offLamps": ["A33-AC"], "onLamps": []}},
        'A34': {"press_action": {"function": "setLamps", "offLamps": [], "onLamps": ["A34-AC"]}, 
               "release_action": {"function": "setLamps", "offLamps": ["A34-AC"], "onLamps": []}},
        'A35': {"press_action": {"function": "setLamps", "offLamps": [], "onLamps": ["A35-AC"]}, 
               "release_action": {"function": "setLamps", "offLamps": ["A35-AC"], "onLamps": []}},
        'A36': {"press_action": {"function": "setLamps", "offLamps": [], "onLamps": ["A36-AC"]}, 
               "release_action": {"function": "setLamps", "offLamps": ["A36-AC"], "onLamps": []}}
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
