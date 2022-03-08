from database.database import DatabaseHelper

class OnlineTools:
    """
    Serves as an interface between the widgets that use this data and the database
    """
    def __init__(self,user_id):
        self.user_id = user_id
        self.list_of_titles = []
        self.list_of_urls = []

    def set_online_tools(self):
        with DatabaseHelper() as db:
            data = db.fech_all( "SELECT * FROM online_tools WHERE user_id = ?",(self.user_id,))
        for data in data:
            self.list_of_titles.append(data[1])
            self.list_of_urls.append(data[2])
    
    def update_online_tools(self):
        pass