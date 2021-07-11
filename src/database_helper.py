import sqlite3
from datetime import datetime
import os
import logging
logging.basicConfig(level=logging.DEBUG,filename="app.log",format='%(asctime)s - %(levelname)s - %(message)s')

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
            logging.exception("sql database")
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
            self.create_tables()
            self.set_up_default_user()
            self.set_up_default_online_tools()
            self.set_up_default_settings()
            self.set_up_default_highlighters()
            self.set_up_default_grammar_rules()
    
    def create_tables(self):
        with DatabaseHelper(self.name) as db:
            query = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER,
                name VARCHAR,
                PRIMARY KEY (id)
            );
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER,
                name VARCHAR,
                value BOOLEAN,
                user_id INTEGER,
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
                audio_start INTEGER,
                audio_end INTEGER,
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
            CREATE TABLE IF NOT EXISTS grammar_rules (
                id INTEGER,
                user_id,
                is_enabled BOOLEAN,
                name VARCHAR,
                color VARCHAR,
                opacity FLOAT,
                style VARCHAR,
                list VARCHAR,
                PRIMARY KEY (id)
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
            CREATE TABLE IF NOT EXISTS recent_files (
                id INTEGER,
                filepath VARCHAR,
                created_at SMALLDATETIME,
                user_id INTEGER,
                PRIMARY KEY (id)
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
            CREATE TABLE IF NOT EXISTS last_user (
                id INTEGER,
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

    def set_up_default_settings(self,user_id=1):
        default_settings1 = "INSERT OR REPLACE INTO settings(name,value,user_id) VALUES (:name,:value,:user_id)"
        default_settings_param1 = ("dark_theme",False,user_id)
        default_settings2 = "INSERT OR REPLACE INTO settings(name,value,user_id ) VALUES (:name,:value,:user_id)"
        default_settings_param2 = ("autofill_back_of_flashcard",True,user_id)
        with DatabaseHelper(self.name) as db:
            db.execute_single(default_settings1,default_settings_param1)
            db.execute_single(default_settings2,default_settings_param2)
    
    def set_up_default_highlighters(self,user_id=1):
        default_highlighter1 = "INSERT OR REPLACE INTO highlighters(user_id,color,style,name) VALUES (:user_id,:color,:style,:name)"
        default_highlighter_param1 = (user_id,"255,0,0,0.8","underline","unknown-sent")
        default_highlighter2 = "INSERT OR REPLACE INTO highlighters(user_id,color,style,name) VALUES (:user_id,:color,:style,:name)"
        default_highlighter_param2 = (user_id,"255,255,0,0.8","underline","semi-known-sent")
        default_highlighter3 = "INSERT OR REPLACE INTO highlighters(user_id,color,style,name) VALUES (:user_id,:color,:style,:name)"
        default_highlighter_param3 = (user_id,"0,255,0,0.5","underline","known-sent")
        default_highlighter4 = "INSERT OR REPLACE INTO highlighters(user_id,color,style,name) VALUES (:user_id,:color,:style,:name)"
        default_highlighter_param4 = (user_id,"255,0,0,0.4","background","unknown")
        default_highlighter5 = "INSERT OR REPLACE INTO highlighters(user_id,color,style,name) VALUES (:user_id,:color,:style,:name)"
        default_highlighter_param5 = (user_id,"255,255,0,0.4","background","semi-known")
        default_highlighter6 = "INSERT OR REPLACE INTO highlighters(user_id,color,style,name) VALUES (:user_id,:color,:style,:name)"
        default_highlighter_param6 = (user_id,"0,255,0,0.1","background","known")
        with DatabaseHelper(self.name) as db:
            db.execute_single(default_highlighter1, default_highlighter_param1)
            db.execute_single(default_highlighter2, default_highlighter_param2)
            db.execute_single(default_highlighter3, default_highlighter_param3)
            db.execute_single(default_highlighter4, default_highlighter_param4)
            db.execute_single(default_highlighter5, default_highlighter_param5)
            db.execute_single(default_highlighter6, default_highlighter_param6)
    
    def set_up_default_grammar_rules(self,user_id=1):
        default_rule1 = "INSERT OR REPLACE INTO grammar_rules(user_id,is_enabled,name,color,opacity,style,list) VALUES (:user_id,:is_enabled,:name,:color,:opacity,:style,:list)"
        default_rule_param1 = (user_id,True,"Connectors","255,0,0",0.4,"highlight","dengan, juga, tetapi, dan, atau, nah")
        default_rule2 = "INSERT OR REPLACE INTO grammar_rules(user_id,is_enabled,name,color,opacity,style,list) VALUES (:user_id,:is_enabled,:name,:color,:opacity,:style,:list)"
        default_rule_param2 = (user_id,True,"passive voice :)","0,255,0",0.8,"underline","(?!\\bdian\\b|\\bdiam\\b|\\bdiam\\b|\\bdia\\b|\\bdinah\\b|\\bdiri(nya|mu|ku)?\\b)di\\w+\\b|\\b(yang|itu|ini)(?<!setelah itu)(\\s)?(tidak|enggak|tak|nggak|)?(sudah|telah|belum|akan)?\\s(saya|kami|kita|dia|ibu|bapak|mereka|pak\\s\\w+|ibu\\s\\w+|bu\\s\\w+)\\s\\w+(kan|i)?")
        default_rule3 = "INSERT OR REPLACE INTO grammar_rules(user_id,is_enabled,name,color,opacity,style,list) VALUES (:user_id,:is_enabled,:name,:color,:opacity,:style,:list)"
        default_rule_param3 = (user_id,True,"Active voice","0,0,255",0.8,"underline","me(ny|n|ng)\\w+(kan)?\\b|\\bbe(r|l)\\w+")
        with DatabaseHelper(self.name) as db:
            db.execute_single(default_rule1, default_rule_param1)
            db.execute_single(default_rule2, default_rule_param2)
            db.execute_single(default_rule3, default_rule_param3)
    
    def get_grammar_rules(self,user_id):
        with DatabaseHelper(self.name) as db:
            return db.get_sql(f"SELECT * FROM grammar_rules WHERE user_id={user_id}")


    def get_highlighters(self, user_id):
        with DatabaseHelper(self.name) as db:
            return db.get_sql(f"SELECT * FROM highlighters WHERE user_id = {user_id}")

    def get_last_user(self):
        with DatabaseHelper(self.name) as db:
            dict_to_return = {}
            the_list = db.get_sql("SELECT * FROM last_user")
            if the_list == None or the_list == []:
                # use defaults
                dict_to_return["id"] = 1
                dict_to_return["name"] = "default_user"
                return dict_to_return
            else:
                user_name = db.get_sql(f"SELECT * FROM users WHERE id = {the_list[0][1]}")[0][1]
                dict_to_return["name"] = user_name
                dict_to_return["id"] = the_list[0][1]
                return dict_to_return
            
    def set_last_user(self,new_user_name):
        #get id from name
        with DatabaseHelper(self.name) as db:
            new_user_id = db.get_sql(f"SELECT * FROM users WHERE name = '{new_user_name}'")[0][0]
        with DatabaseHelper(self.name) as db:
            #replace last user values
            # db.execute_single(f"UPDATE last_user SET user_id={new_user_id} WHERE id=1")
            sql = f"INSERT OR REPLACE INTO last_user (id,user_id) VALUES (:id, :user_id)"
            params = (1,new_user_id)
            db.execute_single(sql, params)
        
    def get_online_tools(self,active_user):
        with DatabaseHelper(self.name) as db:
            return db.get_sql(f"SELECT * FROM online_tools WHERE user_id = {active_user}")

    def get_other_settings(self,active_user_id):
        with DatabaseHelper(self.name) as db:
            dict_to_return = {}
            dict_to_return["dark_theme"] = bool(db.get_sql(f"SELECT value FROM settings WHERE user_id = {active_user_id} AND name = 'dark_theme'" )[0][0])
            dict_to_return["autofill_back_of_flashcard"] = bool(db.get_sql(f"SELECT value FROM settings WHERE user_id = {active_user_id} AND name = 'autofill_back_of_flashcard'")[0][0])
            return dict_to_return

    def get_recent_files(self,current_user):
        with DatabaseHelper(self.name) as db:
            return db.get_sql(f"SELECT * FROM recent_files WHERE user_id = {current_user} ORDER BY created_at DESC LIMIT 10")

    def get_all_users(self):
        with DatabaseHelper(self.name) as db:
            users = db.get_sql(f"SELECT * FROM users")
            list_to_return = []
            for user in users:
                list_to_return.append(user[1])
            return list_to_return

    def add_new_user(self, new_user_name):
        # check if user already exists
        with DatabaseHelper(self.name) as db:
            result = db.get_sql(f"SELECT * FROM users WHERE name = '{new_user_name}'")
        if result != []: 
            print("user name already exists!")
            return True
        else:# new user can be added
            with DatabaseHelper(self.name) as db:
                sql = "INSERT INTO users(name) VALUES (:name)"
                params = (new_user_name,)
                db.execute_single(sql, params)
            new_id = self.get_id_from_name(new_user_name)
            self.set_up_default_online_tools(new_id)
            self.set_up_default_settings(new_id)
            self.set_up_default_highlighters(new_id)
            self.set_up_default_grammar_rules(new_id)

    def get_id_from_name(self, name):
        with DatabaseHelper(self.name) as db:
            id = db.get_sql(f"SELECT * FROM users WHERE name='{name}'")[0][0]
            return id

    def save_online_tools(self,online_tools,current_user_id):  
        with DatabaseHelper(self.name) as db:
            db.execute_single(f"DELETE FROM online_tools WHERE user_id = {current_user_id}")
        with DatabaseHelper(self.name) as db:
            for row in online_tools:
                row_sql = """INSERT INTO online_tools(title,url,user_id)
                 VALUES (:title,:url,:user_id)"""
                row_params = (row[0],row[1],current_user_id)
                db.execute_single(row_sql,row_params)
    
    def save_grammar_rules(self,grammar_rules,current_user_id):
        with DatabaseHelper(self.name) as db:
            db.execute_single(f"DELETE FROM grammar_rules WHERE user_id ={current_user_id}")
        with DatabaseHelper(self.name) as db:
            for row in grammar_rules:
                sql = """INSERT INTO grammar_rules(user_id,is_enabled,name,color,opacity,style,list)
                VALUES (:user_id,:is_enabled,:name,:color,:opacity,:style,:list)"""
                params = (current_user_id,row[0],row[1],row[2],row[3],row[4],row[5])
                db.execute_single(sql, params)


    def save_other_settings(self,current_user_id,other_settings):
        with DatabaseHelper(self.name) as db:
            db.execute_single(f"DELETE FROM settings WHERE user_id ={current_user_id} AND name ='dark_theme'")
            db.execute_single(f"DELETE FROM settings WHERE user_id ={current_user_id} AND name ='autofill_back_of_flashcard'")
        with DatabaseHelper(self.name) as db:
            db.execute_single(f"INSERT INTO settings(name,value,user_id) VALUES (:name,:value,:user_id)",("dark_theme",other_settings["dark_theme"],current_user_id))
            db.execute_single(f"INSERT INTO settings(name,value,user_id) VALUES (:name,:value,:user_id)",("autofill_back_of_flashcard",other_settings["autofill_back_of_flashcard"],current_user_id))


    def add_recent_file(self,filepath,current_user_id):
        date_time = datetime.now()
        with DatabaseHelper(self.name) as db:
            check = db.get_sql(f"SELECT * FROM recent_files WHERE filepath ='{filepath}'")
            if check == []: #it must be a new file
                with DatabaseHelper(self.name) as db:
                    sql = "INSERT INTO recent_files (filepath,created_at,user_id) VALUES (:filepath,:created_at,:user_id)"
                    params = (filepath,date_time,current_user_id)
                    db.execute_single(sql, params)

            elif len(check[0]) > 0: # replace the old entry
                with DatabaseHelper(self.name) as db:
                    old_id = check[0][0]
                    sql = "REPLACE INTO recent_files (id,filepath,created_at,user_id) VALUES (:id,:filepath,:created_at,:user_id)"
                    params = (old_id,filepath,date_time,current_user_id)
                    db.execute_single(sql, params)
    
    
    def save_word_to_vocabulary(self,current_user_id, term, defin, confid):
        date = datetime.now()
        sql = f"INSERT INTO vocabulary(user_id,term,definition,highlighter_id,is_regex,created_at) VALUES(:user_id,:term,:definition,:highlighter_id,:is_regex,:created_at)"
        params = (current_user_id,term.lower() ,defin, confid, False,date)
        with DatabaseHelper(self.name) as db:
            db.execute_single(sql, params)

    def update_word_to_vocab(self,old_id,defin,confid):
        date = datetime.now()
        sql = f"UPDATE vocabulary SET definition='{defin}', highlighter_id ={confid}, created_at ='{date}' WHERE id ={old_id}"
        with DatabaseHelper(self.name) as db:
            db.execute_single(sql)

    def look_up_sel_in_db(self,sel,current_user_id):
        with DatabaseHelper(self.name) as db:
            return db.get_sql(f"SELECT * FROM vocabulary WHERE term='{str(sel).lower()}'AND user_id={current_user_id} LIMIT 1")
    
    def get_list_of_vocab_by_highlighter(self,current_user_id,highlighter_id):
        with DatabaseHelper(self.name) as db:
            return db.get_sql(f"SELECT * FROM vocabulary WHERE user_id={current_user_id} AND highlighter_id={highlighter_id}")

    def add_flashcard_to_db(self,fc,current_user_id):
        with DatabaseHelper(self.name) as db:
            sql = """INSERT INTO flashcards (user_id,front,back,back_image,audio_start,audio_end) 
            VALUES(:user_id,:front,:back,:back_image,:audio_start,:audio_end)
            """
            params = (current_user_id,fc["front"],fc["back"],fc["back_image"],fc["audio_start"],fc["audio_end"])
            db.execute_single(sql, params)

    def get_flashcards_from_db(self,current_user_id):
        try:
            with DatabaseHelper("database.db") as db:
                return db.get_sql(f"SELECT * FROM flashcards WHERE user_id={current_user_id}")
        except:
            return []

    def delete_all_flashcards_for_user(self,current_user_id):
        with DatabaseHelper("database.db") as db:
            db.execute_single(f"DELETE FROM flashcards WHERE user_id={current_user_id}")
    
    def delete_user(self,current_user_id):
        with DatabaseHelper("database.db") as db:
            sql_list = [
                f"DELETE FROM flashcards WHERE user_id={current_user_id}",
                f"DELETE FROM last_user WHERE user_id ={current_user_id}",
                f"DELETE FROM recent_files WHERE user_id ={current_user_id}",
                f"DELETE FROM vocabulary WHERE user_id ={current_user_id}",
                f"DELETE FROM grammar_rules WHERE user_id ={current_user_id}",
                f"DELETE FROM highlighters WHERE user_id ={current_user_id}",
                f"DELETE FROM online_tools WHERE user_id ={current_user_id}",
                f"DELETE FROM settings WHERE user_id ={current_user_id}",
                f"DELETE FROM users WHERE id={current_user_id}",
            ]
            for item in sql_list:
                try:
                    db.execute_single(item)
                except Exception as e:
                    print(e)









