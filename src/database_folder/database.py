import sqlite3

class DatabaseHelper:
    def __init__(self, name="database.db"):
        self.open(name)
        
    def open(self,name):
        try:
            self.conn = sqlite3.connect(name)
            self.cursor = self.conn.cursor()

        except sqlite3.error as e:
            self.conn.rollback()
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
    
    def fetch_one(self,sql, params=None):
        if params is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql,params)
        return self.cursor.fetchone()
    
    def fetch_all(self,sql, params=None):
        if params is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql,params)
        return self.cursor.fetchall()

    def execute_single(self,query,param=None):
        if param is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query,param)
    
    def execute_script(self,query):
        self.cursor.executescript(query)

class DatabaseCreator:
    """creates default database"""
    def __init__(self, name="database.db"):
        self.name = name
    
    def create_db(self):
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
                audio_file VARCHAR,
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
        default_rule_param1 = (
            user_id,
            True,
            "Time words/phrases",
            "0,255,0",
            0.4,
            "highlight",
            "(se)?sudah, akan, sedang, sebelum, sebelumnya, setelah, pada, waktu, saat, hari berikutnya, minggu berikutnya, minggu depan, minggu lalu, lusa, kemarin, besok, yang lalu, hingga, sejak, selanjutnya, lalu, sampai, kemudian, jam, detik, menit, tiba-tiba, dulu, zaman, (se)?lama, sambil"
            )
        default_rule2 = "INSERT OR REPLACE INTO grammar_rules(user_id,is_enabled,name,color,opacity,style,list) VALUES (:user_id,:is_enabled,:name,:color,:opacity,:style,:list)"
        default_rule_param2 = (
            user_id,
            True,
            "Logical Connectors",
            "255,0,0",
            0.4,
            "highlight",
            "nah, untuk, oleh, karena, supaya, agar, oleh sebab, itu sebabnya, jadi, jika, kalau, namun, soalnya, muskipun, sebaliknya, sedangkan, padahal, (te)?tapi"
            )
        default_rule3 = "INSERT OR REPLACE INTO grammar_rules(user_id,is_enabled,name,color,opacity,style,list) VALUES (:user_id,:is_enabled,:name,:color,:opacity,:style,:list)"
        default_rule_param3 = (
            user_id,
            True,
            "Direction/Location words",
            "0,0,255",
            0.4,
            "highlight",
            "di, ke, dari, pada, daripada, kepada, menuju, di mana, ke mana, dari mana, arah, di antara, di tengah, sini, sana, situ, dalam, luar, depan, belakang, samping, dekat, atas, bawah, sekeliling, lewat, melewati"
            )
        default_rule4 = "INSERT OR REPLACE INTO grammar_rules(user_id,is_enabled,name,color,opacity,style,list) VALUES (:user_id,:is_enabled,:name,:color,:opacity,:style,:list)"
        default_rule_param4 = (
            user_id,
            True,
            "Noun Classifiers",
            "148,0,211",
            0.4,
            "highlight",
            "(se)?batang, (se)?buah, (se)?butir, (se)?cangkir, (se)?ekor, (se)?gelas, (se)?helai, (se)?ikat, (se)?lembar, (se)?mangk[ou]k, (se)?orang, (se)?pasang, (se)?sendok, (se)?piring, (se)?siung, (se)?suap, (se)?tangkai, (se)?titik"
            )
        default_rule5 = "INSERT OR REPLACE INTO grammar_rules(user_id,is_enabled,name,color,opacity,style,list) VALUES (:user_id,:is_enabled,:name,:color,:opacity,:style,:list)"
        default_rule_param5 = (
            user_id,
            True,
            "Referral",
            "255,255,0",
            0.4,
            "highlight",
            "selain, mengenai, tentang, soal, yaitu, yang, melewati, tersebut"
            )
        default_rule6 = "INSERT OR REPLACE INTO grammar_rules(user_id,is_enabled,name,color,opacity,style,list) VALUES (:user_id,:is_enabled,:name,:color,:opacity,:style,:list)"
        default_rule_param6 = (
            user_id,
            True,
            "Comparison",
            "255,127,0",
            0.4,
            "highlight",
            "lebih, kurang, sebesar, sekecil, seluas, setinggi, sebagus, setebal, setipis, secepat, sepelan, seperti, mirip, serupa, sama, perbedaan, bedanya, sisi lain, sebaliknya, daripada, dibandingkan(\sdengan)?, atau, juga"
            )

        default_rule7 = "INSERT OR REPLACE INTO grammar_rules(user_id,is_enabled,name,color,opacity,style,list) VALUES (:user_id,:is_enabled,:name,:color,:opacity,:style,:list)"
        default_rule_param7 = (
            user_id,
            True,
            "passive voice :)",
            "0,255,0",
            0.8,
            "underline",
            "(?!\\bdian\\b|\\bdiam\\b|\\bdiam\\b|\\bdia\\b|\\bdinah\\b|\\bdiri(nya|mu|ku)?\\b)di\\w+\\b|\\b(yang|itu|ini)(?<!setelah itu)(\\s)?(tidak|enggak|tak|nggak|)?(sudah|telah|belum|akan)?\\s(saya|kami|kita|dia|ibu|bapak|mereka|pak\\s\\w+|ibu\\s\\w+|bu\\s\\w+)\\s\\w+(kan|i)?"
            )
        default_rule8 = "INSERT OR REPLACE INTO grammar_rules(user_id,is_enabled,name,color,opacity,style,list) VALUES (:user_id,:is_enabled,:name,:color,:opacity,:style,:list)"
        default_rule_param8 = (
            user_id,
            True,
            "Active voice",
            "0,0,255",
            0.8,
            "underline",
            "me(ny|n|ng)\\w+(kan)?\\b|\\bbe(r|l)\\w+"
            )
        with DatabaseHelper(self.name) as db:
            db.execute_single(default_rule1, default_rule_param1)
            db.execute_single(default_rule2, default_rule_param2)
            db.execute_single(default_rule3, default_rule_param3)
            db.execute_single(default_rule4, default_rule_param4)
            db.execute_single(default_rule5, default_rule_param5)
            db.execute_single(default_rule6, default_rule_param6)
            db.execute_single(default_rule7, default_rule_param7)
            db.execute_single(default_rule8, default_rule_param8)




