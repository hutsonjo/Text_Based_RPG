import textwrap

INTRO_TEXT = textwrap.dedent("""
        ARCHON'S ADVENTURE\n\n
        Welcome to Joshua Hutson’s CS 361 Project\n\n
        Welcome to the adventure! In this game, you’ll get to explore different locations, acquire interesting items, 
        and make narrative decisions to progress. Use the directional buttons to move forward, back, left, or right. 
        Interact with items in your inventory to use or discard them, inspect locations for important details, and check 
        your player’s stats to keep track of your progress. Each action is controlled with simple button presses.\n\n
        Ready to start your journey?
        """)

LOAD_TEXT = textwrap.dedent("""
        ARCHON'S ADVENTURE\n\n\n\n
        If this is not your first time playing, you may click “Continue” to load your previous save file.
        If this is your first playthrough or you would like to start a new game, then click “New File”.\n
        BE WARNED! Any old save files will be deleted upon starting anew.
        You may access the save/load commands from the player stats at any point.
        """)

HELP_TEXT = textwrap.dedent("""
        Directions:
        Use the directional buttons to explore the environment. 
        Interact with items in your inventory to use or discard them, inspect locations for important details. 
        Go to the stats screen to check your current stats as well as save the current game or load the previous save file.
        """)

LOAD_WARNING_TEXT = textwrap.dedent("""
        Warning! You will lose any progress that you have made since you last saved!\n
        Are you sure that you want to continue loading your previous save?
        """)

GAME_OVER = textwrap.dedent("""
        What a pity... it would seem misfortune has befallen you.\n\n
        Would you like to turn back the clock?\n\n
        Or perhaps begin anew...
        """)