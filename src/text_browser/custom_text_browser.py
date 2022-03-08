"""
This needs to be custom in order to detect a click release in the main text window
"""
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from text_browser.context_finder import ContextFinder

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
        """ detects a click release in the text window
        and then broadcasts a signal for looking up words/sent """
        # get selection info before signaling
        cursor = self.textCursor()
        selection = self.find_selection(cursor)
        if selection is not None: # it is possible to click on empty space
            context = ContextFinder(cursor,length_of_context=15).get_context()
            selection, context = self.clean_up_results(selection,context)
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
    
    def clean_up_results(self, selection,context):
        cleaned_up_selection = selection.strip()
        cleaned_up_context = context.strip()
        return cleaned_up_selection, cleaned_up_context
