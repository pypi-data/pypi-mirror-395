from .toolbox import no_data, center, timetools, label
from .toolbox import color, underline, choose 
from .toolbox import list_options
from datetime import datetime
from . import storage
from . import level
import time

def menu():
    print(f"\n{center('《 Notebook 》', '—')}\n")
    
    options = {
        "Write a new page": write,
        "Read a page": read,
        "Edit a page": edit,
        "Delete a page": del_page,
        "Trashcan": trashcan
    }
    list_options(options, "Choose action")   
    choose(options, src=menu)

def write():
    header = center(" New Page ")
    print(f"\n{color(header, 'green')}\n")
    
    labels = label(["Enter Title: ", "Write notes:"])
    
    start = time.time()
    page  = {
        "Title": input(f"{labels[0]}") or "Untitled",
        "Content": input(f"{labels[1]}\n\n"),
        "Timestamp": datetime.now().isoformat(),
        "Time": time.time()
    }
    end      = time.time()
    duration = (end - start) / 3600
    
    session = {
        "Timestamp": datetime.now().isoformat(),
        "Task": "Writing notes",
        "Category": "Writing",
        "Focus": 5,
        "Fuzziness": 0,
        "Time spent": duration,
        "Quality range": [5 * duration, 5 * duration]
    }
    
    storage.save_entry(storage.NOTEBOOK, page)
    storage.save_entry(storage.DATA_FILE, session)
    level.Stat("Writing").level_up()
    footer = center(" ✔ Page Saved Successfuly! ","—")
    print(f"\n{footer}")

def read(page=None):
    labels = label(["Title:", "Edited:"])    
    if page:
        stamp = timetools.timestamp(page["Timestamp"])
        print(f"\n{labels[0]} {page['Title']}\n")
        print(f"{page['Content']}\n")
        print(f"{labels[1]} {stamp}\n")
        underline()
        return
        
    notebook = storage.load_data(storage.NOTEBOOK)
    if not notebook:
        no_data("No notes written yet")
        underline()
        return
                      
    print(f"\n{color('Choose page', underule=1)}"+":")
    for pos, page in enumerate(notebook):
        print(f"{pos+1}.", page["Title"])  
    
    choice = choose(notebook, 1, read)
    if choice is None: return        
    page  = notebook[choice]
    stamp = timetools.timestamp(page["Timestamp"])
    print(f"\n{labels[0]} {page['Title']}\n")
    print(f"{page['Content']}\n")
    print(f"{labels[1]} {stamp}\n")
    underline()

def edit():    
    notebook = storage.load_data(storage.NOTEBOOK)
    if not notebook:
        no_data("No notes written yet")
        underline()
        return
    
    print(f"\n{color('Choose page', underule=1)}"+":")
    for pos, page in enumerate(notebook):
        print(f"{pos+1}.", page["Title"])  
    
    choice = choose(notebook, 1, read)
    if choice is None: return
    
    edited = notebook[choice]    
    labels = label([
        "Enter new title: ", 
        f"Add more notes:\n\n{edit['Content']}\n"
    ])
    
    print()
    list_options(["Edit title", "Edit content"],
                  "Choose action")
    choice = choose([0, 1], 1, edit)
    if choice is None: return
    elif choice == 0:
        edited["Title"] = input(labels[0])
    elif choice == 1:
        edited["Content"] += "\n"+input(labels[1])
    
    edited["Timestamp"] = datetime.now().isoformat()
    storage.save_data(storage.NOTEBOOK, notebook)
    foot = center(" ✔ Page Edited Successfuly! ", "—")
    print(f"\n{foot}")

def del_page():
    notebook = storage.load_data(storage.NOTEBOOK)
    if not notebook:
        no_data("No notes written yet")
        underline()
        return
    
    print(f"\n{color('Choose page', underule=1)}"+":")
    for pos, page in enumerate(notebook):
        print(f"{pos+1}.", page["Title"])  
    
    choice = choose(notebook, 1, del_page)
    if choice is None: return        
    
    page = notebook[choice]    
    text = color("\nAre you sure you want to delete "
         + f"{page['Title']}? [y/n]: ", "red") 
    confirmation = input(text)[0].lower().strip()
    
    if confirmation != "y":
        footer = center(" ✔ Page Not Deleted ", "—")
        print(f"\n{footer}\n")
        return
        
    page["Position"] = choice
    storage.save_entry(storage.TRASHCAN, page)
    del notebook[choice]
    storage.save_data(storage.NOTEBOOK, notebook)
    footer = center(" ✔ Page Moved to Trashcan ", "—")
    print(f"\n{footer}")
    
def trashcan():
    trash = storage.load_data(storage.TRASHCAN)
    if not trash:
        no_data("No deleted pages found")
        underline()
        return
        
    header = center(" Trashcan ")
    print(f"\n{color(header, 'green')}\n")
        
    notebook = storage.load_data(storage.NOTEBOOK)
    
    print(f"{color('Choose page', underule=1)}"+":")
    for pos, page in enumerate(trash):
        print(f"{pos+1}.", page["Title"])
    
    index = choose(trash, 1, trashcan)
    if index is None: return        
    
    page = trash[index]
    
    print()
    options = ["View page", "Restore page"]   
    list_options(options, "Choose action")    
    choice = choose(options, 1, trashcan)
    if choice is None: return 
    
    if choice == 0:
        read(page)
        return
        
    notebook.insert(page["Position"], page)
    del trash[index]
    storage.save_data(storage.TRASHCAN, trash)
    storage.save_data(storage.NOTEBOOK, notebook)
    foot =center(" ✔ Page Restored Successfuly! ","—")    
    print(f"\n{foot}")