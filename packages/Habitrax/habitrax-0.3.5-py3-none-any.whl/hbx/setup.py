from .toolbox import clear, color, center, underline
from .toolbox import warning, timetools, iter_print
from .toolbox import wrap_text, help_msg
from . import storage
import time
import sys
import os

USER_FILE_PATH = storage.DATA_DIR / storage.USER_FILE

def user_exists():
    if os.path.exists(USER_FILE_PATH):
        with open(USER_FILE_PATH) as f:
            if len(list(f)) > 1: return True

def commandments():
    msg = "Enter commandments one by one." \
        + "Type 'done' when finished:"
    print("\n"+color(wrap_text(msg), 'yellow'), "\n")
    
    decalogue = []
    while True:
        commandment = input(color(
            f"Commandment {len(decalogue)+1}: ",
            "cyan")).strip()
        
        # Stops input if user types 'done'
        if commandment.lower() == "done": break
        elif commandment: decalogue.append(commandment)
    
    return decalogue

def setup_user():
    print("\n"+center(" 《 HABITRAX SETUP 》 ", "="))
    welcome = f"Welcome! Let's get a few details to " \
            + f"personalize your experience."    
    print(f"\n{wrap_text(welcome)}\n")

    user_data = {}
    user_data["Name"] = input(color(
        "Your name or nickname: ", "cyan")).strip()
    
    name = user_data.get("Name", "Anonymous")
    while True:
        try: 
            birthday = input(color("Your birthday (YYYY"
                     + "-MM-DD): ", "cyan")).strip()
            user_data["Birthday"] = timetools.to_iso(
                                    birthday)
            if user_data["Birthday"] is None:
                raise ValueError
            break
        except ValueError:
            warning("Invalid format! Try again.")
    
    user_data["Aim"] = input(color("Your chief aim: ", 
                       "cyan")).strip()    
    prompt = input("\nDo you want to write your "
           + "commandments? [y/n]\n"
           + f"{color('>>> ', 'magenta')}")
    
    if prompt and prompt[0].lower() == "y":
        user_data["Decalogue"] = commandments()
    
    if name:
        print("\n"+color(f"Welcome, {name}!", "green"))
    storage.save_data(storage.USER_FILE, user_data)
    footer = center(" Setup complete! ", "—")
    print(f"\n{footer}\n")
    time.sleep(.75)
    print(color("Launching Habitrax", "green"), end="", 
        flush=True)
    time.sleep(1)
    iter_print(color(".", "green"), times=3, end="", 
        delay=.75)
    time.sleep(1)
    clear(print_header=False)

if __name__ != "__main__": 
    if not user_exists():
        if len(sys.argv) > 1: help_msg(True, True)
        try: setup_user()
        except (KeyboardInterrupt, EOFError) as e:
            if isinstance(e, EOFError): print()
            warning("Setup cancelled by user.", True)
            underline()
            time.sleep(1)
            clear(print_header=False)
            sys.exit(1)
