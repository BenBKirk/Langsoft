
from PyQt5.QtWidgets import * #QApplication, QWidget, QFrame, QLineEdit, QHBoxLayout, QVBoxLayout, QSplitter, QTableWidget, QTableWidgetItem, QAbstractItemView, QTabWidget, QToolBar
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize
from API.google_trans_API import GoogleTranslate

class WordEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.set_up_gui()

    def set_up_gui(self):
        self.text_editor = QTextEdit()
        self.text_editor.setMinimumHeight(30)
        # self.text_editor.setBaseSize(QSize(30, 30))

        #display selected word
        self.selected_word_label = QLabel()
        self.selected_word_label.setFont(QtGui.QFont("Calibri",15))

        #buttons
        self.unknown_btn = QPushButton("Unknown")
        self.semi_known_btn = QPushButton("Semi-Known")
        self.known_btn = QPushButton("Known")
        self.unknown_btn.setStyleSheet(f"background-color : rgb(255,0,0)")
        self.semi_known_btn.setStyleSheet(f"background-color : rgb(255,255,0)")
        self.known_btn.setStyleSheet(f"background-color : rgb(0,255,0)")
        color_btn_layout = QHBoxLayout() 
        color_btn_layout.addWidget(self.unknown_btn)    
        color_btn_layout.addWidget(self.semi_known_btn)
        color_btn_layout.addWidget(self.known_btn)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.selected_word_label)
        self.main_layout.addWidget(self.text_editor)
        self.main_layout.addLayout(color_btn_layout)
        # self.main_layout.addLayout(suggestion_layout)
        self.main_layout.setStretch(0,1)
        self.main_layout.setStretch(1,0)
        self.setLayout(self.main_layout)

    def set_definition_text(self, text):
        self.definition_text = text
        self.text_editor.setText(text)
    
    def set_selection_text(self, text):
        self.selected_word = text
        self.selected_word_label.setText(f"<b>{text}</b>")
    
    def get_google_suggestion(self):
        self.google_suggestion = GoogleTranslate().translate(self.selected_word)
        
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
    
if __name__ == "__main__":
    """this is just test code"""
    import sys
    app = QApplication(sys.argv)
    window = WordEditor()
    # example data
    window.set_definition_text("Hello World")

    window.show()
    sys.exit(app.exec())
