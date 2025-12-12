"""
This module is meant to streamline deep reflection
Main functions:
  -        reflect(...)
  - shadow_journal(...)
  - debrief_review(...)
"""
from .toolbox import choose_from, strip_ansi, no_data
from .toolbox import choose, list_options, underline
from .toolbox import wrap_text as wrap, center as c
from .toolbox import warning, label, variables
from .toolbox import color, timetools
from .slight_edge import ballot
from datetime import datetime
from time import time
from . import storage
from . import level
import random

def menu():
    header = c("《 Debrief 》", line="—")
    print(f"\n{header}\n")
        
    options = {
        "Daily reflection": reflect,
        "Shadow work journal": shadow_journal,
        "Debrief review": debrief_review
    }
    
    list_options(options)
    choose(options, src=menu)

def reflect(from_term: bool = False):
    """
Reflect deeply from a series of 5 to 10 questions per session
    """
    line = "—" if from_term else ""
    header = c(" Daily Reflection ", line)
    print(f"\n{color(header, fg='green')}")
    
    # Load the pool of questions from the JSON file
    data = storage.load_data(storage.QUESTIONS)

    start = time()
    
    # Flatten the questions into a single list with 
    # themes
    pool = [{
        "question": question, 
           "theme": theme
    } for theme, questions in data.items()
      for question in questions]
    
    count    = random.randint(5, 10)
    selected = random.sample(pool, count)

    try:
      for n, item in enumerate(selected):
         i = len(f"Q{n+1}. ")
         print()
         print(wrap(f"Q{n+1}. {item['question']}", i))
         reply     = input(color(">>> ", "magenta"))
         timestamp = datetime.now().isoformat()
        
         # Save each reflection as a separate entry
         reflection = {
              "Question": item["question"],
                "Answer": reply           ,
                 "Theme": item["theme"]   ,
             "Timestamp": timestamp       ,
                  "Time": time()
         }        
         storage.save_entry(storage.REFLECTIONS, 
                            reflection)       
    
      end = time()    
      duration = round((end - start) / 3600, 3)    
    
      labels = label([
          "Depth level (1–10): ", 
          "Uncertainty in depth (±): "
      ])    
    
      focus, fuzziness = variables(labels)
    except(KeyboardInterrupt, EOFError, TypeError)as e:
        if     isinstance(e,  EOFError): print()
        if not isinstance(e, TypeError):
            print()
            underline()
        if from_term: print()
        return
    
    focus     = max(0, min(focus,     10))
    fuzziness = max(0, min(fuzziness,  2))

    q_min   = max( 0, (focus - fuzziness) * duration)
    if q_min > 10: q_min = 10
    q_max   = min(10, (focus + fuzziness) * duration)
    if q_max <  0: q_max =  0
    q_range = [q_min, q_max]

    session = {
            "Timestamp": datetime.now().isoformat()  ,
                 "Task": "Daily reflection session"  ,
             "Category": "Meditation"                ,
                "Focus": focus                       ,
            "Fuzziness": fuzziness                   ,
           "Time spent": duration                    ,
        "Quality range": [round(q,2) for q in q_range]
    }
    
    storage.save_entry(storage.DATA_FILE, session)
    
    ballot(1)
    level.Stat("Meditation").level_up()
    done = c(" ✔ Reflection Logged Successfuly! ","—")
    print(f"\n{done}")
    if from_term: print()

def shadow_journal(from_term: bool = False):
    """Reflect on what recently occured to you"""
    line = "—" if from_term else ""
    header = c(" Shadow Work Journal ", line)
    print(f"\n{color(header, fg='green')}")
    
    start = time()
    
    long = [
"How did you react externally (words, body language, tone)?",
"Does this remind you of anything from your past?",
"What belief about yourself or others was exposed?",
"What did you need in that moment but didn't get?",
"How can you view this situation differently now?",
"How do you want to handle similar moments going forward?"
    ]
    
    wrapped = [wrap(q) for q in long]
    prompt = color('>>> ', 'magenta')
    
    questions = [
f"\nWhat happened?\n{prompt}",
f"\nWhat did you feel?\n{prompt}",
f"\n{wrapped[0]}\n{prompt}",
f"\nWhy did it affect you so strongly?\n{prompt}",
f"\n{wrapped[1]}\n{prompt}",
f"\n{wrapped[2]}\n{prompt}",
f"\n{wrapped[3]}\n{prompt}",
f"\n{wrapped[4]}\n{prompt}",
f"\n{wrapped[5]}\n{prompt}"
    ]
    
    try:
        entry = {
         "Trigger Event": input(questions[0])       ,
    "Emotional Response": input(questions[1])       ,
              "Reaction": input(questions[2])       ,
          "Deeper Truth": input(questions[3])       ,
             "Past Echo": input(questions[4])       ,
           "Core Belief": input(questions[5])       ,
                  "Need": input(questions[6])       ,
               "Reframe": input(questions[7])       ,
             "Next Time": input(questions[8])       ,
             "Timestamp": datetime.now().isoformat(),
                  "Time": time()
        }    
    
        end      = time()
        duration = round((end - start) / 3600, 3)
    
        labels = label([
            "Depth level (1–10): ", 
            "Uncertainty in depth (±): "
        ])
    
        focus, fuzziness = variables(labels)    
    except(KeyboardInterrupt, EOFError, TypeError)as e:
        if     isinstance(e,  EOFError): print()
        if not isinstance(e, TypeError):
            print()
            underline()
        if from_term: print()
        return
    
    focus     = max(0, min(focus,     10))
    fuzziness = max(0, min(fuzziness,  2))

    q_min   = max( 0, (focus - fuzziness) * duration)
    if q_min > 10: q_min = 10
    q_max   = min(10, (focus + fuzziness) * duration)
    if q_max <  0: q_max =  0
    q_range = [q_min, q_max]

    session = {
            "Timestamp": datetime.now().isoformat()  ,
                 "Task": "Shadow work"               ,
             "Category": "Meditation"                ,
                "Focus": focus                       ,
            "Fuzziness": fuzziness                   ,
           "Time spent": duration                    ,
        "Quality range": [round(q,2) for q in q_range]
    }
    
    storage.save_entry(storage.JOURNAL, entry)
    storage.save_entry(storage.DATA_FILE, session)
    ballot(1)
    level.Stat("Meditation").level_up()
    done = c(" ✔ Entry Logged Successfully ", "—")
    print(f"\n{done}")
    if from_term: print()

def debrief_review(proxy: bool = False, from_term: 
                   bool = False):
    """
Opens the Debrief Review menu
If proxy=True, it means this was called from another module, so we skip the theme filter to avoid unnecessary nesting

Purpose:
    view logged reflections for analysis (you can 
    copy-paste them to ChatGPT for an in-depth 
    analysis)
    """
    if not proxy:
        line = "—" if from_term else ""
        header = c(' Debrief Review ', line)
        print(f"\n{color(header, 'green')}\n")
    
    options = {
         "View all entries": view_all_entries,
          "Filter by theme": filter_by_theme ,
           "Filter by date": filter_by_date  ,
        "Search by keyword": search_keyword
    }
    
    if proxy:
        options = {
             "View all entries": view_all_entries,
               "Filter by date": filter_by_date  ,
            "Search by keyword": search_keyword
        }
            
    list_options(options)
    
    if proxy: choose(options, 0, debrief_review, 1)
    else    : choose(options, 0, debrief_review)
    
    if from_term: print()

def choose_journal_type() -> tuple:
    """
Prompts the user to choose between viewing Reflections or Shadow Journal entries.

Returns:
  - A string indicating the type ('reflections' or 
    'shadow')
  - The corresponding loaded data
    """
    print()
    types = ["Reflections", "Shadow Journal"]
    list_options(types, "Choose entry type")
    choice = input(color(">>> ", "magenta")).strip()
    if choice == "1":
        return "reflections", storage.load_data(
                storage.REFLECTIONS)
    elif choice == "2":
        return "shadow", storage.load_data(
                storage.JOURNAL)
    
    warning("Invalid choice.")
    return None, []

def view_all_entries(proxy: bool = False):
    """
Displays all entries from either reflections or shadow journals
If proxy=True, it's being called internally (e.g. from another filter), so it skips the journal type selection
    """
    entries = storage.load_data(storage.SERVICES)
    if not proxy:kind, entries = choose_journal_type()
    if not entries: no_data("No entries found")
    if not entries: return
    
    if not proxy: print_entries(entries, kind)
    else        : print_entries(entries)

def filter_by_theme():
    """
Allows user to filter reflection entries by their associated theme
Only applies to reflection-type journals (not shadow work)
    """
    kind, entries = choose_journal_type()
    if not entries: no_data("No entries found")
    if not entries: return

    file   = storage.REFLECTIONS
    themes = storage.get_tables(file, repair=False)

    list_options(storage.get_tables(file), "Choose theme")
    
    try:
        i = int(input(color(">>> ", 'magenta'))) - 1
        if 0 <= i < len(themes):
            print_entries(storage.load_table_as_list(file, 
                          themes[i]), kind)
        else: warning("Invalid choice")
    except EOFError: warning("Invalid input")

def filter_by_date(proxy: bool = False):
    """
Filters journal entries based on a given date
    """
    print()
    entries = storage.load_data(storage.SERVICES)
    
    if not proxy:kind, entries = choose_journal_type()
    if not entries: no_data("No entries found")
    if not entries: return

    date_input = input("\nEnter date (YYYY-MM-DD): "
                 ).strip()
    selected = [e for e in entries if 
                e["Timestamp"].startswith(date_input)]
    if not selected:
        no_data("No entries found for that date")
    else:
        if not proxy:
            print_entries(selected, kind)
            return
        print_entries(selected)

def search_keyword(proxy: bool = False):
    """
Searches journal entries for a user-specified keyword
If proxy=True, the function is being called internally, so it handles data differently.
    """
    print()
    entries = storage.load_data(storage.SERVICES)
    if not proxy:kind, entries = choose_journal_type()
    if not entries: no_data("No entries found")
    if not entries: return

    prompt  = color("Enter keyword to search:","cyan")
    keyword = input(f"\n{prompt} ").lower()
    
    # Match logic varies based on type and proxy status
    def match(entry):
        if kind == "reflections":
            return keyword in entry["Answer"
                   ].lower() or keyword in entry[
                   "Question"].lower()
        elif proxy:
            return keyword in entry["Entry"]["Subject"
                   ].lower() or keyword in entry[
                   "Entry"]["Service"].lower()
        else:
            return any(keyword in str(v).lower() for 
                   k, v in entry.items() if 
                   isinstance(v, str))
    
    selected = [e for e in entries if match(e)]
    if not selected: no_data("No results found")
    else:
        if not proxy:
            print_entries(selected, kind)
            return
        print_entries(selected)

def print_entries(entries: list, kind: str|None=None):
    """
Prints journal entries in a readable format based on entry type.
    kind='reflections': Shows Q&A with theme
         kind='shadow': Shows shadow work prompts
             kind=None: Shows service log style 
                        entries (used in soul_work.py)
    """
    for e in entries:
        print(end="\n\n")
        stamp = timetools.timestamp(e['Timestamp'])
        ago   = timetools.get_time_diff(time(), e['Time'])
        
        labels = label([
            "Date:", "Theme:", "Q:", "A:", 
            "Rendered to:", "Service:"
        ])
        
        print(labels[0], stamp)
        if kind == "reflections":
            question = f'{labels[2]} {e["Question"]}'
            answer   = f'{labels[3]} {e["Answer"]}'            
            print(labels[1], e["Theme"])
            print(wrap(question, 3))
            print(wrap(answer,   3))
        elif not kind:
            subject = f" {e['Entry']['Subject']}"
            service = f" {e['Entry']['Service']}"
            sub     = len(strip_ansi(labels[4]) + 1)
            ser     = len(strip_ansi(labels[5]) + 1)
            print(wrap(f"{labels[4]}{subject}", sub))
            print(wrap(f"{labels[5]}{service}", ser))
        else:
            for k, tag in {
                     "Trigger Event": "Trigger" ,
                "Emotional Response": "Emotion" ,
                          "Reaction": "Reaction",
                      "Deeper Truth": "Truth"   ,
                         "Past Echo": "Past"    ,
                       "Core Belief": "Belief"  ,
                              "Need": "Need"    ,
                           "Reframe": "Reframe" ,
                         "Next Time": "Next"
            }.items():
                legend  = color(f"{tag}:", "cyan")
                content = f"{legend} {e.get(k, '')}"
                print(wrap(content, len(tag)+2))
        print(color("Logged:", "cyan"), ago)
    print(); underline()
