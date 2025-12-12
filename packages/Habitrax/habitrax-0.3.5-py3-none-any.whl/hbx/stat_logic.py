from .toolbox import no_data, color, center, underline
from .toolbox import get_exp, number_padding, warning
from .toolbox import var_per_cat, label, choose
from .toolbox import list_options, get_exp
from . import storage

def menu():   
    header = center(" Stat logic ")
    print(f"\n{color(header, 'green')}\n")
    
    options = {
        "Rename stats": rename,
        "Combine stats": combine
    }
        
    list_options(options)
    choose(options, src=menu)       
    
def rename():
    data = storage.load_data(storage.LEVEL_FILE)[1:]
    if not data:
        no_data("No stats found")
        return
    
    mapping  = storage.load_map()
    combined = mapping.get("Combinations", {})
    
    print()
    names = []
    for entry in data:
        name = entry["Category"]
        for co_name, group in combined.items():
            if name in group: name = co_name
        if name not in names: names.append(name)
        
    list_options(names)
    choice = choose(names, 1, rename)        
    if choice is None: return
        
    name     = names[choice]
    new_name = input(color("\nEnter new name for "
             + f"{name.lower()}: "))
    rename_stat(name, new_name)
    ft = center(f" {name} Renamed Successfully ", "—")
    print(f"\n{ft}")

def combine():
    data = storage.load_data(storage.LEVEL_FILE)[1:]
    if not data:
        no_data("No stats found")
        return
    
    mapping  = storage.load_map()
    combined = mapping.get("Combinations", {})   
    labels   = label([
        "Enter new name: ",
        "Choose stats to combine (e.g., 1 2): "
    ])
    
    print()       
    names = []
    for entry in data:
        name = entry["Category"]
        for co_name, group in combined.items():
            if name in group: name = co_name
        if name not in names:
            names.append(name.strip().title())
        
    list_options(names, "Choose name(s)")
    print(f"{len(names)+1}. Back\n")        
    while True:
        try:
            prompt = input(labels[1])
            if prompt == str(len(names)+1):
                print()
                underline()
                return
                
            choices = prompt.split()              
            indices = [int(num) for num in choices]
            if any(0 >= i or i > len(names) for i in 
                indices): raise ValueError
            break
        except ValueError: pass
        warning("Invalid input! Try again.")
        
    source_list = [names[int(c)-1] for c in choices]
        
    print()
    names = ["New"]
    if mapping["Combinations"]:
        names = [name for name in 
                mapping["Combinations"]]
        names.append("New")
    list_options(names, "Add to combination")
    choice = choose(names, 1, combine)
    if choice is None: return
                
    target_name = names[choice].title().strip()
    if target_name == "New":
        print()
        target_name = input(labels[0]).strip().title()
        
    combine_stats(target_name, source_list)
    footer = center(f" {len(source_list)} Names "
           + "Combined Successfully ", "—")
    print(f"\n{footer}")

def rename_stat(original: str, new_name: str):
    mapping = storage.load_map()
    mapping["Renames"][original] = new_name
    storage.save_data(storage.STAT_MAP, mapping)

def combine_stats(target_name:str, source_list:list):
    mapping      = storage.load_map()
    combinations = mapping["Combinations"]
    
    if target_name in combinations:
        combinations[target_name].extend(source_list)
        storage.save_data(storage.STAT_MAP, mapping)
        return
    
    combinations[target_name] = source_list
    storage.save_data(storage.STAT_MAP, mapping)

def get_resolved_stats() -> dict:
    data     = storage.load_data(storage.DATA_FILE)
    mapping  = storage.load_map()   
    renames  = mapping.get("Renames", {})
    combined = mapping.get("Combinations", {})
    resolved = {}

    for stat in data:
        original = stat["Category"]
        name     = renames.get(original, original)

        # If this stat is part of a combination
        for combined_name, group in combined.items():
            if original in group:
                name = combined_name
                name = renames.get(name, name)               

        resolved.setdefault(name, [])
        if original not in resolved[name]:
            resolved[name].append(original)

    return resolved
