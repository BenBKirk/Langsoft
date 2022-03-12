
from database_folder.database import DatabaseHelper
from database_folder.user import User
import re

class Highlighters:
    def __init__(self):
        self.user_id = User().get_user_id()

    def find_appropriate_highlighter_id(self,word,confidence):
        if self.is_word_actually_a_phrase(word):
            confidence = confidence + "-sent"
        with DatabaseHelper() as db:
            id = db.fetch_one("SELECT id FROM highlighters WHERE user_id = ? AND name =?",(self.user_id,confidence))[0]
        return id
        

    def is_word_actually_a_phrase(self,word):
        pattern = re.compile("\s") #this is a regex that matches any whitespace
        if re.search(pattern, word):
            return True
        return False

    def fetch_all_highlighters_by_user_id(self) -> list:
        with DatabaseHelper() as db:
            data = db.fetch_all("SELECT * FROM highlighters WHERE user_id = ?",(self.user_id,))
            return data