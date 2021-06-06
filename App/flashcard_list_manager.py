import os
import json
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from bs4 import BeautifulSoup



class FlashcardManager(QWidget):
    text_edits_front = {}
    text_edits_back = {}
    text_edits_img = {}
    btn = {}
    def __init__(self):
        super(FlashcardManager, self).__init__()
        self.fontL = QtGui.QFont("Ubuntu",12, 200)
        self.resize(800,700)
        self.list_table_widget = QTableWidget()
        # self.setupTableWidget()
        layout = QGridLayout()
        # mainLabel = QLabel("Flashcard Manager")
        # mainLabel.setFont(QtGui.QFont("Ubuntu",16)) 
        self.save_button = QPushButton("Save")
        self.save_button.setFont(self.fontL)
        self.save_button.clicked.connect(self.save_flashcards_to_json)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFont(self.fontL)
        self.cancel_button.clicked.connect(self.close)
        hbox = QHBoxLayout()
        hbox.addWidget(self.cancel_button)
        hbox.addWidget(self.save_button)
        widget_for_buttons = QWidget()
        widget_for_buttons.setLayout(hbox)
            
        # layout.addWidget(mainLabel)
        layout.addWidget(self.list_table_widget)
        layout.addWidget(widget_for_buttons)
        self.setLayout(layout)
        self.setWindowTitle("Flashcard Manager")
        self.setWindowIcon(QtGui.QIcon(os.path.join("App","img","list.png")))
    
    def get_flashcard_data_from_json(self):
        path = os.path.join(os.getcwd(),"App","flashcards.json")
        with open(path,"r+") as f:
            data = json.load(f)
        return data
    
    def save_flashcards_to_json(self):
        # loop through and get html data from widgets, to make a dict ready to save as json
        tempDict = {"cards":[]}


        # for i in range(self.listTableWidget.rowCount()):
        if self.list_table_widget.rowCount() != False:

            for key in self.text_edits_front.keys():
                i = int(key)
                card = {}
                card["front"] = str(self.makeSoup(self.text_edits_front[i].toHtml()).body)
                card["back"] = str(self.makeSoup(self.text_edits_back[i].toHtml()).body)
                img = None
                try:
                    imgSoup = self.makeSoup(self.text_edits_img[i].toHtml())
                    img = imgSoup.find("img")["src"]
                except:
                    pass

                if img is not None:
                    card["img"] = str(img)
                else:
                    card["img"] = ""
                tempDict["cards"].append(card)

        #delete old json and save new one
        path = os.path.join(os.getcwd(),"App","flashcards.json")
        if os.path.exists(path):
            os.remove(path)
        with open(path,"w") as f:
            myJson = json.dumps(tempDict)
            json.dump(tempDict, f)
        self.text_edits_back = {}
        self.text_edits_front = {}
        self.text_edits_img = {}
        self.card_dict = self.get_flashcard_data_from_json()
        self.close()


    def makeSoup(self,html):
        soup = BeautifulSoup(html,"html.parser")
        return soup

    def setup_table_widget(self):
        self.card_dict = self.get_flashcard_data_from_json()
        num_of_cards = len(self.card_dict["cards"])
        self.list_table_widget.setRowCount(num_of_cards)
        self.list_table_widget.setColumnCount(4)
        self.list_table_widget.setHorizontalHeaderLabels(["Del","Front","Back","Image"])
        self.list_table_widget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.list_table_widget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        for i, card in enumerate(self.card_dict["cards"]):
            self.text_edits_front[i] = self.create_text_edit_widget(card["front"])
            self.text_edits_back[i] = self.create_text_edit_widget(card["back"])
            if card["img"] != "":
                self.text_edits_img[i] = self.create_text_edit_widget('<img src="' + card["img"] + '>')
                self.list_table_widget.setCellWidget(i, 3,self.text_edits_img[i])
            btn = self.make_btn(i)
            self.list_table_widget.setCellWidget(i, 1, self.text_edits_front[i])
            self.list_table_widget.setCellWidget(i, 2, self.text_edits_back[i])
            self.list_table_widget.setCellWidget(i,0,btn)
        self.list_table_widget.resizeColumnsToContents()
        self.list_table_widget.resizeRowsToContents()
        print(self.text_edits_front)
        print(self.text_edits_back)
        print(self.text_edits_img)


    def create_text_edit_widget(self,html):
        text_edit_widget = QTextEdit()
        # textEditWidget.setFixedHeight(100)
        text_edit_widget.setFont(QtGui.QFont("Calibri",10))
        text_edit_widget.setHtml(html)
        return text_edit_widget

    def make_btn(self,i):
        self.btn[i] = QPushButton("X")
        self.btn[i].setMaximumWidth(50)
        self.btn[i].clicked.connect(self.remove_table_row)
        return self.btn[i]
    
    def remove_table_row(self):
        current_index = self.list_table_widget.currentIndex().row()
        try:

            self.list_table_widget.removeRow(current_index)
            del self.text_edits_front[current_index]
            del self.text_edits_back[current_index]
            try:
                del self.text_edits_img[current_index]
            except KeyError:
                pass
        except Exception as e:
            print(e)
        print(current_index)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FlashcardManager()
    window.show()
    sys.exit(app.exec())