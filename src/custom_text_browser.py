"""
This needs to be custom in order to detect a click (actually release) in the main text window
"""
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class CustomTextBrowser(QTextEdit):
    clicked_signal = pyqtSignal(list)
    hightlight = pyqtSignal(str)
    clear_highlighting = pyqtSignal()
    # got_focus = pyqtSignal()
    scroll = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setFontPointSize(16)
        self.setMouseTracking(True)  
        self.installEventFilter(self)


    def eventFilter(self, obj, event):
        if event.type() == QEvent.Wheel: #.ToolTip:
            # self.hover.emit(event.pos())
            self.scroll.emit()
            return False
        # Call Base Class Method to Continue Normal Event Processing
        return super(CustomTextBrowser, self).eventFilter(obj, event)

    def mouseReleaseEvent(self, event):
        """
        detects a click release in the text window that is needed for looking up words/sent
        """

        # get selection info before signaling
        cursor = self.textCursor()
        selection = self.find_selection(cursor)
        if selection is not None: # it is possible to click on nothing
            context = ContextFinder(cursor,length_of_context=15).get_context()
            print(f"selection is: {selection} \ncontext is: {context}")
            #broadcast signal for other widgets such as the web search
            self.clicked_signal.emit([selection,context])

    def find_selection(self,cursor):
        if not cursor.hasSelection():# What it a click or click and drag selection?
            cursor.select(QTextCursor.WordUnderCursor)# if not, select the word under the cursor
        if cursor.selectedText() == "":
            return None
        return cursor.selectedText() #return whatever is selected
 
    def contextMenuEvent(self, event):
        contextMenu = self.createStandardContextMenu(event.pos())
        hightlight_custom = contextMenu.addAction("Custom Highlight")
        clear_highlighting = contextMenu.addAction("Clear Highlighting")
        add_to_connectors = contextMenu.addAction("Add Word To Connectors")

        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == hightlight_custom:
            color = QColorDialog.getColor()
            self.hightlight.emit(color.name())
        if action == clear_highlighting:
            self.clear_highlighting.emit()
    

class ContextFinder:
    """
    responisible for getting the context of the word that was clicked on 
    """
    def __init__(self,cursor,length_of_context):
        super().__init__()
        self.cursor = cursor
        self.length_of_context = length_of_context
        # if the limit is reached then "..." will be appended to the text so show that did not reach the end of the sentence before being too long
        self.upper_limit_reached = True
        self.lower_limit_reached = True

        distance_moved_left = self.move_cursor_left()
        self.distance_moved_right = self.move_cursor_right(distance_moved_left)
    
    def move_cursor_left(self):
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
    
    def get_context(self):
        text = self.cursor.selectedText()
        text = self.append_dots_if_needed(text)
        return text











