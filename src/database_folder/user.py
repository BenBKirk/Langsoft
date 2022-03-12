
from .database import DatabaseHelper

class User:
    def __init__(self):
        self.user_id = self.get_user_id_from_db()

    def get_user_id_from_db(self):
        with DatabaseHelper() as db:
            user_id = db.fetch_one("SELECT user_id FROM last_user WHERE id = ?",(1,))[0]
            if user_id:
                return user_id
            else: # set the last user to default user which is 1
                db.execute_single("INSERT INTO last_user(user_id) VALUES(?)",(1,))
                return 1

    def get_user_id(self):
        return self.user_id

if __name__ == "__main__":
    from database import DatabaseHelper
    user = User()
    print(user.get_user_id())