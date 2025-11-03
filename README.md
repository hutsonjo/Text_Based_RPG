# Text-Based RPG

A Python-based text adventure game with a graphical interface built in Tkinter and microservice communication powered by ZeroMQ.
Players can move around a map, collect items, and view stats — all within a simple GUI that interacts with a separate map server.

## Project Overview

This project demonstrates a microservice-driven architecture for a text-based RPG.
The main UI and game logic are separated from the map generation and retrieval service, which runs independently and communicates via ZeroMQ sockets.

### Components

UI.py - The main game interface and logic controller. Handles player input, movement, inventory, and interactions. 

test_map.py - A standalone map microservice that responds to map position requests from the main game.

item.py - Defines the Item class and item effect behavior.

save_file.json - Stores persistent player data (position, stats, and inventory).

### How It Works

1. test_map.py runs as a server using ZeroMQ REP socket.

   * It listens for incoming map requests.

   * It returns the environment data (narration and inspection text) for given coordinates.

   * If the player moves out of bounds, it returns an error message.

2. UI.py runs as the client using a ZeroMQ REQ socket.

   * Sends the player’s position to the map service.

   * Receives and displays the map data (narration, inspection, etc.).

   * Updates the player’s location and state accordingly.

### Running the Game

#### Important: The map service (test_map.py) must be running before launching the main game (UI.py).

Step 1: Run the Map Service
python test_map.py

Keep this terminal open — it will log map requests and responses.

Step 2: Run the Main Game
python UI.py

The Tkinter UI should appear.
You can move using the directional buttons and interact with items as they appear.

### Saving & Loading

The game includes save file and load file buttons in the stat screen that save to json.

Saved data includes:

Player name and position

Stats (attack, defense, etc.)

Inventory (stored by item names)

Current Limitation

Inventory items are serialized as their names; item effects are re-linked via an internal ITEM_LIBRARY when loading.

Only pre-defined items can be restored correctly after reloading.

## Known Issues / Limitations
Map dependency - The map server (test_map.py) must be running before UI.py. Otherwise, the game will hang waiting for a response.

Single map - Currently only supports one static map (test_map).

Lack of content - The game is currently in a test state and therefor lacks in narrative content and is absent of combat.

### Future Improvements

* Add combat to the game as a feature

* Add error handling to prevent UI freezing when map service is unavailable.

* Convert movement and map access into async or threaded operations for better responsiveness.

* Implement multiple maps and smoother transitions.

* Add richer text descriptions.


## Tech Stack

Python 3.13

Tkinter — GUI framework

ZeroMQ (pyzmq) — Microservice communication

JSON — Data serialization for player saves

OOP Design — Modular player, item, and logic classes

### Author

Joshua Hutson
Designed and implemented as part of a software development portfolio project.
Focused on object-oriented design, inter-process communication, and stateful UI programming.