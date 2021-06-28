import sqlite3

from PyQt5.QtCore import QDateTime

from datetime import datetime

class DatabaseHelper(object):
    def __init__(self, name=None):
        self.conn = None
        self.cursor = None
        if name:
            self.open(name)
        
    def open(self,name):
        try:
            self.conn = sqlite3.connect(name)
            self.cursor = self.conn.cursor()

        except sqlite3.error as e:
            print("error connecting to database!") 

    def close(self):
        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self,exc_type,exc_value,traceback):
        self.close() 

    # def get(self,table,columns,limit=None):
    #     query = "SELECT {0} from {1};".format(columns,table)
    #     self.cursor.execute(query)
    #     # fetch data
    #     rows = self.cursor.fetchall()
    #     return rows[len(rows)-limit if limit else 0:]
    
    def get_sql(self,sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    # def write(self,table,columns,data):
    #     query = "INSERT INTO {0} ({1}) VALUES ({2});".format(table,columns,data)
    #     self.cursor.execute(query)

    def execute_single(self,query,param=None):
        if param is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query,param)
    
    def execute_script(self,query):
        self.cursor.executescript(query)

class Database(object):
    def __init__(self,db_name="database.db"):
        self.name = db_name
        self.create_tables()
        self.set_up_defaults()
        self.check_active_user()
    
    def create_tables(self):
        with DatabaseHelper(self.name) as db:
            query = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER AUTO_INCREMENT,
                name VARCHAR,
                is_active BOOLEAN,
                PRIMARY KEY (id)
            );
            CREATE TABLE IF NOT EXISTS languages (
                id INTEGER AUTO_INCREMENT,
                name VARCHAR,
                user_id INTEGER,
                PRIMARY KEY (id)
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER AUTO_INCREMENT,
                user_id INTEGER,
                name VARCHAR,
                value VARCHAR,
                PRIMARY KEY (id)
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
            CREATE TABLE IF NOT EXISTS highlighters (
                id INTEGER AUTO_INCREMENT,
                user_id INTEGER,
                color VARCHAR,
                style VARCHAR,
                name VARCHAR,
                PRIMARY KEY (id)
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
            CREATE TABLE IF NOT EXISTS online_tools (
                id INTEGER AUTO_INCREMENT,
                title VARCHAR,
                url VARCHAR,
                user_id INTEGER,
                lang_id INTEGER,
                PRIMARY KEY (id)
                FOREIGN KEY (user_id) REFERENCES users (id)
                FOREIGN KEY (lang_id) REFERENCES languages (id)
            );
            CREATE TABLE IF NOT EXISTS flashcards (
                id INTEGER AUTO_INCREMENT,
                user_id INTEGER,
                front VARCHAR,
                back VARCHAR,
                back_image VARCHAR,
                language_id INTEGER,
                PRIMARY KEY (id)
                FOREIGN KEY (user_id) REFERENCES users (id)
                FOREIGN KEY (language_id) REFERENCES languages (id)
            );
            CREATE TABLE IF NOT EXISTS vocabulary (
                id INTEGER AUTO_INCREMENT,
                user_id INTEGER,
                term VARCHAR,
                language_id INTEGER,
                definition VARCHAR,
                highlighter_id INTEGER,
                is_regex BOOLEAN,
                created_at DATE,
                PRIMARY KEY (id)
                FOREIGN KEY (user_id) REFERENCES users (id)
                FOREIGN KEY (language_id) REFERENCES languages (id)
                FOREIGN KEY (highlighter_id) REFERENCES highlighters (id)
            );
            CREATE TABLE IF NOT EXISTS recent_files (
                id INTEGER,
                filepath VARCHAR,
                created_at SMALLDATETIME,
                user_id INTEGER,
                PRIMARY KEY (id)
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
            """
            db.execute_script(query)
    
    def set_up_defaults(self):
        default_user = """
        INSERT OR REPLACE INTO users(id,name) VALUES (:id,:name)
        """
        default_user_param = (1,"default_user")

        default_lang = """
        INSERT OR REPLACE INTO languages(id,name,user_id) VALUES (:id,:name,:user_id)
        """
        default_lang_param = (1,"Indonesian",1)

        with DatabaseHelper(self.name) as db:
            db.execute_single(default_user, default_user_param)
            db.execute_single(default_lang, default_lang_param)
        
        
    def check_active_user(self):
        with DatabaseHelper(self.name) as db:
            active_user = db.get_sql("SELECT * FROM users WHERE is_active = true")
            # active_user = db.get_sql("SELECT * FROM users ")
            if active_user == []: #the program is probably being run for the first time
                default_user = """
                INSERT OR REPLACE INTO users(id,name,is_active) VALUES (:id,:name,:is_active)
                """
                default_user_param = (1,"default_user",True)
                db.execute_single(default_user, default_user_param)
    
    def get_active_user(self):
        with DatabaseHelper(self.name) as db:
            return db.get_sql("SELECT * FROM users WHERE is_active=1")

    def add_recent_file(self,filepath):
        active_user_id = self.get_active_user()[0][0]
        date_time = datetime.now()
        # delete older instances of same file
        with DatabaseHelper(self.name) as db:
            check = db.get_sql(f"SELECT * FROM recent_files WHERE filepath ='{filepath}'")
            if check == []:
                with DatabaseHelper(self.name) as db:
                    sql = "INSERT INTO recent_files (filepath,created_at,user_id) VALUES (:filepath,:created_at,:user_id)"
                    params = (filepath,date_time,active_user_id)
                    db.execute_single(sql, params)

            elif len(check[0]) > 0: #check if there is already an entry
                with DatabaseHelper(self.name) as db:
                    old_id = check[0][0]
                    sql = "REPLACE INTO recent_files (id,filepath,created_at,user_id) VALUES (:id,:filepath,:created_at,:user_id)"
                    params = (old_id,filepath,date_time,active_user_id)
                    db.execute_single(sql, params)




        
        print(self.latest_recent_files())
    
    def latest_recent_files(self):
        with DatabaseHelper(self.name) as db:
            return db.get_sql("SELECT * FROM recent_files ORDER BY created_at DESC LIMIT 10")
            

class SettingsData(object):
    """data model for settings"""
    _darktheme = False
    _autofill_flashcard = True
    _current_language = ""

    def set_darktheme(self,val):
        self._darktheme = val
    
    def set_autofill_flashcard(self,val):
        self._autofill_flashcard = val
    
    def set_current_language(self,lang):
        self._current_language = lang

    def get_darktheme(self):
        return self._darktheme
    
    def get_autofill_flashcard(self):
        return self._autofill_flashcard
    
    def get_current_language(self):
        return self._current_language