"""
This needs to be custom in order to detect a click release in the main text window
"""
from PyQt5.QtWidgets import QTextEdit, QColorDialog
from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtCore import *
from text_browser.context_finder import ContextFinder
from .syntax_highlighter import SyntaxHighlighter

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
        self.syntax_highlighter = SyntaxHighlighter(self.document())
        self.setFont(QFont("Calibri",14))

    def mouseDoubleClickEvent(self,event):
        cursor = self.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)
        selection = cursor.selectedText()
        if selection != "":
            context = ContextFinder(cursor,length_of_context=15).get_context()
            selection, context = self.clean_up_strings(selection,context)
            self.clicked_signal.emit([selection,context,event.globalPos()])

    def mouseReleaseEvent(self, event):
        """ detects a click release in the text window
        and then broadcasts a signal for looking up words/sent """
        cursor = self.textCursor()
        if cursor.hasSelection():
            selection = cursor.selectedText()
            if len(selection) < 50:
                context = ContextFinder(cursor,length_of_context=15).get_context()
                selection, context = self.clean_up_strings(selection,context)
                self.clicked_signal.emit([selection,context,event.globalPos()])

 
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
    
    def clean_up_strings(self, selection,context):
        cleaned_up_selection = selection.strip()
        cleaned_up_context = context.strip()
        return cleaned_up_selection, cleaned_up_context
