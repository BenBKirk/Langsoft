
from datetime import datetime
from .database import DatabaseHelper
from .highlighters import Highlighters
from .user import User

class Vocabulary:
    """
    Serves as an interface between the widgets that use this data and the database
    """
    def __init__(self):
        self.user_id = User().get_user_id()

    def fetch_single_exact_vocab(self,search_term) -> str:
        with DatabaseHelper() as db:
            data = db.fetch_one("SELECT definition FROM vocabulary WHERE term=? AND user_id=? LIMIT 1",(search_term.lower(),self.user_id))
            # TODO probably need to slice this better
            if data is not None:
                return data[0]
    
    def fetch_like_vocab(self,search_term):
        with DatabaseHelper() as db:
            data = db.fetch_all("SELECT * FROM vocabulary WHERE term LIKE ? AND user_id=?",(search_term,self.user_id))
            return data

    # def convert_list_to_list_of_dict(self,sql_list):
    #     #fields: id, user_id,term,definition,highlighter_id,is_regex
    #     new_list = []
    #     for item in sql_list:
    #         temp_dict = {"id":item[0], "user_id":item[1], "term":item[2], "definition":item[3], "highlighter_id":item[4], "is_regex":item[5]}
    #         new_list.append(temp_dict)

    def add_word_to_database(self,word,definition,confidence):
        date = datetime.now()
        hl = Highlighters()
        confidence = hl.find_appropriate_highlighter_id(word,confidence)  

        if self.is_word_in_database(word):
            self.update_word_in_db(word,definition,confidence,date)
        else:
            self.add_new_word_to_db(word,definition,confidence,date)
    
    def is_word_in_database(self,word):
        if self.fetch_single_exact_vocab(word) is not None:
            return True

    def add_new_word_to_db(self,word,definition,confidence,date):
        sql = "INSERT INTO vocabulary(user_id,term,definition,highlighter_id,is_regex,created_at) VALUES(:user_id,:term,:definition,:highlighter_id,:is_regex,:created_at)"
        params = (self.user_id,word.lower() ,definition, confidence, False,date)
        with DatabaseHelper() as db:
            db.execute_single(sql, params)
    
    def update_word_in_db(self,word,definition,confidence,date):
        sql = "UPDATE vocabulary SET definition = ?, highlighter_id = ?, created_at = ? WHERE term = ?"
        params = (definition,confidence,date,word)
        with DatabaseHelper() as db:
            db.execute_single(sql, params)
    
    def fetch_vocab_by_highlighter_id(self,highlighter_id):
        with DatabaseHelper() as db:
            list_of_tuples = db.fetch_all("SELECT term FROM vocabulary WHERE highlighter_id = ? AND user_id=?",(highlighter_id, self.user_id))
            temp_list = []
            for tuple in list_of_tuples:
                temp_list.append(tuple[0])
            return temp_list

        




