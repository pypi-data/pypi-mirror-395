from tuikit.logictools import make_progress_bar, rated_bar
from tuikit.logictools import copy, visual_width, not_all
from tuikit.textools import pluralize, style_text, label
from tuikit.listools import list_items as list_options
from tuikit.textools import pad_args as format_number
from tuikit.logictools import _wrap_text as wrap_text
from tuikit.textools import iter_print, strip_ansi
from tuikit.console import spacer, clear as _clear
from tuikit.console import underline as _underline
from tuikit.textools import transmit as _transmit
from tuikit.exceptions import warning as _warning
from tuikit.exceptions import empty as no_data
from tuikit.listools import choose as _choose
from tuikit import timetools as tt
from typing import Callable
from . import storage
import shutil
import random
import time
import sys

def lvl_up_msg(cat):
    msg, cap = "", ""
    tense = [["are", "is"], ["have", "has"]]
   
    for i, [f, s] in zip([0, 1], tense):
        text = f"skills {f}" if (cat.endswith("ion")
            or cat.endswith("ing")) else s
        if i == 0: msg += text
        else     : cap += text

    return msg, cap

def ExitError(): return (KeyboardInterrupt, EOFError)

def print_help(at: int = 0, option: str | None = None):
    print()
    if option: print(f"Invalid option: {option!r}\n")
    if not at: 
        print("        Task: use -t or --task")
        print("  Reflection: use -r or --reflect")
        print("Shadow entry: use -s or --shadow")
    elif at == 1:
        print("  Reflections: use -d or --debrief")
        print("Status window: use -w or --status-window")
        print("   Statistics: use -s or --stats")
        print("      Balance: use -b or --balance")
        print(" Bank account: use -a or --account")
        print(" Transactions: use -t or --transactions")
    else:
        print(" Deposit: use -d or --deposit ")
        print("Withdraw: use -w or --withdraw")
    print()

def help_msg(found:bool = False, setup:bool = False):
    try:
        if "--setup" == sys.argv[1]: return
    except IndexError: pass
    args = {
        "log": ["-t", "--task", "-r", "--reflect", "-s",
               "--shadow"],
        "view": ["-d", "--debrief", "-w", 
                "--status-window", "-s", "--stats",
                "-b", "--balance", "-a", "--account",
                "-t", "--transactions"],
        "coffer": ["-d", "--deposit", "-w", "--withdraw"]
    }
    header   = center("《 HABITRAX HELP 》", line="—")
    h        = ["-h", "--h","-help", "--help"]
    commands = ["log", "view", "coffer"]
    cta      = "I see you haven't completed your " \
             + "setup yet. Use entry point without"\
             + " a command and/or with option --setup" \
             + " to complete setup."
    
    if len(sys.argv) == 2:
        if sys.argv[1] in commands: return
    elif len(sys.argv) > 2:
        for i, command in enumerate(commands):
            if command == sys.argv[1]:
                arg = sys.argv[2]
                if arg in args[command] and not setup:
                    return
                print(f"\n{header}")
                print_help(i, None if arg in h else arg)
                if setup:
                    _transmit(cta, speed=0.075,
                               hold=0.075,hue='red')
                    print()
                underline()
                print()
                sys.exit(0)

    for arg in h:
        if arg in sys.argv: found = True
    if not found: return

    cta_for_info = "Use <entry-point command -h/"\
                 + "--help> for options of that command"
    example      = " e.g: python run.py view "\
                 + "--status-window"
    print(f"\n{header}\n")
    print("Entry points:")
    print("      git clone            python run.py")
    print("      as module (pip)      python -m hbx")
    print("      bash direct (pip)    habitrax\n")
    print("Usage:")
    print("      entry-point")
    print("      entry-point command option")
    print(f"{color(example, 'green')}\n")
    print("Commands:")
    print("      log                  Log an activity")
    print("      view                 View information")
    print("      coffer               Personal bank\n")
    print(wrap_text(color(cta_for_info, 'yellow')))
    print()
    if setup:
        _transmit(cta, speed=0.075, hold=0.075, hue='red')
        print()

    underline()
    print()
    sys.exit(0)

def main_menu():
    print(end="\n\n")
    underline()

def generate_otp() -> str:
    number = random.randint(0, 999)
    return str(format_int(number, deno=3))

def money(*args) -> list[str]:
    formatted = []
    for amount in args:
        denomination = len(str(int(amount))) - 1
        formats = [
            f"  {amount:.2f} ",
            f" {amount:.2f} ",
            f"{amount:.2f} ",
            f"  {amount/1e3:.2f}K",
            f" {amount/1e3:.2f}K",
            f"{amount/1e3:.2f}K",
            f"  {amount/1e6:.2f}M",
            f" {amount/1e6:.2f}M",
            f"{amount/1e6:.2f}M"
            f"  {amount/1e9:.2f}B",
            f" {amount/1e9:.2f}B",
            f"{amount/1e9:.2f}B"
        ]
        try: formatted.append(formats[denomination])
        except IndexError: formatted.append("Really?")
    return formatted

def variables(labels: list) -> list[str]:
    print()
    varz = []
    while True:
        try:
            var = int(input(labels[len(varz)]))
            if len(varz) == 0 and 1 <= var <= 10:
                varz.append(var)
                continue
            elif len(varz) == 1 and 0 <= var <= 2:
                varz.append(var)
                break
        except Exception as e:
            if isinstance(e, ExitError()):
                if not isinstance(e, EOFError):print()
                main_menu()
                return
                
        if len(varz) == 0:
           warning("Enter a number between 1 and 10.")
        else: warning("Enter a number between 0 and 2.")
    return varz

def choose(options: list|dict, check:bool = False, 
           src:Callable = None, proxy:bool = False):
    """
Custom input menu for choosing an option from a list.
If check=True, returns index.
If proxy=True, passes (proxy=True) to chosen function.
If user inputs 'clear', resets the source screen.
    """
    return _choose(options, getch=check, src=src, proxy=
           proxy)

def past(string: str) -> str:
    past = string.split()[0].lower()
    if past.endswith("y"):
        past = past.replace("y", "ied")
    elif past.endswith("r"): past += "ed"
    rest = string.split()[1:]
    return f"{past} {' '.join(rest)}"

def choose_from(dictionary: dict, index: str | int):
    """
Takes a dictionary and a numeric index
Returns the corresponding value
    """
    return next((dictionary[opt] for pos, opt in 
           enumerate(dictionary) if pos == int(index)))

def clear(print_header:bool=True, terminate:bool=False):
    _clear()
    if terminate: exit()
    if not print_header: return
    _clear(center("《 QUESTLINE 》", line="="))

def warning(msg, inline=False, transmit=False):
    if not transmit: return _warning(msg, inline=inline)
    print()
    _transmit(msg, hue="yellow")
    print()

def color(text,fg: str|None = None, bg: str|None = None,
          bold:bool = False, underule:bool = False) -> str:
    return style_text(text, fg, bg, bold, bool(underule))   
 
def number_padding(num: int, pad: int = 3) -> str:
    return str(num).rjust(pad)
        
def center(text: str, line: str | None = None, 
           get: bool = False, fixed: int | None = None):
    term_width = shutil.get_terminal_size((80, 
        20)).columns
    display_len = visual_width(text)
    
    # Centers stats in status window
    if fixed: display_len = fixed
    total_pad = max(term_width - display_len, 0)
    left_pad = total_pad // 2
        
    # magic number 56 used to fix termux centering
    # alignement
    left_pad -= 1 if any(char in text for char in 
        ("█", "▒")) and "%" in text and (term_width 
        < 56) else 0
    right_pad = total_pad - left_pad
    if get: return left_pad, total_pad, right_pad

    if line:
        line_color = "magenta" if line == "—" else "green"
        text_color = "magenta" if line != "—" else "green"
        left   = color(line *  left_pad, line_color)   
        right  = color(line * right_pad, line_color)
        middle = color(text, fg=text_color)
        return f"{left}{middle}{right}"
        
    return " " * left_pad + text

def underline() -> None: _underline(hue="magenta")
    
def variance(new: int | float | None, 
             old: int | float | None) -> int | float:
    if old: return ((new - old) / old) * 100
    elif not_all(new, old): return 0
    return 100

def format_int(number, deno: int = 2, form: str = "0"):
    length = len(str(int(float(number))))
    if length < deno:
        fill = (deno - length) * form
        number = f"{fill}{number}"
    return number
    
def get_exp(category: str) -> float:
    data = storage.load_data(storage.DATA_FILE)
    
    exp = 0
    for entry in data:
        if entry["Category"] == category:
            exp += entry["Time spent"]

    return exp
    
def var_per_cat(index: int | None = None, 
             grouped: list | None = None):
    data     = storage.load_data(storage.LEVEL_FILE)
    entry    = data[index]
    now      = time.time()
    last     = entry["Time"]
    lapsed   = timetools.get_time_diff(now, last)
    date     = timetools.timestamp(entry["Timestamp"])
    level    = entry["Level"] * 10
    try: exp = get_exp(entry["Category"])
    except KeyError: return None
    if grouped:
        level, exp = grouped
    progress = exp - (level * 10 if grouped else level)
    exp_pc   = progress / 10 * 100 if level < 1000 else 100
    bar      = make_progress_bar(exp_pc / 100)
    return bar, date, lapsed, exp_pc

def percent_colored(progress: int|float, head="",
                    tail="%") -> str:
    sign = f"+{head}" if progress >= 0 else f"-{head}"
    hue  = "green" if progress >= 0 else "red"
    prog = abs(progress)
    return color(f"{sign}{prog:.2f}{tail}", fg=hue)

class PercentageCalcs:
    def __init__(self):
        self.data = storage.load_data(storage.DATA_FILE)
    
    def get_percent(self):
        prev_total = len(self.data) - 1
        total      = len(self.data)
        
        if prev_total == 0: return tuple(percent_colored
                            (100) for _ in range(3))
        
        time_pc    = percent_colored(variance(self.avg
                     ('Time spent'), self.avg
                     ('Time spent', prev_total)))
        focus_pc   = percent_colored(variance(self.avg
                     ('Focus'), self.avg('Focus', 
                     prev_total)))
        quality_pc = percent_colored(variance(
                     sum(entry['Quality range'][0] for 
                        entry in self.data) / total,
                     sum(entry['Quality range'][0] for 
                        entry in self.data[:prev_total
                        ]) / prev_total
        ))
        return time_pc, focus_pc, quality_pc
    
    def get_grouped_percent(self, data):
        prev_total = len(data)-1
        
        if not prev_total: return copy(percent_colored(100))
        
        time_pc  = percent_colored(variance(self.avg(
                   'Time spent', data=data), self.avg(
                   'Time spent', prev_total, 
                   data=data)))
        focus_pc = percent_colored(variance(self.avg(
                   'Focus', data=data), self.avg(
                   'Focus', prev_total, data=data)))
        
        return time_pc, focus_pc
    
    def avg(self, field, upto=None, data=None):
        data   = self.data if not data else data
        subset = data if upto is None else data[:upto]
        return sum(entry[field] for entry in subset
               ) / len(subset)

class Timetools:
    @staticmethod
    def format_time_passed(timestamp):
        return tt.get_time_lapsed(timestamp)
    
    @staticmethod  
    def format_time(total_time, total=None):
        time = total_time
        if total: time /= total
        return tt.format_time(time, set_to="hour", 
               hue="yellow", only=True, faulty=False)

    @staticmethod  
    def to_iso(timestamp):
        try: return tt.to_iso(timestamp)
        except Exception: return None
    
    @staticmethod  
    def timestamp(iso_str, short=False, spec=False):
        return tt.timestamp(iso_str, short, spec)
        
    @staticmethod  
    def get_age(birthday):
        return tt.get_age(birthday)
    
    @staticmethod  
    def get_time_diff(now, last):
        return tt.time_lapsed(last, now)
        
timetools = Timetools()
pc        = PercentageCalcs()
