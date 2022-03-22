
from .database import DatabaseHelper

class User:
    def __init__(self):
        self.user_id = self.get_user_id_from_db()

    def get_user_id_from_db(self):
        with DatabaseHelper() as db:
            try:
                user_id = db.fetch_one("SELECT user_id FROM last_user WHERE id = ?",(1,))[0]
            except Exception as e:
                db.execute_single("INSERT INTO last_user(user_id) VALUES(?)",(1,))
                user_id = 1
            return user_id

    def get_user_id(self):
        return self.user_id

if __name__ == "__main__":
    from database import DatabaseHelper
    user = User()
    print(user.get_user_id())