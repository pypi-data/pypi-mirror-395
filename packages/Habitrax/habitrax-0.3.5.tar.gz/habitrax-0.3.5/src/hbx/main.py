"""
Entry point of the Questline CLI application (Habitrax)
Displays the main menu and routes to each core module
"""
from .toolbox import warning, choose_from, list_options
from .toolbox import center, color, clear, underline
from . import status_window
from . import soul_work
from . import notebook
from . import debrief
from . import profile
from . import config
from . import logger
from . import setup
from . import stats
from . import tasks

def main():
    header = center("《 QUESTLINE 》", line="=")
    print(header)
    
    options = {       
               "Log session": logger.log_session  ,
            "Mission center": tasks.menu          ,
                   "Debrief": debrief.menu        ,
                 "Soul work": soul_work.menu      ,
        "View Status Window": status_window.window,
                "Statistics": stats.menu          ,        
                  "Notebook": notebook.menu       ,
                   "Profile": profile.menu        ,
                  "Settings": config.menu
    }
    
    all_opt = str(len(options) + 1)
    while True:
        print()
        list_options(options, "Choose action")
        print(f"{all_opt}. Exit")
        
        try: opt = input(color(">>> ", "magenta"))
        except (EOFError, KeyboardInterrupt): 
            opt = all_opt
        try:
            # Convert user input to index, call the 
            # associated function
            choice = int(opt) - 1
            choose_from(options, choice)()
        except (ValueError, StopIteration):
            # Special command to clear screen
            if opt == "clear": clear()
            # Exit condition
            elif opt == all_opt: clear(terminate=True)
            # Invalid input handling
            else: print(warning("\nInvalid choice. "
                       +f"Choose from 1 to {all_opt}.", 
                       inline=True))
            continue