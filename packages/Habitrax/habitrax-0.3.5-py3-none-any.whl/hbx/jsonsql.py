from tuikit.listools import flatten, normalize
from tuikit.logictools import any_in
from pathlib import Path
import sqlite3 as sql
import json
import os

# Dynamically resolve the main folder
DATA_DIR = Path(__file__).parent / "data"

# Load data safely from a file
def load_data(file:str) -> list | dict:
    file_path = DATA_DIR / file
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def load_table(table:str, cur:sql.Cursor, _type:int = 1
              ) -> list[dict]:
    data = []
    for row in cur.execute(f"SELECT * FROM {table}"):
        entry = {}
        if _type == 1:            
            entry["Timestamp"]     = row[0]
            entry["Task"]          = row[1]
            entry["Focus"]         = row[2]
            entry["Fuzziness"]     = row[3]
            entry["Time spent"]    = row[4]
            entry["Quality range"] = eval(row[5])
        elif _type == 2:
            entry["Timestamp"] = row[0]
            entry["Question"]  = jsonsql._sql_repr(row[1])
            entry["Answer"]    = jsonsql._sql_repr(row[2])
            entry["Theme"]     = jsonsql._sql_repr(table)
            entry["Time"]      = float(row[3])
        data.append(entry)
    
    return data

def load_table_as_list(file:str, table:str) -> list[dict]:
    db_name = file.replace(".json", ".db")
    if not os.path.exists(DATA_DIR / db_name): 
        jsonsql.migrate_to_sql(file)    
    data = load_data(file)
    db   = sql.connect(str(DATA_DIR / db_name))
    cur  = db.cursor()
    if "log_data" in file: return load_table(table, cur, 1)
    elif "reflec" in file: return load_table(table, cur, 2)

def get_tables(file:str, repair:bool = True) -> list[str]:
    db_name = file.replace(".json", ".db")
    if not os.path.exists(DATA_DIR / db_name): 
        jsonsql.migrate_to_sql(file)        
    db = sql.connect(str(DATA_DIR / db_name))
    cr = db.cursor()
    tl = cr.execute(f"SELECT tbl_name FROM sqlite_master")
    if not repair: return normalize(flatten(tl))
    return normalize(flatten(tl), use=jsonsql._sql_repr)

class JsonSQL:
    @staticmethod
    def _sql_clean(*args, table:bool = True) -> str:
        if not table:
            if len(args) == 1:
                a = args[0].replace("'m", "’m")
                return args[0].replace("'s", "’s")
            a = args[0].replace("'", "’")
            b = args[1].replace("'", "’")
            return a, b
        
        args = args[0]   
        args = args.replace("&", "and")
        args = args.replace(" ", "_")
        return args.replace("-", "–")

    @staticmethod
    def _sql_repr(text:str) -> str:
        text = text.replace("_and_", " & ")
        text = text.replace("–", "-")
        text = text.replace("_", " ")
        return text

    def add(self, cur: sql.Cursor, table:str, stamp:str, 
            **kw: dict) -> None:
        table = self._sql_clean(table)
        rows  = cur.execute(f"SELECT * FROM {table}")
        keys  = [repr(row[0]) for row in rows]
        if stamp in keys: return
        if len(kw) > 3:
            task, focus, fuzz, durata, qlty = kw.values()
            task = self._sql_clean(task, table=False)
            cur.execute(f"""INSERT INTO {table} VALUES
                        ({stamp}, {task}, {focus}, {fuzz}, 
                         {durata}, '{qlty}')""")
        else:
            qstn, answer, time = kw.values()
            qstn, answer = self._sql_clean(qstn, answer,
                           table=False)
            cur.execute(f"""INSERT INTO {table} VALUES
                        ({stamp}, {repr(qstn)}, 
                         {repr(answer)}, {time})""")
    
    def migrate_log_data(self, data:list[dict], 
                         db:sql.Connection, cur:sql.Cursor
                         ) -> None:  
        tables  = []
        for entry in data:
            cat = entry["Category"]
            if cat not in tables: tables.append(cat)
    
        for table in tables:
            try: cur.execute(f"""CREATE TABLE {table}
                    (timestamp text, task text,focus real, 
                     fuzziness real, duration real, 
                     quality_range text,
                     CONSTRAINT pk_{table.lower()} PRIMARY 
                     KEY (timestamp))""")
            except sql.OperationalError: pass
    
        for entry in data:
            table  = entry["Category"]
            stamp  = repr(entry["Timestamp"])
            task   = repr(entry["Task"])
            focus  = repr(entry["Focus"])
            fuzz   = repr(entry["Fuzziness"])
            durata = repr(entry["Time spent"])
            qlty   = repr(entry["Quality range"])
            self.add(cur, table, stamp, task=task, 
                     focus=focus, fuzz=fuzz, durata=durata, 
                     qlty=qlty)

    def migrate_reflections(self, data:list[dict], 
                         db:sql.Connection, cur:sql.Cursor
                         ) -> None:
        tables  = []
        for entry in data:
            cat = entry["Theme"]
            if cat not in tables: tables.append(cat)
    
        for table in tables:
            table = self._sql_clean(table)
            try: cur.execute(f"""CREATE TABLE {table}
                    (timestamp text, question text, 
                     answer text, time text,
                     CONSTRAINT pk_{table.lower()} PRIMARY 
                     KEY (timestamp))""")
            except sql.OperationalError: pass
    
        for entry in data:
            table  = entry["Theme"]
            stamp  = repr(entry["Timestamp"])
            qstn   = entry["Question"]
            answer = entry["Answer"]
            time   = repr(entry["Time"])
            self.add(cur, table, stamp, qstn=qstn, 
                     answer=answer, time=time)  

    def migrate_to_sql(self, file:str, 
                       data:list[dict]|None = None)-> None:
        db_name = file.replace(".json", ".db")
        path    = DATA_DIR / db_name
        if not os.path.exists(path): data = load_data(file)        
        db  = sql.connect(str(path))
        cur = db.cursor()
        
        if "log_data" in file: 
            self.migrate_log_data(data, db, cur)
        elif "reflect" in file: 
            self.migrate_reflections(data, db, cur)
        
        db.commit()
        db.close()
    
jsonsql = JsonSQL() 
