from tkinter import *
import json


###############
# UI Structure
###############


###############
# Game instance
###############


class Game:
    """A class that holds the logic for running an instance of the game and communicating with microservices."""

    def __init__(self, player):
        """Initialize the game instance, defined by player character save data and other factors."""
        self._player = player


class Player:
    """A class that represents the player character information"""

    def __init__(self, player_data):
        """Initialize the player object by searching for save data"""
        self._name = player_data["name"]
        self._stats = player_data["stats"]
        self._inventory = player_data["inventory"]
        self._position = player_data["position"]

    def get_name(self):
        """Return the name of the player character"""
        return self._name

    def get_health(self):
        """Return the health stat of the player character"""
        return self._stats["health"]

    def get_mana(self):
        """Return the mana stat of the player character"""
        return self._stats["mana"]

    def get_attack(self):
        """Return the attack stat of the player character"""
        return self._stats["attack"]

    def get_defense(self):
        """Return the defense stat of the player character"""
        return self._stats["defense"]

    def get_inventory(self):
        """Return the player character's inventory"""
        return self._inventory

    def add_item(self, item):
        """Add an item to the player character's inventory."""
        self._inventory.append(item)


def create_player():
    """Create the player object by evaluating whether there is save_data being loaded."""

    # Create data to load into player class in case there is no legitimate save data
    new_player_data = {"name": "placeholder",
                       "stats": {
                           "health": 100,
                           "mana": 0,
                           "attack": 10,
                           "defense": 10
                       },
                       "inventory": [],
                       "position": ["placeholder", [0, 0]]
                       }

    # Examine the save data file, evaluate validity, create player and return accordingly
    try:
        with open('save_file.json', 'r') as save_data:
            contents = save_data.read().strip()
            if not contents:
                player = Player(new_player_data)
            else:
                player_data = json.loads(contents)
                player = Player(player_data)
    except (FileNotFoundError, json.JSONDecodeError):
        player = Player(new_player_data)
        # CODE TO TELL PLAYER ERROR HAPPENED?

    return player

# test = create_player()
# print(test.get_name())
# test.add_item('pear')
# print(test.get_inventory())
# print(test.get_health())
