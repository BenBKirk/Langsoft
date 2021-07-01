import sqlite3
from PyQt5.QtCore import QDateTime
from datetime import datetime
import os

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
        if not os.path.exists(os.path.join(os.getcwd(),db_name)):
            print("create new database")
            self.create_tables()
            self.set_up_default_user()
            self.set_up_default_online_tools()
        self.check_active_user()
    
    def create_tables(self):
        with DatabaseHelper(self.name) as db:
            query = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER,
                name VARCHAR,
                is_active BOOLEAN,
                PRIMARY KEY (id)
            );
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER,
                user_id INTEGER,
                name VARCHAR,
                value VARCHAR,
                PRIMARY KEY (id)
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
            CREATE TABLE IF NOT EXISTS highlighters (
                id INTEGER,
                user_id INTEGER,
                color VARCHAR,
                style VARCHAR,
                name VARCHAR,
                PRIMARY KEY (id)
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
            CREATE TABLE IF NOT EXISTS online_tools (
                id INTEGER,
                title VARCHAR,
                url VARCHAR,
                user_id INTEGER,
                PRIMARY KEY (id)
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
            CREATE TABLE IF NOT EXISTS flashcards (
                id INTEGER,
                user_id INTEGER,
                front VARCHAR,
                back VARCHAR,
                back_image VARCHAR,
                PRIMARY KEY (id)
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
            CREATE TABLE IF NOT EXISTS vocabulary (
                id INTEGER,
                user_id INTEGER,
                term VARCHAR,
                definition VARCHAR,
                highlighter_id INTEGER,
                is_regex BOOLEAN,
                created_at DATE,
                PRIMARY KEY (id)
                FOREIGN KEY (user_id) REFERENCES users (id)
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
    
    def set_up_default_user(self):
        default_user = "INSERT OR REPLACE INTO users(id,name) VALUES (:id,:name)"
        default_user_param = (1,"default_user")
        with DatabaseHelper(self.name) as db:
            db.execute_single(default_user, default_user_param)

    def set_up_default_online_tools(self,user_id=1):
        default_online_tools1 = "INSERT OR REPLACE INTO online_tools(title,url,user_id) VALUES (:title,:url,:user_id);"
        default_online_tools_param1 = ("Google Translate WORD","https://translate.google.com/?sl=id&tl=en&text=WORD&op=translate",user_id)
        default_online_tools2 = "INSERT OR REPLACE INTO online_tools(title,url,user_id) VALUES (:title,:url,:user_id);"
        default_online_tools_param2 = ("Google Translate SENT","https://translate.google.com/?sl=id&tl=en&text=SENT&op=translate",user_id)
        default_online_tools3 = "INSERT OR REPLACE INTO online_tools(title,url,user_id) VALUES (:title,:url,:user_id);"
        default_online_tools_param3 = ("Google Images","https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q=WORD",user_id)
        default_online_tools4 = "INSERT OR REPLACE INTO online_tools(title,url,user_id) VALUES (:title,:url,:user_id);"
        default_online_tools_param4 = ("Globse","https://glosbe.com/id/en/WORD",user_id)
        default_online_tools5 = "INSERT OR REPLACE INTO online_tools(title,url,user_id) VALUES (:title,:url,:user_id);"
        default_online_tools_param5 = ("KBBI","https://kbbi.web.id/WORD",user_id)
        with DatabaseHelper(self.name) as db:
            db.execute_single(default_online_tools1, default_online_tools_param1)
            db.execute_single(default_online_tools2, default_online_tools_param2)
            db.execute_single(default_online_tools3, default_online_tools_param3)
            db.execute_single(default_online_tools4, default_online_tools_param4)
            db.execute_single(default_online_tools5, default_online_tools_param5)

        
    def check_active_user(self):
        with DatabaseHelper(self.name) as db:
            active_user = db.get_sql("SELECT * FROM users WHERE is_active = 1")
            print(f"the active user is {active_user}")
            # active_user = db.get_sql("SELECT * FROM users ")
            if active_user == []: #the program is probably being run for the first time
                print("looks like the program is running for the first time")
                default_user = """
                INSERT OR REPLACE INTO users(id,name,is_active) VALUES (:id,:name,:is_active)
                """
                default_user_param = (1,"default_user",True)
                db.execute_single(default_user, default_user_param)
                self.active_user_id = 1
            else:
                self.active_user_id = active_user[0][0]
            
    
    def change_active_user(self,new_active_user):
        # find the active user and set them to inactive
        with DatabaseHelper(self.name) as db:
            sql_for_setting_all_to_inactive = "UPDATE users SET is_active = false WHERE is_active = true"
            db.execute_single(sql_for_setting_all_to_inactive)
            sql_to_make_user_active = f"UPDATE users SET is_active = true WHERE name='{new_active_user}'"
            db.execute_single(sql_to_make_user_active )
        # find the selected user and set them to active
        print("active user updated")
        self.check_active_user() # so that self.active_user is updated
    
    # def set_active_user(self):
    #     with DatabaseHelper(self.name) as db:
    #         active_user_id = db.get_sql("SELECT * FROM users WHERE is_active=1 LIMIT 1")
    #         self.active_user = active_user_id
    #         print(active_user_id)

    def add_recent_file(self,filepath):
        date_time = datetime.now()
        with DatabaseHelper(self.name) as db:
            check = db.get_sql(f"SELECT * FROM recent_files WHERE filepath ='{filepath}'")
            if check == []: #it must be a new file
                with DatabaseHelper(self.name) as db:
                    sql = "INSERT INTO recent_files (filepath,created_at,user_id) VALUES (:filepath,:created_at,:user_id)"
                    params = (filepath,date_time,self.active_user_id)
                    db.execute_single(sql, params)

            elif len(check[0]) > 0: # replace the old entry
                with DatabaseHelper(self.name) as db:
                    old_id = check[0][0]
                    sql = "REPLACE INTO recent_files (id,filepath,created_at,user_id) VALUES (:id,:filepath,:created_at,:user_id)"
                    params = (old_id,filepath,date_time,self.active_user_id)
                    db.execute_single(sql, params)
    
    def get_latest_recent_files(self):
        with DatabaseHelper(self.name) as db:
            return db.get_sql("SELECT * FROM recent_files ORDER BY created_at DESC LIMIT 10")
    
            
    def get_dict_settings(self):
        with DatabaseHelper(self.name) as db:
            print(f"trying to get dict settings for - user:{self.active_user_id}")
            return db.get_sql(f"SELECT * FROM online_tools WHERE user_id = {self.active_user_id}")
    
    def get_all_users_sorted_by_active(self):
        with DatabaseHelper(self.name) as db:
            data = db.get_sql(f"SELECT * FROM users ORDER BY is_active DESC")
            return data

    def add_new_user(self, user):
        new_user_name = user
        # check if user already exists
        with DatabaseHelper(self.name) as db:
            result = db.get_sql(f"SELECT * FROM users WHERE name = '{new_user_name}'")
        if result != []: 
            print("user name already exists!")
        else:# new user can be added
            with DatabaseHelper(self.name) as db:
                sql = "INSERT INTO users(name,is_active) VALUES (:name,:is_active)"
                params = (new_user_name,False)
                db.execute_single(sql, params)




    # def get_discourse_settings(self):
    #     with DatabaseHelper(self.name) as db:
    #         data = db.get_sql(f"SELECT * FROM highlighters WHERE user_id = {self.active_user} AND lang_id ={self.active_lang}")
    #         return data

        


class SettingsData(object):
    """
    This stores the data temporarily, so that we don't have to query the database for everything.
    """
    def __init__(self,user_id=None):
        if user_id:
            self.load_user_data()
    
    def load_user_data(self):
        pass
    

    


