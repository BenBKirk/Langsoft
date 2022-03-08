
from database.database import DatabaseHelper

class vocabulary:
    """
    Serves as an interface between the widgets that use this data and the database
    """
    def __init__(self,user_id):
        self.user_id = user_id
        self.single_exact_match_results = None
        self.like_results = []

    def search_single_exact_vocab(self,search_term):
        with DatabaseHelper() as db:
            data = db.fech_all("SELECT * FROM vocabulary WHERE term=? AND user_id=? LIMIT 1",(search_term.lower(),self.user_id))
            # TODO probably need to slice this better
            self.single_exact_match = data[0]
    
    def search_like_vocab(self,search_term):
        with DatabaseHelper() as db:
            data = db.fech_all("SELECT * FROM vocabulary WHERE term LIKE ? AND user_id=?",(search_term,self.user_id))
            self.like_results = data

    def convert_list_to_list_of_dict(self,sql_list):
        #fields: id, user_id,term,definition,highlighter_id,is_regex
        new_list = []
        for item in sql_list:
            temp_dict = {"id":item[0], "user_id":item[1], "term":item[2], "definition":item[3], "highlighter_id":item[4], "is_regex":item[5]}
            new_list.append(temp_dict)

    def list_tem_to_dict(self,item):
        pass

    


    def set_all_vocab(self):
        pass