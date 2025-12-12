from .toolbox import center, color, choose, warning
from .toolbox import make_progress_bar, underline
from .toolbox import list_options, choose_from
from .toolbox import no_data, timetools, label
from .toolbox import visual_width
from datetime import datetime
from . import storage
import shutil

def menu():
    header = center(" The Slight Edge ")
    print(f"\n{color(header, 'green')}\n")
    
    options = {
        "Vote action": ballot,
        "View trajectory": direction
    }
    
    list_options(options)  
    choose(options, src=menu)

def ballot(voting_via_proxy=False):
    data  = storage.load_data(storage.SLIGHT_EDGE)
    today = datetime.now().date()
    def new_day(vote=1):
        entry = {
            "Day": datetime.now().isoformat(),
            "Action": 1,
            "Score": vote,
            "Edge": (vote / 1) * 100
        }
        storage.save_entry(storage.SLIGHT_EDGE, entry)
        
    if voting_via_proxy:
        found = False
        for entry in data:
            if datetime.fromisoformat(entry["Day"]
                                ).date() == today:
                entry["Score"]  += 1
                entry["Action"] += 1
                entry["Edge"] = (entry["Score"] 
                              / entry["Action"]) * 100
                storage.save_data(storage.SLIGHT_EDGE, 
                    data)
                found = True
                break
            
        if not found: new_day()
        return
        
    header = center(" Ballot ")
    print(f"\n{color(header, 'green')}\n")
   
    list_options(["Good","Bad"], "Vote action")
    choice = choose([0, 1], 1, ballot)
    
    if choice is None: return
    
    vote = 1 if choice == 0 else 0

    found = False
    for entry in data:
        if datetime.fromisoformat(entry["Day"]).date(
                                          ) == today:
            entry["Score"]  += vote
            entry["Action"] += 1
            entry["Edge"] = (entry["Score"] 
                          / entry["Action"]) * 100
            storage.save_data(storage.SLIGHT_EDGE, 
                data)
            found = True
            break
            
    if not found: new_day(vote)
    
    footer = center(" Action Voted Successfully ","—")
    print("\n"+footer)

def direction():
    data = storage.load_data(storage.SLIGHT_EDGE)
    if not data:
        no_data("No decision/action votes found")
        underline()
        return
        
    header = center(" Life Trajectory ")
    print(f"\n{color(header, 'green')}\n")   
    
    options = [
        "Overall trajectory", 
        "Daily trajectory",
        "Trajectory graphs"
    ]
    
    list_options(options)    
    choice = choose(options, 1, direction)
    
    if choice is None: return
    elif choice < 2:
        print()
        display(choice)
    else: graph()
    underline()

def display(daily: bool = False):
    data    = storage.load_data(storage.SLIGHT_EDGE)
    actions = sum([entry["Action"] for entry in data])
    score   = sum([entry["Score"] for entry in data])    
    edge    = score / actions * 100
    trajectory = "Headed for success" if (edge >= 50
          ) else "Headed for failure"    
    
    labels = label([
        "Date:", "Trajectory:", "Chance of success:"
    ])
    
    if not daily:
        print(labels[1], trajectory)
        print(f"{labels[2]} {edge:.2f}%\n")
        return

    for entry in data:
        date = timetools.timestamp(entry["Day"], 1)
        trajectory = "Headed for success" if entry[
           "Edge"] >= 50 else "Headed for failure" 
        print(labels[0], date)
        print(labels[1], trajectory)
        print(f"{labels[2]} {entry['Edge']:.2f}%\n")

def graph():
    header = center(" Edge Trajectory Graphs ")
    print(f"{color(header, 'green')}\n")

    options = {
        "Bar Graph (Edge % per day)": edge_bar_graph,
        "Trendline": edge_trendline
    }

    list_options(options)
    choose(options)

def edge_bar_graph(limit: int = 7):
    print()
    data  = storage.load_data(storage.SLIGHT_EDGE)
    limit = min(limit, len(data))
    for entry in data[-limit:]:
        date = timetools.timestamp(entry["Day"], 0, 1)
        edge = entry["Edge"]
        bar  = make_progress_bar(edge / 100)
        print(f"\n{date[:-5]} {bar} {edge:>5.1f}%")
    print()

def edge_trendline(limit: int = 7):
    print()    
    data   = storage.load_data(storage.SLIGHT_EDGE)
    limit  = min(limit, len(data))
    values = [round(entry["Edge"]) for entry in 
             data[-limit:]]
    dates  = [timetools.timestamp(e["Day"], 0, 1)[:2] 
             for e in data[-limit:]]  # day only

    for y in range(100, -1, -5):
        row = f"{y:>3} ┤"
        for pos, v in enumerate(values):
            if v == 100: point = color("●", "magenta")
            elif 100 > v >= 75:
                point = color("●", "green")
            elif 75 > v > 30:
                point = color("●", "yellow")
            else: point = color("●", "red")
            filler = color("○", "gray")
            row += f"  {point} "  if (y - 5 < v <= y 
            ) else f"  {filler} "
        print(center(row))

    term_width  = shutil.get_terminal_size((80, 
                  20)).columns
    display_len = 28 if term_width > 49 else 25
    f           = 28 if term_width > 55 else 26
    print(center(" └" + "─" * display_len, fixed=f))
    print(center("   " + "  ".join(dates), fixed=f))
    print()