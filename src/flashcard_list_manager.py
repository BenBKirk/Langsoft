import os
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from bs4 import BeautifulSoup
from database_helper import DatabaseHelper

import logging
logging.basicConfig(level=logging.DEBUG,filename="app.log",format='%(asctime)s - %(levelname)s - %(message)s')


class FlashcardManager(QWidget):
    text_edits_front = {}
    text_edits_back = {}
    text_edits_img = {}
    text_edits_audio = {}
    audio_start ={}
    audio_end ={}
    del_btn = {}
    def __init__(self):
        super(FlashcardManager, self).__init__()
        self.fontL = QtGui.QFont("Ubuntu",12, 200)
        self.resize(800,700)
        self.list_table_widget = QTableWidget()
        layout = QGridLayout()
        self.save_button = QPushButton("Save")
        self.save_button.setFont(self.fontL)
        self.save_button.clicked.connect(self.save_flashcards_to_db)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFont(self.fontL)
        self.cancel_button.clicked.connect(self.close)
        hbox = QHBoxLayout()
        hbox.addWidget(self.cancel_button)
        hbox.addWidget(self.save_button)
        widget_for_buttons = QWidget()
        widget_for_buttons.setLayout(hbox)
        layout.addWidget(self.list_table_widget)
        layout.addWidget(widget_for_buttons)
        self.setLayout(layout)
        self.setWindowTitle("Flashcard Manager")
        self.setWindowIcon(QtGui.QIcon(os.path.join("src","img","list.png")))
    
    def get_flashcards_from_db(self):
        try:
            with DatabaseHelper("database.db") as db:
                return db.get_sql(f"SELECT * FROM flashcards WHERE user_id={self.current_user_id}")
        except:
            return []

    def set_up(self,current_user_id):
        self.current_user_id = current_user_id
        self.load_flashcards_to_ui()
        
    def load_flashcards_to_ui(self):
        self.list_table_widget.clear()
        flashcard_list = self.get_flashcards_from_db()
        self.list_table_widget.setRowCount(len(flashcard_list))
        self.list_table_widget.setColumnCount(5)
        self.list_table_widget.setHorizontalHeaderLabels(["Del","Front","Back","Image","Audio"])
        self.list_table_widget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.list_table_widget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        for i, card in enumerate(flashcard_list):
            self.text_edits_front[i] = self.create_text_edit_widget(card[2])
            self.text_edits_back[i] = self.create_text_edit_widget(card[3])
            if card[4] != "":
                self.text_edits_img[i] = self.create_text_edit_widget('<img src="' + card[4] + '>')
                self.list_table_widget.setCellWidget(i, 3,self.text_edits_img[i])
            if card[5] != None and card[6] != None:
                self.audio_start[i] = card[5]
                self.audio_end[i] = card[6]
                self.text_edits_audio[i] = self.create_audio_edit_widget()
                self.list_table_widget.setCellWidget(i, 4,self.text_edits_audio[i])
            del_btn = self.make_del_btn(i)
            self.list_table_widget.setCellWidget(i,0,del_btn)
            self.list_table_widget.setCellWidget(i, 1, self.text_edits_front[i])
            self.list_table_widget.setCellWidget(i, 2, self.text_edits_back[i])
        self.list_table_widget.resizeColumnsToContents()
        self.list_table_widget.resizeRowsToContents()

    def get_list_of_flashcards(self):
        flashcard_list = []
        for i,key in enumerate(self.text_edits_front.keys()):
            card = {}
            card["front"] = str(self.makeSoup(self.text_edits_front[key].toHtml()).body)
            card["back"] = str(self.makeSoup(self.text_edits_back[key].toHtml()).body)
            try:
                imgSoup = self.makeSoup(self.text_edits_img[key].toHtml())
                img = imgSoup.find("img")["src"]
            except:
                img = None
            if img is not None:
                card["img"] = str(img)
            else:
                card["img"] = ""
            try:
                card["audio_start"] = self.audio_start[i]
                card["audio_end"] = self.audio_end[i]
            except:
                card["audio_start"] = None
                card["audio_end"] = None
            flashcard_list.append(card)
        return flashcard_list
    
    def save_flashcards_to_db(self):
        flashcards = self.get_list_of_flashcards()
        with DatabaseHelper("database.db") as db:
            db.execute_single(f"DELETE FROM flashcards WHERE user_id={self.current_user_id}")
        with DatabaseHelper("database.db") as db:
            for card in flashcards:
                sql = """INSERT INTO flashcards(user_id,front,back,back_image,audio_start,audio_end)
                VALUES (:user_id,:front,:back,:back_image,:audio_start,:audio_end)
                """
                params = (self.current_user_id,card["front"],card["back"],card["img"],card["audio_start"],card["audio_end"])
                db.execute_single(sql, params)
        self.hide()

    def makeSoup(self,html):
        soup = BeautifulSoup(html,"html.parser")
        return soup

    def create_text_edit_widget(self,html):
        text_edit_widget = QTextEdit()
        # textEditWidget.setFixedHeight(100)
        text_edit_widget.setFont(QtGui.QFont("Calibri",10))
        text_edit_widget.setHtml(html)
        return text_edit_widget
    
    def create_audio_edit_widget(self):
        name = "play"
        play_button = QPushButton()
        play_button.setIcon(QIcon(os.path.join(os.getcwd(),"src","img",name + ".png")))
        return play_button

    def make_del_btn(self,i):
        self.del_btn[i] = QPushButton("X")
        self.del_btn[i].setMaximumWidth(50)
        self.del_btn[i].clicked.connect(self.remove_table_row)
        return self.del_btn[i]
    
    def remove_table_row(self):
        current_index = self.list_table_widget.currentIndex().row()
        # get keys from dict of widgets
        the_keys = self.text_edits_front.keys()
        for i, key in enumerate(the_keys):
            if i == current_index:
                key_index = int(key)
        try:
            self.list_table_widget.removeRow(current_index)
            self.text_edits_front.pop(key_index)
            self.text_edits_back.pop(key_index)
            try:
                self.text_edits_img.pop(key_index)
            except Exception as e:
                pass
        except Exception as e:
            logging.exception(f"THERE WAS AN ERROR WHEN REMOVING ITEM FROM LIST AT INDEX {current_index} --- {e}")
            print(f"THERE WAS AN ERROR WHEN REMOVING ITEM FROM LIST AT INDEX {current_index} --- {e}")
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FlashcardManager()
    window.show()
    sys.exit(app.exec())