import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5557")

ERROR = {'narration': 'Map name does not match save file',
         'inspection': 'Map name does not match save file',
         'biome': '',
         'encounter': 0}

OUTOFBOUNDS = {'narration': 'You only see vast sea where you are trying to go.',
               'inspection': 'You smell salt.'}

NAME = 'test_map'

SCORCHED = {'narration': "The land that surrounds you is scorched. No life could ever live here.",
            'inspection': "you feel as though you are being watched.",
            'biome': 'scorched',
            'encounter': 5}

FIELDS = {'narration': "You stand in a vast field. The ground beneath you is as green as emerald.",
          'inspection': "You only notice the warmth of the sun on your face.",
          'biome': 'fields',
          'encounter': 15}

DESERT = {'narration': "You find yourself in a dry desert. It would take a hearty person to survive these lands.",
          'inspection': "You kick the sand around to find only more sand.",
          'biome': 'desert',
          'encounter': 10}

test_map = [[SCORCHED, SCORCHED, SCORCHED, SCORCHED, SCORCHED, SCORCHED, SCORCHED, SCORCHED],
            [SCORCHED, DESERT, FIELDS, FIELDS, FIELDS, FIELDS, DESERT, SCORCHED],
            [SCORCHED, DESERT, FIELDS, FIELDS, FIELDS, FIELDS, DESERT, SCORCHED],
            [SCORCHED, DESERT, FIELDS, FIELDS, FIELDS, FIELDS, DESERT, SCORCHED],
            [SCORCHED, DESERT, FIELDS, FIELDS, FIELDS, FIELDS, DESERT, SCORCHED],
            [SCORCHED, DESERT, FIELDS, FIELDS, FIELDS, FIELDS, DESERT, SCORCHED],
            [SCORCHED, DESERT, FIELDS, FIELDS, FIELDS, FIELDS, DESERT, SCORCHED],
            [SCORCHED, DESERT, FIELDS, FIELDS, FIELDS, FIELDS, DESERT, SCORCHED],
            [SCORCHED, DESERT, FIELDS, FIELDS, FIELDS, FIELDS, DESERT, SCORCHED],
            [SCORCHED, SCORCHED, SCORCHED, SCORCHED, SCORCHED, SCORCHED, SCORCHED, SCORCHED]
            ]

while True:
    message = socket.recv_json()
    print(message)
    map_name = message['map']
    x, y = message['coords']
    if map_name != NAME:
        socket.send_json({'status': 'error', 'data': ERROR})
    if 0 <= x < len(test_map) and 0 <= y < len(test_map[0]):
        position = test_map[x][y]
        socket.send_json({'status': 'success', 'data': position})
    else:
        socket.send_json({'status': 'out_of_bounds', 'data': OUTOFBOUNDS})
