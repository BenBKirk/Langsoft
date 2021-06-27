import sqlite3


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

    def get(self,table,columns,limit=None):
        query = "SELECT {0} from {1};".format(columns,table)
        self.cursor.execute(query)
        # fetch data
        rows = self.cursor.fetchall()
        return rows[len(rows)-limit if limit else 0:]
    
    def get_sql(self,sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def write(self,table,columns,data):
        query = "INSERT INTO {0} ({1}) VALUES ({2});".format(table,columns,data)
        self.cursor.execute(query)

    def query(self,sql):
        self.cursor.execute(sql)
    

class Database(object):
    def __init__(self,db_name="database.db"):
        self.name = db_name
        # self.helper = DatabaseHelper(self.name)
        self.create_tables()
    
    def create_tables(self):
        with DatabaseHelper(self.name) as db_helper:
            query = """
            CREATE TABLE IF NOT EXISTS users (
                id Integer,
                name VARCHAR,
                PRIMARY KEY (id)
            )
            CREATE TABLE IF NOT EXISTS languages (
                id INTEGER,
                name VARCHAR,
                user_id INTEGER,
                PRIMARY KEY (id)
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER,
                user_id INTEGER,
                name VARCHAR,
                value VARCHAR,
                default VARCHAR,
                PRIMARY KEY (id)
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            CREATE TABLE IF NOT EXISTS highlighters (
                id INTEGER,
                user_id INTEGER,
                color VARCHAR,
                style VARCHAR,
                name VARCHAR,
                PRIMARY KEY (id)
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            CREATE TABLE IF NOT EXISTS online_tools (
                id INTEGER,
                title VARCHAR,
                url VARCHAR,
                user_id,
                PRIMARY KEY (id)
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            CREATE TABLE IF NOT EXISTS flashcards (
                id INTEGER,
                user_id INTEGER,
                front VARCHAR,
                back VARCHAR,
                back_image VARCHAR,
                language_id INTEGER,
                PRIMARY KEY (id)
                FOREIGN KEY (user_id) REFERENCES users (id)
                FOREIGN KEY (language_id) REFERENCES languages (id)
                
            )
            CREATE TABLE IF NOT EXISTS vocabulary (
                id INTEGER,
                user_id INTEGER,
                term VARCHAR,
                language_id INTEGER,
                definition VARCHAR,
                highlighter_id INTEGER,
                is_regex BOOLEAN,
                PRIMARY KEY (id)
                FOREIGN KEY (user_id) REFERENCES users (id)
                FOREIGN KEY (language_id) REFERENCES languages (id)
                FOREIGN KEY (highlighter_id) REFERENCES highlighters (id)
            )
            """
            db_helper.query(query)
    
    def set_up_defaults(self):
        pass

            



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