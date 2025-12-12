from .toolbox import timetools, color, number_padding
from . import soul_work
from . import storage
from . import toolbox
from . import level
from . import tasks

def window(from_term: bool = False):
    header = toolbox.center("《 STATUS 》", "—")
    print(f"\n{header}")
    
    user     = storage.load_data(storage.USER_FILE)
    birthday = user.get("Birthday")
    age      = "Unknown"
    if birthday: age = timetools.get_age(birthday)
    
    stat        = level.Stat()
    lvl, blocks = stat.get_stat_blocks()
    rank        = stat.get_rank(lvl)
    title       = stat.get_title(rank)
    name        = user.get("Name") or "Unknown"
    money       = soul_work.coffer(getter=True)
    
    toolbox.spacer(2)
    print(f" {color('Name:', 'cyan')} {name}")
    print(f"  {color('Age:', 'cyan')} {age}")
    print(f"{color('Level:', 'cyan')} {lvl}")
    print(f"{color('Title:', 'cyan')} {title}")
    print(f"{color('Money:', 'cyan')} ${money:.2f}")
    
    if not blocks:
        toolbox.no_data("No stats available yet")
        toolbox.underline()
        if from_term: print()
        return
    
    toolbox.spacer(2)        
    for block in blocks:
        stat =(f"{color(block['Short'], 'cyan')}  "
             + f"{block['Weight']}   {block['Bar']}   "
             + f"{block['Rank']}")
        print(toolbox.center(stat, fixed=41), "\n") 
    
    missions = tasks.get_missions()
    if not missions:
        toolbox.underline()
        return
    
    toolbox.spacer(2)       
    MISSIONS = toolbox.center("《 MISSIONS 》")
    print(color(MISSIONS, "green"))
    print()
    for index, mission in enumerate(missions):
        tasks.render_mission_card(mission, index)
    
    toolbox.underline()
    if from_term: print()
