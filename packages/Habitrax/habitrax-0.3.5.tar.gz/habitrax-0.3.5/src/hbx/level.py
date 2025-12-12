"""
This module handles all the logic related to leveling
up

Methods:
  - __init__(...)
  - level_up(...)
  - custom_stat_level_up(...)
  - get_rank(...)
  - get_title(...)
  - get_level(...)
  - get_stat_blocks(...)
"""
from .toolbox import number_padding, get_exp, lvl_up_msg
from .toolbox import color, var_per_cat, spacer
from datetime import datetime as dt
from . import stat_logic
from . import storage
import time

MAX_LEVEL = 1000

class Stat:
    def __init__(self, name: str | None = None):
        """
Initializes the exp, level, rank and title if stat name is provided
        """
        if not name: return
        self.name    = name
        self.exp     = get_exp(name)
        self.level   = int(self.exp / 10)
        self.rank    = self.get_rank(self.level)
        self.title   = self.get_title(self.rank)
        self.prv_lvl = self.get_level()

    def level_up(self):
        """
Handles stat creation and user level ups/downs
        """
        level_data = storage.load_data(
                     storage.LEVEL_FILE)
        if not level_data: level_data = []

        found = False
        for entry in level_data[1:]:
            if entry["Category"]  == self.name:
                found              = True
                new_level          = self.level
                entry["Time"]      = time.time()
                entry["Level"]     = new_level
                entry["Timestamp"] = dt.now()\
                                       .isoformat()
                self.custom_stat_level_up()
                break

        if not found:
            level_data.append({
                 "Category": self.name           ,
                    "Level": self.level          ,
                "Timestamp": dt.now().isoformat(),
                     "Time": time.time()
            })
            print("\n"+color(f"New category {self.name!r} "
                + f"added at level {self.level}", 
                  "yellow"))
        
        storage.save_data(storage.LEVEL_FILE, 
            level_data)
        
        new_lvl = self.get_stat_blocks()[0]
        if self.prv_lvl < new_lvl:
            n = color(f"You are now level {new_lvl}!", 
                'yellow')
            print(f"\n{color('Level up!', 'yellow')}")
            print(f"\n{n}")
            user_lvl = level_data[0]
            user_lvl["Level"]     = new_lvl
            user_lvl["Timestamp"] = dt.now().isoformat()
            user_lvl["Time"]      = time.time()
        elif self.prv_lvl > new_lvl:
            w = color('Level re-adjustment!', 'red')
            n = color(f"Level re-adjusted to ", "red")
            r = color(f"{new_lvl} from {self.prv_lvl}"
                , 'red')
            print(f"\n{w}\n\n{n}{r}")          
            user_lvl = level_data[0]
            user_lvl["Level"]     = new_lvl
            user_lvl["Timestamp"] = dt.now().isoformat()
            user_lvl["Time"]      = time.time()
        storage.save_data(storage.LEVEL_FILE, 
            level_data)

    def custom_stat_level_up(self):
        """Handles stat level up"""
        stats_level = storage.load_data(storage.S_LVL)
        blocks      = self.get_stat_blocks()
        skills      = [key for key in 
                      stat_logic.get_resolved_stats()]

        if not stats_level:
            for block in blocks[1:][0]:
                stats_level.append({
                    "Name": block["Short"],
                    "Level": block["Raw"]
                })
        
        for index, stat in enumerate(stats_level):
            skill = skills[index].lower()
            msg, cap = lvl_up_msg(skill)
            for block in blocks[1:][0]:
                if stat["Name"] == block["Short"]:
                    lvl = block["Raw"]
                    if stat["Level"] < lvl < 1000:
                        print(color(
                            '\nStat level up!\n', 
                            'yellow'))
                        print(color(
                            f"Your {skill} {msg} now", 
                            "yellow"), end=color(
                            " level ", "yellow"))
                        print(color(f"{lvl}!", 
                            "yellow"))
                    elif lvl == 1000:
                        print(color(
                            '\nStat level up!\n', 
                            'yellow'))
                        print(color(
                            f"Your {skill} {cap}", 
                            "yellow"), end=color(
                            " reached "))
                        print(color("max level!",
                            "yellow"))
                    stat["Level"] = lvl
       
        storage.save_data(storage.S_LVL, stats_level)
    
    @staticmethod
    def get_rank(level: int) -> str:
        # F-rank block
        if level <  10: return "FFF"
        if level <  50: return "FF"
        if level < 100: return "F"

        # Tiered ranks
        tiers = [
            ("E", 100), ("D", 200), 
            ("C", 300), ("B", 400)
        ]
        for rank, base in tiers:
            if base <= level < base + 10: 
                return rank
            if base + 10 <= level < base + 50: 
                return rank * 2
            if base + 50 <= level < base + 100: 
                return rank * 3
        
        # A-rank block
        if 500 <= level < 520: return "A"
        if 520 <= level < 600: return "AA"
        if 600 <= level < 700: return "AAA"

        # S-rank block
        if 700 <= level <  800: return "S"
        if 800 <= level <  900: return "SS"
        if 900 <= level < 1000: return "SSS"

        return "Z"

    @staticmethod
    def get_title(rank: str) -> str:
        titles = {
            "FFF": "Trashiest of Trash"    ,
             "FF": "Wandering Newbie"      ,
              "F": "Curious Fledgling"     ,
              "E": "Focused Novice"        ,         
             "EE": "Intentional Amateur"   , 
            "EEE": "Consistency Embodiment",            
              "D": "System Crafter"        ,
             "DD": "Growth Enthusiast"     ,
            "DDD": "Structured Mind"       ,
              "C": "Studious Operator"     ,
             "CC": "Tactical Executor"     ,
            "CCC": "Deep Worker"           ,
              "B": "Workflow Architect"    ,
             "BB": "Self-Mastery Adept"    ,
            "BBB": "Mental Mechanic"       ,
              "A": "Focused Virtuoso"      ,
             "AA": "Meta-Thinker"          ,
            "AAA": "Multi-domain Achiever" ,
              "S": "Discipline Demi-God"   ,
             "SS": "Flow Incarnate"        ,
            "SSS": "Realm Architect"       ,
              "Z": "Transcendental"
        }
        return titles.get(rank)
        
    @staticmethod
    def get_level() -> int:
        """Initializes and/or retrieves user level"""
        data = storage.load_data(storage.LEVEL_FILE)
        if not data:
            data = [{
                "Level": 0,
                "Timestamp": dt.now().isoformat(),
                "Time": time.time()
            }]
        
        if len(data[0]) != 3:
            data.insert(0, {
                "Level": 0,
                "Timestamp": dt.now().isoformat(),
                "Time": time.time()
            }) 
        
        storage.save_data(storage.LEVEL_FILE, data)
        return data[0]["Level"]

    def get_stat_blocks(self) -> tuple[int, list]:
        """
Creates stat block per task category
Each block has: <name> <level> <exp bar> <stat rank>
        """
        resolved = stat_logic.get_resolved_stats()
        blocks = []

        total_exp = 0
        for index, (name, stats) in enumerate(
                resolved.items()):
            group_exp = sum(get_exp(stat) for 
                stat in stats)
            total_exp += group_exp        
            level = min(int(group_exp / 10), 1000)
            weigh = level if level != 1000 else "MAX"
            weight = number_padding(weigh)
            bar = var_per_cat(1, [level, 
                group_exp])[0]
            short=name[:3] if name[:3]!="Ope"else"Ops"
            rank = self.get_rank(level)

            blocks.append({
                "Short": short,
                "Rank": rank,
                "Raw": weigh,
                "Weight": weight,
                "Bar": bar,
                "Index": index
            })
    
        total = len(resolved)
        level = min(int(total_exp / 10 / total), 
                1000) if total else 0

        return level, blocks
