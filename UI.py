from tkinter import *
import json
from game_texts import INTRO_TEXT, LOAD_TEXT


###############
# Game Logic
###############

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

    def remove_item(self, item):
        """Remove an item from the player character's inventory"""
        self._inventory.remove(item)


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


class GameLogic:
    """A class that holds the logic for running an instance of the game and communicating with microservices."""

    def __init__(self):
        """Initialize the game instance, defined by player character save data and other factors."""
        self._player = Player({"name": "placeholder",
                           "stats": {
                               "health": 100,
                               "mana": 0,
                               "attack": 10,
                               "defense": 10
                           },
                           "inventory": [],
                           "position": ["placeholder", [0, 0]]
                           })

    def load_player(self):
        """Access the save_file.json file get information to create a previously saved player object."""
        try:
            with open('save_file.json', 'r') as save_data:
                contents = save_data.read().strip()
                if not contents:
                    return
                else:
                    player_data = json.loads(contents)
                    self._player = Player(player_data)
        except (FileNotFoundError, json.JSONDecodeError):
            return


# ##############
# UI Structure
# ##############
class UI:
    """A class that presents the UI to the user and calls on the GameLogic object in according to user input"""

    def __init__(self, game_logic):
        # Inherit the game logic object
        self._game_logic = game_logic

        # Root window
        self._root = Tk()
        self._root.geometry("1000x800")
        self._root.title("Joshua Hutson CS361 Project")
        self._icon = PhotoImage(file='static/moon_icon.png')
        self._root.iconphoto(True, self._icon)
        self._root.option_add("*Font", ('Morris Roman', 20))
        self._root.option_add("*Foreground", "white")
        self._root.option_add("*Background", "#171717")

        # UI component frames
        self._control_panel = Frame(self._root, bg='#9c9c9c')
        self._direction_frame = Frame(self._control_panel, bg='#9c9c9c')
        self._inventory_frame = Frame(self._control_panel, bg='#9c9c9c')
        self._inspect_frame = Frame(self._control_panel, bg='#9c9c9c')
        self._stats_frame = Frame(self._control_panel, bg='#9c9c9c')

        # Start window frames and button
        self._text_window = Frame(self._root)
        self._text_window.place(relx=0, rely=0, relwidth=1, relheight=.8)
        self._intro_label = Label(self._text_window,
                                  text=INTRO_TEXT,
                                  wraplength=800,
                                  justify='center',
                                  )
        self._intro_label.pack(expand=True, fill='both')
        self._intro_bottom_frame = Frame(self._root)
        self._intro_bottom_frame.place(relx=0, rely=0.8, relwidth=1, relheight=.2)
        self._ready_button = Button(self._intro_bottom_frame,
                                    text="I'm Ready!",
                                    command=self._ready,
                                    bg='#9c9c9c')
        self._ready_button.place(relx=0.5, rely=0.25, anchor='center')

        # Load window buttons
        self._new_file_button = Button(self._intro_bottom_frame,
                                       text="New File",
                                       command=lambda: self._initiate_game,
                                       bg='#9c9c9c')
        self._load_button = Button(self._intro_bottom_frame,
                                   text="Continue",
                                   command=self._load_save,
                                   bg='#9c9c9c')

        # Initialize the UI
        self._root.mainloop()

    def _ready(self):
        """Responds user clicking the ready button and moves to the next page offering the chance to load save data"""
        self._intro_label.config(text=LOAD_TEXT)
        self._ready_button.place_forget()
        self._new_file_button.place(relx=0.4, rely=0.25, anchor="center")
        self._load_button.place(relx=0.6, rely=0.25, anchor="center")

    def _load_save(self):
        """Loads the saved or initiates a new player"""
        self._game_logic.load_player()
        self._initiate_game()

    def _initiate_game(self):
        """Initiates the gameplay portion of the UI."""
        # Reshape the text window


if __name__ == '__main__':
    logic = GameLogic()
    game = UI(logic)
