

class DefinitionFinder:
    """
   This class is responible for finding the definition of a word
   whether using the google translate API or the database lookup 
    """
    def __init__(self,selected_word):
        self.selected_word = selected_word

    def search_db(self,selected_word):
        pass

    def search_google_api(self,selected_word):
        pass