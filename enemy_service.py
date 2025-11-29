import zmq
import random

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5558")

enemies = {
        {
            'name': 'Goblin',
            'health': 10,
            'attack': 3,
            'defense': 5,
            'biome': 'fields'
        },
        {
            'name': 'Wolf',
            'health': 12,
            'attack': 4,
            'defense': 3,
            'biome': 'fields'

        },
        {
            'name': 'Scorpion',
            'health': 10,
            'attack': 5,
            'defense': 1,
            'biome': 'desert'
        },
        {
            'name': 'Bandit',
            'health': 18,
            'attack': 6,
            'defense': 5,
            'biome': 'desert'
        },
        {
            'name': 'Giant Spider',
            'health': 20,
            'attack': 7,
            'defense': 4,
            'biome': 'scorched'
        },
        {
            'name': 'Undead',
            'health': 10,
            'attack': 6,
            'defense': 6,
            'biome': 'scorched'
        },
        {
            'name': 'Knight',
            'health': 20,
            'attack': 6,
            'defense': 10,
            'biome': 'scorched'
        },
        {
            'name': 'Vagabond',
            'health': 18,
            'attack': 10,
            'defense': 7,
            'biome': 'scorched'
        }}


while True:
    biome = socket.recv_string()
    possibilities = [enemy for enemy in enemies if enemy['biome'] == biome]
    enemy = random.choice(possibilities)
    socket.send_json(enemy)
