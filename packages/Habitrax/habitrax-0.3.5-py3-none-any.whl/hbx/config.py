from .toolbox import center, choose, list_options
from . import stat_logic
from . import about

def menu():
    header = center("《 Settings 》", line="—")
    print(f"\n{header}\n")
    
    options = {
        "Stats": stat_logic.menu,
        "About": about.menu
    }
    
    list_options(options)
    choose(options, src=menu)