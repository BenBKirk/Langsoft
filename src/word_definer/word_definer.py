
from PyQt5.QtWidgets import QTextEdit, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QApplication
from PyQt5.QtGui import QFont, QFocusEvent
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QEvent
from API.google_trans_API import GoogleTranslate
from database_folder.vocabulary import Vocabulary

class WordDefiner(QWidget):
    word_saved_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.set_up_gui()
        self.unknown_btn.clicked.connect(lambda: self.save_word(confidence="unknown"))
        self.semi_known_btn.clicked.connect(lambda: self.save_word(confidence="semi-known"))
        self.known_btn.clicked.connect(lambda: self.save_word(confidence="known"))
        self.setContentsMargins(0,0,0,0)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setGeometry(0,0,300,100)

    def set_up_gui(self):
        self.text_editor = QTextEdit()
        self.text_editor.setMinimumHeight(30)
        # self.text_editor.setMaximumHeight(30)
        self.text_editor.setFont(QFont("Arial", 12))

        #display selected word
        self.selected_word_label = QLabel()
        self.selected_word_label.setFont(QFont("Arial",15))
        self.selected_word_label.setMaximumHeight(30)

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
        self.main_layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.main_layout)

    def set_definition_text(self, text):
        self.definition_text = text
        self.text_editor.setText(text)
    
    def look_up_word(self,text):
        self.set_selection_text(text)
        from_db = Vocabulary().fetch_single_exact_vocab(text)
        if from_db != None:
            self.set_definition_text(from_db)
        else:
            self.google_suggestion = GoogleTranslate().translate(self.selected_word)
            self.set_definition_text(self.google_suggestion) if self.google_suggestion != None else self.set_definition_text("")
    
    def set_selection_text(self, text):
        self.selected_word = text
        self.selected_word_label.setText(f"<b>{text}</b>")
    
    def save_word(self,confidence):
        definition = self.text_editor.toPlainText()
        # word = self.selected_word.lower()
        Vocabulary().add_word_to_database(self.selected_word, definition, confidence)
        self.clear_ui()
        self.word_saved_signal.emit()
    
    def clear_ui(self):
        self.text_editor.clear()
        self.selected_word_label.clear()
        self.selected_word = ""
        self.definition_text = ""
        self.google_suggestion = ""
    

    def move_to_click_position(self,pos):
        width = self.width()
        height = self.height()
        # make sure it doesn't go off the side 
        x = int(pos.x())
        y = int(pos.y())
        dis_cen = width/2 # minimum allowed distance from the center, in other words don't go past this limit otherwise it will be cut off the screen.
        while x <= dis_cen: # if passes the limit add 1 until it is  no longer past the limit.
            x += 1
        if x > dis_cen:
            x = x-dis_cen # center over click pos
        y = y - height/2 # center over click pos
        y = y - 120 # offset above click pos
        self.move(x,y)
        
