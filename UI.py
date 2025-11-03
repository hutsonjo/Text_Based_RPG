import textwrap
from tkinter import *
import json
from game_texts import INTRO_TEXT, LOAD_TEXT, HELP_TEXT, LOAD_WARNING_TEXT
from items import *

###############
# Game Logic
###############


class Player:
    """A class that represents the player character information"""

    def __init__(self, player_data):
        """Initialize the player object by searching for save data"""
        self.name = player_data["name"]
        self.stats = player_data["stats"]
        self.inventory = player_data["inventory"]
        self.position = player_data["position"]


class Item:
    """A class that defines an item that can be held in the user's inventory."""
    def __init__(self, name, description, consumable=False,
                 equip_effect=lambda player: None,
                 apply_effect=lambda player: None,
                 remove_effect=lambda player: None):
        """Initialize the attributes of the Item object"""
        self.name = name
        self.description = description
        self.consumable = consumable
        self.equip_effect = equip_effect
        self.apply_effect = apply_effect
        self.remove_effect = remove_effect


class GameLogic:
    """A class that holds the logic for running an instance of the game and communicating with microservices."""

    def __init__(self):
        """Initialize the game instance, defined by player character save data and other factors."""
        self._player = Player({
            "name": "Hero",
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

    def save_player(self):
        """Access the save_file.json file and overwrite information to store current player object."""
        player_data = vars(self._player)
        try:
            with open('save_file.json', 'w') as save_data:
                json.dump(player_data, save_data)
        except Exception as e:
            print(f'error saving player data: {e}')

    def add_item(self, item):
        """Adds an item to the player character's inventory."""
        self._player.inventory.append(item)
        item.equip_effect(self._player)

    def remove_item(self, item):
        """Removes an item from the player character's inventory."""
        if item in self._player.inventory:
            self._player.inventory.remove(item)

    def use_item(self, item):
        """Uses the apply effect of an item in the player character's inventory."""
        item.apply_effect(self._player)
        self.remove_item(item)

    def stat_retrieval(self):
        """Returns a string of the player stats to be displayed in the stat label."""
        return textwrap.dedent(f"""
            Player: {self._player.name}
            
            Health: {self._player.stats['health']}
            Mana: {self._player.stats['mana']}
            Attack: {self._player.stats['attack']}
            Defense: {self._player.stats['defense']}
            """)

    def inv_retrieval(self):
        """Returns a list of the player's inventory defined by name, narration, and description."""
        return self._player.inventory



# ##############
# UI Structure
# ##############
class UI:
    """A class that presents the UI to the user and calls on the GameLogic object in according to user input"""

    def __init__(self, game_logic):
        # Inherit the game logic object
        self._game_logic = game_logic

        # Establish root window
        self._root = Tk()
        self._root.geometry("1000x800")
        self._root.title("Joshua Hutson CS361 Project")
        self._icon = PhotoImage(file='static/moon_icon.png')
        self._root.iconphoto(True, self._icon)
        self._root.option_add("*Font", ('Morris Roman', 20))
        self._root.option_add("*Foreground", "white")
        self._root.option_add("*Background", "#171717")

        # Establish UI control component frames
        self._direction_frame = Frame(self._root, bg='#9c9c9c')
        self._inventory_frame = Frame(self._root, bg='#9c9c9c')
        self._inspect_frame = Frame(self._root, bg='#9c9c9c')
        self._stats_frame = Frame(self._root, bg='#9c9c9c')

        # Establish UI control component buttons
        self._north_button = Button(self._direction_frame, text='North', command=lambda: self._move('north'))
        self._east_button = Button(self._direction_frame, text='East', command=lambda: self._move('east'))
        self._south_button = Button(self._direction_frame, text='South', command=lambda: self._move('south'))
        self._west_button = Button(self._direction_frame, text='West', command=lambda: self._move('west'))
        self._inventory_button = Button(self._inventory_frame, text='Inventory', command=self._inventory_page)
        self._inspect_button = Button(self._inspect_frame, text='Inspect', command=self._inspect_page)
        self._stats_button = Button(self._stats_frame, text='Stats', command=self._stats_page)

        # Establish and initialize text window frame
        self._text_window = Frame(self._root)
        self._text_window.place(relx=0, rely=0, relwidth=1, relheight=.8)

        # Establish labels that will switch out in text window frame
        self._text_label = Label(self._text_window,
                                 text=INTRO_TEXT,
                                 wraplength=800,
                                 justify='center',)
        self._inv_listbox = Listbox(self._text_window, justify='left')
        self._inv_desc_label = Label(self._text_window, wraplength=800, justify='left')
        self._inspection_label = Label(self._text_window, wraplength=800, justify='left')
        self._stats_label = Label(self._text_window, wraplength=800, justify='left')

        # Initialize each widget and then lift the primary text label
        for frame in (self._text_label, self._inspection_label, self._stats_label):
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._inv_listbox.place(relx=0, rely=0, relwidth=1, relheight=0.5)
        self._inv_desc_label.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)
        self._text_label.lift()

        # Initialize bottom of text window for button placements & initialize ready button
        self._bottom_window = Frame(self._root)
        self._bottom_window.place(relx=0, rely=0.8, relwidth=1, relheight=.2)
        self._ready_button = Button(self._bottom_window,
                                    text="I'm Ready!",
                                    command=self._ready,
                                    bg='#9c9c9c')
        self._ready_button.place(relx=0.5, rely=0.25, anchor='center')

        # Establish Bottom Pane buttons for later use
        self._help_button = Button(self._bottom_window, text='Help', command=self._help_page)
        self._return_button = Button(self._bottom_window, text='Return', command=self._return)
        self._use_item_button = Button(self._bottom_window, text='Use Item', command=self._use_item)
        self._discard_item_button = Button(self._bottom_window, text='Discard', command=self._discard_item)
        self._save_file_button = Button(self._bottom_window, text='Save File', command=self._game_logic.save_player)
        self._load_file_button = Button(self._bottom_window, text='Load File', command=self._load_warning)

        # Establish load window buttons
        self._new_file_button = Button(self._bottom_window,
                                       text="New File",
                                       command=self._initiate_game,
                                       bg='#9c9c9c')
        self._continue_button = Button(self._bottom_window,
                                       text="Continue",
                                       command=self._load_initial_save,
                                       bg='#9c9c9c')

        # Initialize the UI
        self._root.mainloop()

    def _ready(self):
        """Responds user clicking the ready button and moves to the next page offering the chance to load save data"""
        self._text_label.config(text=LOAD_TEXT)
        self._ready_button.place_forget()
        self._new_file_button.place(relx=0.4, rely=0.25, anchor="center")
        self._continue_button.place(relx=0.6, rely=0.25, anchor="center")

    def _load_initial_save(self):
        """Loads the saved or initiates a new player"""
        self._game_logic.load_player()
        self._initiate_game()

    def _initiate_game(self):
        """Initiates the gameplay portion of the UI."""
        # Reshape the text windows
        self._text_window.place_configure(relx=0, rely=0, relwidth=.8, relheight=.8)
        self._bottom_window.place_configure(relx=0, rely=0.8, relwidth=.8, relheight=.2)

        # Remove the new/continue buttons
        self._new_file_button.place_forget()
        self._continue_button.place_forget()

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
        self._help_button.place(relx=0, rely=1, anchor='sw')
        self._return_button.place(relx=1, rely=1, anchor='se')

    def _return(self):
        """Places the text window that holds narration at the front of the screen."""
        # Remove unneeded widgets
        self._remove_item_buttons()
        self._remove_save_buttons()

        # Enable any disabled controls and lift the text window
        self._inventory_button.config(state='normal')
        self._inspect_button.config(state='normal')
        self._stats_button.config(state='normal')
        self._enable_movement()
        self._text_window.lift()

    def _move(self, direction):
        """Advances the player through the map"""
        pass

    def _inventory_page(self):
        """Restructures the text window according to the inventory of the player character."""
        # Remove or disable unneeded widgets
        self._disable_movement()
        self._remove_save_buttons()
        self._inventory_button.config(state='disabled')
        self._stats_button.config(state='normal')

        # Bring up Inventory UI
        self._inv_listbox.lift()
        self._inv_desc_label.lift()
        self._use_item_button.place(relx=0.4, rely=0.25, anchor="center")
        self._discard_item_button.place(relx=0.6, rely=0.25, anchor="center")

        # UI logic
        self._inv_listbox.bind("<<ListboxSelect>>", self._on_inv_select)

        # Populate item list
        item_list = self._game_logic.inv_retrieval()
        for item in item_list:
            self._inv_listbox.insert('end', item.name)

    def _on_inv_select(self, event):
        """Displays the narration and description of the item that is currently selected to the text box on the
        inventory page."""
        # Identify cursor selection
        sel = event.widget.curselection()
        if not sel:
            return

        # Initialize variable for item and insert its description into the label
        item_list = self._game_logic.inv_retrieval()
        item = item_list[sel[0]]
        self._inv_desc_label.config(text=item.description)

    def _use_item(self):
        """Processes the apply_effect if the selected item is a consumable and then updates the displayed inventory
        accordingly."""
        # Identify cursor selection
        sel = self._inv_listbox.curselection()
        if not sel:
            return

        # Initialize variable for item and use it if it is a consumable, update inventory display
        item_list = self._game_logic.inv_retrieval()
        item = item_list[sel[0]]
        if item.consumable:
            self._game_logic.use_item(item)
            self._inv_listbox.delete(sel[0])

    def _discard_item(self):
        """Remove the selected item from the player character's inventory."""
        # Identify cursor selection
        sel = self._inv_listbox.curselection()
        if not sel:
            return

        # Removes the item, update inventory display
        item_list = self._game_logic.inv_retrieval()
        item = item_list[sel[0]]
        self._game_logic.remove_item(item)
        self._inv_listbox.delete(sel[0])

    def _inspect_page(self):
        """Inspects the environment, fetching additional text information for the user to read."""
        self._disable_movement()

    def _stats_page(self):
        """Restructures the text window according to the stats of the player character."""
        # Remove or disable unneeded widgets
        self._disable_movement()
        self._remove_item_buttons()
        self._stats_button.config(state='disabled')
        self._inventory_button.config(state='normal')

        # Bring up stats UI
        self._stats_label.lift()
        self._stats_label.configure(text=self._game_logic.stat_retrieval())
        self._save_file_button.place(relx=0.4, rely=0.25, anchor="center")
        self._load_file_button.place(relx=0.6, rely=0.25, anchor="center")

    def _load_warning(self):
        """Loads the saved player data after warning player about losing current state"""
        self._load_warning_popup = Toplevel(self._root)
        self._load_warning_popup.geometry('500x400')
        self._load_warning_popup.title('SLOW YOUR ROLL')
        self._load_warning_label = Label(self._load_warning_popup, text=LOAD_WARNING_TEXT, wraplength=400)
        self._load_warning_label.pack()
        self._yes_load_button = Button(self._load_warning_popup, text='YES',
                                       command=lambda: (self._game_logic.load_player(),
                                                        self._load_warning_popup.destroy()))
        self._yes_load_button.place(relx=0.4, rely=0.8, anchor='center')
        self._no_load_button = Button(self._load_warning_popup, text='NO', command=self._load_warning_popup.destroy)
        self._no_load_button.place(relx=0.6, rely=0.8, anchor='center')

    def _help_page(self):
        """Deploys a pop-up window to remind the player of the control scheme."""
        self._help_popup = Toplevel(self._root)
        self._help_popup.geometry('500x400')
        self._help_popup.title('WE COULD ALL USE A LITTLE HELP SOMETIMES')
        self._help_label = Label(self._help_popup, text=HELP_TEXT, wraplength=400)
        self._help_label.pack()

    def _disable_movement(self):
        """Disables the movement buttons while on the non-exploration screens"""
        self._north_button.config(state='disabled')
        self._east_button.config(state='disabled')
        self._south_button.config(state='disabled')
        self._west_button.config(state='disabled')

    def _enable_movement(self):
        """Enables the movement buttons while on the non-exploration screens"""
        self._north_button.config(state='normal')
        self._east_button.config(state='normal')
        self._south_button.config(state='normal')
        self._west_button.config(state='normal')

    def _remove_item_buttons(self):
        """Removes the use item and discard buttons from the UI."""
        if self._use_item_button.winfo_ismapped:
            self._use_item_button.place_forget()
        if self._discard_item_button.winfo_ismapped:
            self._discard_item_button.place_forget()

    def _remove_save_buttons(self):
        """Removes the save file and load file buttons from the UI."""
        if self._save_file_button.winfo_ismapped:
            self._save_file_button.place_forget()
        if self._load_file_button.winfo_ismapped:
            self._load_file_button.place_forget()


if __name__ == '__main__':
    logic = GameLogic()
    game = UI(logic)
