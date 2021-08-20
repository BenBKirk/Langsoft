"""
This needs to be custom in order to detect a click (actually release) in the main text window
"""
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class CustomTextBrowser(QTextEdit):
    clicked = pyqtSignal()
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
        self.clicked.emit()
    

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
