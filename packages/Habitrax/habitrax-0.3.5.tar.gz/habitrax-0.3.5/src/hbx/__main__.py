from . import logger, status_window, debrief
from . import stats, soul_work, toolbox
from .main import main as menu
import argparse
import sys

def parse_args() -> argparse.ArgumentParser:
    parser         = argparse.ArgumentParser(description=
                     toolbox.help_msg())
    subparsers     = parser.add_subparsers(dest="command")
    session        = subparsers.add_parser("log")
    view           = subparsers.add_parser("view")
    bank           = subparsers.add_parser("coffer")
    
    comparsers = {
       "adders": [session.add_argument,
                  view.add_argument,
                  bank.add_argument],
       
       "cargs": [# session parser
                 [["-t", "--task"],
                  ["-r", "--reflect"], 
                  ["-s", "--shadow"]], 
                
                # view parser
                 [["-d", "--debrief"], 
                  ["-w", "--status-window"],
                  ["-s", "--stats"],
                  ["-b", "--balance"], 
                  ["-t", "--transactions"], 
                  ["-a", "--account"]], 
                
                # bank parser
                 [["-d", "--deposit"],
                  ["-w", "--withdraw"]]
                ]
    }
    
    adders, cargs = comparsers["adders"],comparsers["cargs"]
    for add_arg, args in zip(adders, cargs):
        for arg in args:
            short, long = arg
            add_arg(short, long, action="store_true")
    
    return parser.parse_args()

def main():
    args = parse_args()
    if not args.command: sys.exit(menu())
    
    if args.command == "log":
        if args.reflect: debrief.reflect(True)
        elif  args.task: logger.log_session(True)
        else           : debrief.shadow_journal(True)
    elif args.command == "view":
        if   args.debrief: debrief.debrief_review(0, 1)
        elif args.status_window: status_window.window(1)
        elif   args.stats: stats.menu(True)
        elif args.balance: soul_work.coffer(view=0)
        elif args.account: soul_work.coffer(view=1)
        else             : soul_work.coffer(view=2)
    else:
        if args.withdraw: soul_work.coffer(cashflow=0)
        else            : soul_work.coffer(cashflow=1)

if __name__ == "__main__": main()
