
from PyQt5.QtGui import QTextCursor

class ContextFinder:
    """
    responisible for getting the context of the word that was clicked on 
    """
    def __init__(self,cursor,length_of_context):
        super().__init__()
        self.cursor = cursor
        self.length_of_context = length_of_context
        self.upper_limit_reached = True # if the limit is reached then "..." will be appended to the text so show that did not reach the end of the sentence before being too long
        self.lower_limit_reached = True

    def get_context(self):
        distance_moved_left = self.move_cursor_left()
        self.move_cursor_right(distance_moved_left)
        text = self.cursor.selectedText()
        text = self.append_dots_if_needed(text)
        return text
    
    def move_cursor_left(self) -> int:
        """move cursor left and start a selection by moving anchor"""
        for i in range(self.length_of_context):
            self.cursor.movePosition(QTextCursor.WordLeft,QTextCursor.MoveAnchor)
            #break early if at block start
            if self.cursor.atBlockStart():
                self.upper_limit_reached = False
                return i
        return self.length_of_context
    
    def move_cursor_right(self,distance_moved_left):
        """move cursor right and complete selection by keeping anchor in postion"""
        for i in range(self.length_of_context + distance_moved_left):
            self.cursor.movePosition(QTextCursor.WordRight,QTextCursor.KeepAnchor)
            #break early if at block end
            if self.cursor.atBlockEnd():
                self.lower_limit_reached = False
                break
    def append_dots_if_needed(self,text):
        """append bots to show that the end of the sentence has not been reached but rather the word limit"""
        if self.upper_limit_reached:
            text = "..." + text
        if self.lower_limit_reached:
            text = text + "..."
        return text
    
