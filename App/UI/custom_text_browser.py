"""
This needs to be custom in order to detect a click (actually release) in the main text window
"""
from PyQt5 import QtWidgets, QtCore
# from PyQt5.QtGui import QMenu, QCursor
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import Qt
class CustomTextBrowser(QtWidgets.QTextEdit):
    clicked = QtCore.pyqtSignal()
    hightlight = QtCore.pyqtSignal(str)
    clear_highlighting = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setFontPointSize(16) #in the future it might be necessary to more this to the logic file because of the settings.
        # self.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.customContextMenuRequested.connect()

    # def mousePressEvent(self, QMouseEvent):
    #     self.clicked.emit()

    def mouseReleaseEvent(self, QMouseEvent):
        self.clicked.emit()
    
    def contextMenuEvent(self,event):
        contextMenu = self.createStandardContextMenu(event.pos())
        hightlight_custom = contextMenu.addAction("Custom Highlight")
        clear_highlighting = contextMenu.addAction("Clear Highlighting")
        add_to_connectors = contextMenu.addAction("Add Word To Connectors")
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == hightlight_custom:
            color = QtWidgets.QColorDialog.getColor()
            print(color.name())
            self.hightlight.emit(color.name())
        if action == clear_highlighting:
            self.clear_highlighting.emit()

            

            # self.hightlight.emit("Green")


    

