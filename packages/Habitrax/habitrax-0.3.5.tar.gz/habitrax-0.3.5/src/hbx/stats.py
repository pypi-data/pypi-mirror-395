from .toolbox import choose_from, var_per_cat, choose
from .toolbox import warning, list_options, wrap_text
from .toolbox import timetools, label, underline, pc
from .toolbox import color, center, no_data, clear 
from .toolbox import make_progress_bar as mpb
from tuikit.textools import strip_ansi
from datetime import datetime as dt
from operator import itemgetter
from . import storage

catch = []

def menu(from_term: bool = False):
    header = center("《 Statistics 》", "—")
    print(f"\n{header}")
    
    data = storage.load_data(storage.DATA_FILE)
    if not data:
        no_data("No data found")
        underline()
        return
        
    options = {
        "Overall stats": overall_stats,
        "Stats by category": by_category,
        "Stats by time of day": by_time,
        "All records": view_all,
        "View levels": get_levels
    }
    
    print()
    list_options(options, "View")    
    choose(options, src=menu)
    if from_term: print()

def overall_stats():
    header = center(" Overall ")
    print(f"\n{color(header, fg='green')}\n")
    
    data       = storage.load_data(storage.DATA_FILE)
    total      = len(data)
    total_time = sum(entry['Time spent'] for entry 
                 in data)
    avg_focus  = round(sum(entry['Focus'] for entry 
                 in data) / total, 2)
    avg_q_min  = round(sum(entry['Quality range'][0] 
                 for entry in data) / total, 2)
    avg_q_max  = round(sum(entry['Quality range'][1] 
                 for entry in data) / total, 2)
    avg_duration = timetools.format_time(total_time, 
                   total)
    total_time   = timetools.format_time(total_time)       
    time_pc, focus_pc, range_pc = pc.get_percent()   
    
    labels = label([
        "Avg focus:", "Total time:", 
        "Avg time:", "Total sessions:", 
        "Avg quality range:"
    ])    
    
    avg_fcs = f"{labels[0]} {avg_focus} {focus_pc}"
    avg_drn = f"{labels[2]} {avg_duration} {time_pc}"
    fcs     = len(strip_ansi(labels[0])) + 1
    drn     = len(strip_ansi(labels[2])) + 1
    
    print(wrap_text(avg_fcs, indent=fcs))
    print(wrap_text(avg_drn, indent=drn))
    print(labels[1], total_time)
    print(labels[3], total)       
    print(labels[4], avg_q_min,"—",avg_q_max,range_pc)    
    print()
    underline()

def by_category():
    header = center(" By Category ")
    print(f"\n{color(header, fg='green')}\n")
    
    file = storage.DATA_FILE
    categories = storage.get_tables(file, repair=False)
    cats_reprd = storage.get_tables(file)  
    
    labels = label([
        "Category:", "Avg Time:", "Avg Focus:",
        "Total time:", "Total sessions:"
    ])
    
    for cat_reprd, cat in zip(cats_reprd, categories):
        entries    = storage.load_table_as_list(file, cat)
        total      = len(entries)
        avg_focus  = sum(e["Focus"] for e in entries)\
                   / total
        total_time = sum(e["Time spent"] for e in entries)
        avg_duration      = timetools.format_time(
                            total_time, total)
        total_duration    = timetools.format_time(
                            total_time)
        time_pc, focus_pc = pc.get_grouped_percent(entries)
                
        avg_drn = f"{labels[1]} {avg_duration} "\
                + f"{time_pc}"
        avg_fcs = f"{labels[2]} {avg_focus:.2f} "\
                + f"{focus_pc}"
        drn     = len(strip_ansi(labels[1])) + 1
        fcs     = len(strip_ansi(labels[2])) + 1
    
        print(labels[0], cat_reprd)
        print(wrap_text(avg_drn, indent=drn))
        print(wrap_text(avg_fcs, indent=fcs))
        print(labels[3], total_duration)
        print(labels[4], total, end="\n\n")               
    underline()

def by_time():
    header = center(" By Time of Day ")
    print(f"\n{color(header, fg='green')}\n")
    
    data = storage.load_data(storage.DATA_FILE)
    
    timeblock = {
        'Morning': [], 'Afternoon': [], 
        'Evening': [], 'Night': []
    }

    for entry in data:
        hr = dt.fromisoformat(entry["Timestamp"]).hour
        if 5 <= hr < 12:
            timeblock['Morning'].append(entry)
        elif 12 <= hr < 17:
            timeblock['Afternoon'].append(entry)
        elif 17 <= hr < 21:
            timeblock['Evening'].append(entry)
        else: timeblock['Night'].append(entry)          
    
    labels = label([
        "Period:", "Avg Time:", "Avg Focus:", 
        "Total time:", "Total sessions:"
    ])
        
    for period, entries in timeblock.items():
        if not entries: continue
        total      = len(entries)
        avg_focus  = sum(e["Focus"] for e in entries
                 ) / total
        total_time = sum(e["Time spent"] for e in 
                     entries)
        total_duration    = timetools.format_time(
                            total_time)
        avg_duration      = timetools.format_time(
                            total_time, total)
        time_pc, focus_pc = pc.get_grouped_percent(
                            entries)
        
        avg_drn = f"{labels[1]} {avg_duration} "\
                + f"{time_pc}"
        avg_fcs = f"{labels[2]} {avg_focus:.2f} "\
                + f"{focus_pc}"
        drn     = len(strip_ansi(labels[1])) + 1
        fcs     = len(strip_ansi(labels[2])) + 1
    
        print(labels[0], period)
        print(wrap_text(avg_drn, indent=drn))
        print(wrap_text(avg_fcs, indent=fcs))
        print(labels[3], total_duration)
        print(labels[4], total, end="\n\n")
    underline()   

def category_records() -> list[dict] | None:
    file       = storage.DATA_FILE
    categories = storage.get_tables(file)
    print()
    list_options(categories, "Choose category")
    choice = choose(categories, 1, category_records)
    catch.append(choice)
    choice = catch[0]
    if choice is not None:        
        category = categories[choice]
        return storage.load_table_as_list(file, category)

def period_records() -> list[dict] | None:
    data = storage.load_data(storage.DATA_FILE)
    if not data:
        no_data("No data found")
        return
    
    timeblock = {'Morning': [], 'Afternoon': [], 
                 'Evening': [],     'Night': []}

    for entry in data:
        hr = dt.fromisoformat(entry["Timestamp"]).hour
        if 5 <= hr < 12:
            timeblock['Morning'].append(entry)
        elif 12 <= hr < 17:
            timeblock['Afternoon'].append(entry)
        elif 17 <= hr < 21:
            timeblock['Evening'].append(entry)
        else: timeblock['Night'].append(entry)

    print()    
    list_options(timeblock, "Choose period")    
    choice = choose(timeblock, 1, period_records)
    catch.append(choice)
    choice = catch[0]
    if choice is not None:
        return choose_from(timeblock, choice)

def view_all():
    header = center(" Viewing All Records! ")
    print(f"\n{color(header, fg='green')}")
    print()
    
    data = storage.load_data(storage.DATA_FILE)
    
    records = {
        "View All": "Placeholder", 
        "View Category": category_records, 
        "View Period": period_records
    }    
    list_options(records)
    choice = choose(records, 1, view_all)
    if choice is None: return
    elif choice > 0: 
        data = choose_from(records, choice)()
    if not data: return
    
    filters = {
        "A-Z": sorted(data, key=itemgetter('Task')),
        "Z-A": sorted(data, key=itemgetter('Task'), 
               reverse=True),
        "Latest": data.copy()[::-1],
        "Oldest": data,
        "Highest Focus": sorted(data, key=itemgetter(
                         'Focus'), reverse=True),
          "Least Focus": sorted(data, key=itemgetter(
                         'Focus')),
         "Longest Duration": sorted(data, key=itemgetter(
                             'Time spent'), reverse=True),
        "Shortest Duration": sorted(data, key=itemgetter(
                             'Time spent'))
    }
    
    print()
    list_options(filters, "Filter by")            
    choice = choose(filters, 1, view_all)
    if choice is None: return
    
    filtered = choose_from(filters, choice)            
    labels   = label([
        "Date:", "Task:", "Focus:",
        "Duration:", "Logged:"
    ])
    for entry in filtered:
        duration = timetools.format_time(entry[
                   'Time spent'])
        time = timetools.timestamp(entry['Timestamp'])
        lapsed = timetools.format_time_passed(entry[
                 'Timestamp'])
        description = f"{labels[1]} {entry['Task']}"
        print()
        print(labels[0], time)
        print(wrap_text(description, 6))
        print(labels[2], entry['Focus'])
        print(labels[3], duration)
        print(labels[4], lapsed, end="\n\n")
    underline()

def get_levels():
    header = center(" Skill Levels ", "—")    
    print(f"\n{header}\n")
    
    data = storage.load_data(storage.LEVEL_FILE)
    
    labels = label([
        "Category:", "Level:", "EXP",
        "Leveled up:", "On:"
    ])

    vpc = var_per_cat
    for index, entry in enumerate(data):
        if vpc(index) is None: continue
        bar, date, lapsed, exp_pc = vpc(index)        
        print(labels[0], entry['Category'])
        print(labels[1], entry['Level'])
        print(labels[2], bar, f"{exp_pc:.2f}%")
        print(labels[3], lapsed)
        print(labels[4], date, end="\n\n")
    underline()