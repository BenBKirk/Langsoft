

from PyQt5.QtWidgets import * #QApplication, QWidget, QFrame, QLineEdit, QHBoxLayout, QVBoxLayout, QSplitter, QTableWidget, QTableWidgetItem, QAbstractItemView, QTabWidget, QToolBar
from PyQt5 import QtGui
from PyQt5.QtCore import Qt


class WordEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.set_up_gui()

    def set_up_gui(self):
        self.text_editor = QTextEdit()
        # self.text_editor.setFixedHeight(40)
        self.unknown_btn = QPushButton("1.Unknown")
        self.semi_known_btn = QPushButton("2.Semi-Known")
        self.known_btn = QPushButton("3.Known")
        self.unknown_btn.setStyleSheet(f"background-color : rgb(255,0,0)")
        self.semi_known_btn.setStyleSheet(f"background-color : rgb(255,255,0)")
        self.known_btn.setStyleSheet(f"background-color : rgb(0,255,0)")
        color_btn_layout = QHBoxLayout()
        color_btn_layout.addWidget(self.unknown_btn)    
        color_btn_layout.addWidget(self.semi_known_btn)
        color_btn_layout.addWidget(self.known_btn)
        widget_for_btn_layout = QWidget()
        widget_for_btn_layout.setLayout(color_btn_layout)
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.text_editor)
        splitter.addWidget(widget_for_btn_layout)#
        layout = QVBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)

    def set_text(self, text):
        self.text = text
        self.text_editor.setText(text)

    
if __name__ == "__main__":
    """this is just test code"""
    import sys
    app = QApplication(sys.argv)
    window = WordEditor()
    # example data
    window.set_text("Hello World")

    window.show()
    sys.exit(app.exec())
