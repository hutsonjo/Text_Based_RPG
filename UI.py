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
        self._player = Player({
            "name": "placeholder",
            "stats": {
                "health": 100,
                "mana": 0,
                "attack": 10,
                "defense": 10
            },
            "inventory": [],
            "position": ["placeholder", [0, 0]]})

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

        # UI control component frames
        self._direction_frame = Frame(self._root, bg='#9c9c9c')
        self._inventory_frame = Frame(self._root, bg='#9c9c9c')
        self._inspect_frame = Frame(self._root, bg='#9c9c9c')
        self._stats_frame = Frame(self._root, bg='#9c9c9c')

        # UI control component buttons
        self._north_button = Button(self._direction_frame, text='North', command=lambda: self._move('north'))
        self._east_button = Button(self._direction_frame, text='East', command=lambda: self._move('east'))
        self._south_button = Button(self._direction_frame, text='South', command=lambda: self._move('south'))
        self._west_button = Button(self._direction_frame, text='West', command=lambda: self._move('west'))
        self._inventory_button = Button(self._inventory_frame, text='Inventory', command=self._inventory_page)
        self._inspect_button = Button(self._inspect_frame, text='Inspect', command=self._inspect_page)
        self._stats_button = Button(self._stats_frame, text='Stats', command=self._stats_page)

        # Start window frames and button
        self._text_window = Frame(self._root)
        self._text_window.place(relx=0, rely=0, relwidth=1, relheight=.8)
        self._text_label = Label(self._text_window,
                                 text=INTRO_TEXT,
                                 wraplength=800,
                                 justify='center',)
        self._text_label.pack(expand=True, fill='both')
        self._bottom_window = Frame(self._root)
        self._bottom_window.place(relx=0, rely=0.8, relwidth=1, relheight=.2)
        self._ready_button = Button(self._bottom_window,
                                    text="I'm Ready!",
                                    command=self._ready,
                                    bg='#9c9c9c')
        self._ready_button.place(relx=0.5, rely=0.25, anchor='center')
        self._help_button = Button(self._bottom_window, text='Help', command=self._help_page)  # Later use

        # Load window buttons
        self._new_file_button = Button(self._bottom_window,
                                       text="New File",
                                       command=self._initiate_game,
                                       bg='#9c9c9c')
        self._load_button = Button(self._bottom_window,
                                   text="Continue",
                                   command=self._load_save,
                                   bg='#9c9c9c')

        # Initialize the UI
        self._root.mainloop()

    def _ready(self):
        """Responds user clicking the ready button and moves to the next page offering the chance to load save data"""
        self._text_label.config(text=LOAD_TEXT)
        self._ready_button.place_forget()
        self._new_file_button.place(relx=0.4, rely=0.25, anchor="center")
        self._load_button.place(relx=0.6, rely=0.25, anchor="center")

    def _load_save(self):
        """Loads the saved or initiates a new player"""
        self._game_logic.load_player()
        self._initiate_game()

    def _initiate_game(self):
        """Initiates the gameplay portion of the UI."""
        # Reshape the text windows
        self._text_window.place_configure(relx=0, rely=0, relwidth=.8, relheight=.8)
        self._bottom_window.place_configure(relx=0, rely=0.8, relwidth=.8, relheight=.2)

        # Place the frames for the controls onto the UI
        self._direction_frame.place(relx=0.8, rely=0, relwidth=.2, relheight=.25)
        self._inventory_frame.place(relx=0.8, rely=0.25, relwidth=.2, relheight=.25)
        self._inspect_frame.place(relx=0.8, rely=0.5, relwidth=.2, relheight=.25)
        self._stats_frame.place(relx=0.8, rely=0.75, relwidth=.2, relheight=.25)

        # Place the buttons into the control frames
        self._north_button.place(relx=0.5, rely=0.0, anchor="n")
        self._east_button.place(relx=1, rely=0.5, anchor="e")
        self._south_button.place(relx=0.5, rely=1, anchor="s")
        self._west_button.place(relx=0, rely=0.5, anchor="w")
        self._inventory_button.pack(expand=True, fill="both")
        self._inspect_button.pack(expand=True, fill="both")
        self._stats_button.pack(expand=True, fill="both")
        self._help_button.pack(side='bottom', anchor='w')

    def _move(self, direction):
        """Advances the player through the map"""
        pass

    def _inventory_page(self):
        """Restructures the text window according to the inventory of the player character."""
        pass

    def _inspect_page(self):
        """Inspects the environment, fetching additional text information for the user to read."""
        pass

    def _stats_page(self):
        """Restructures the text window according to the stats of the player character."""
        pass

    def _help_page(self):
        """Deploys a pop-up window to remind the player of the control scheme."""
        pass


if __name__ == '__main__':
    logic = GameLogic()
    game = UI(logic)
