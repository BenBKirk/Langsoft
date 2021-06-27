
import sys
from PyQt5.QtWidgets import * 
from PyQt5 import QtGui
from PyQt5 import QtCore
import json
import os 

class SettingsPage(QWidget):
    def __init__(self):
        super(SettingsPage, self).__init__()
        self.dict_tab = DictTab()
        self.other_tab = OtherTab()
        self.discourse_tab = DiscourseTab()
        self.font_L = QtGui.QFont("Ubuntu",12, 200)
        self.font_S = QtGui.QFont("Ubuntu",7)
        self.resize(800,700)
        vbox = QVBoxLayout()
        self.tabs = QTabWidget()
        self.tabs.addTab(UsersTab(),"Users")
        self.tabs.addTab(self.dict_tab,"Online Tools (URLs)")
        self.tabs.addTab(self.discourse_tab,"Discourse Highlighter")
        self.tabs.addTab(self.other_tab,"Other")
        vbox.addWidget(self.tabs)
        self.save_button = QPushButton("Save")
        self.save_button.setFont(self.font_L)
        self.save_button.setMaximumWidth(100)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFont(self.font_L)
        self.cancel_button.setMaximumWidth(100)
        self.cancel_button.clicked.connect(self.close)
        hbox = QHBoxLayout()
        hbox.addWidget(self.cancel_button)
        hbox.addWidget(self.save_button)
        widget_for_buttons = QWidget()
        widget_for_buttons.setLayout(hbox)
        vbox.addWidget(widget_for_buttons)
        self.setLayout(vbox)
        self.setWindowTitle("Settings")
        self.setWindowIcon(QtGui.QIcon(os.path.join("App", "img", "settings.png")))
        self.dict_tab.restore_defaults.clicked.connect(lambda: self.load_settings(True))
    
    def load_settings(self,default):
        data = self.get_json_data()
        if default:
            tabs = data["default_tabs"]
        else:
            tabs = data["tabs"]
        self.dict_tab.dict_table_widget.clearContents()
        self.dict_tab.dict_table_widget.setRowCount(len(tabs)+1)
        self.dict_tab.dict_table_widget.setColumnCount(3)
        self.dict_tab.dict_table_widget.setHorizontalHeaderLabels(["Del","Tab Name", "URL"])
        for i, tab in enumerate(tabs):
            dict_btn = self.dict_tab.make_dict_btn(i)
            self.dict_tab.dict_table_widget.setCellWidget(i,0, dict_btn)
            self.dict_tab.dict_table_widget.setItem(i,1,QTableWidgetItem(tab[0]))
            self.dict_tab.dict_table_widget.setItem(i,2,QTableWidgetItem(tab[1]))
        self.dict_tab.dict_table_widget.resizeColumnsToContents()
        # theme settings 
        if data["dark_theme"]:
            self.other_tab.dark_theme_checkbox.setChecked(True)
        if data["autofill_flashcards"]:
            self.other_tab.autofill_checkbox.setChecked(True)
        #Discourse settings
        discourse_data = data["discourse_highlighter"]
        self.discourse_tab.discourse_table_widget.setColumnCount(4)
        self.discourse_tab.discourse_table_widget.setRowCount(len(discourse_data.items())+1)
        self.discourse_tab.discourse_table_widget.setHorizontalHeaderLabels(["Del","Category","Colour", "List Of Words"])
        index = 0
        for key,value in discourse_data.items():
            color = value["color"]
            dis_btn = self.discourse_tab.make_dis_btn(index)
            color_widget = self.discourse_tab.make_dis_color_widget(index,color)
            # color_widget.setStyleSheet("background-color : rgb(255,0,255")
            self.discourse_tab.discourse_table_widget.setCellWidget(index,0,dis_btn)
            self.discourse_tab.discourse_table_widget.setItem(index,1,QTableWidgetItem(key))
            self.discourse_tab.discourse_table_widget.setCellWidget(index,2,color_widget)
            self.discourse_tab.discourse_table_widget.setItem(index,3,QTableWidgetItem(", ".join(value["list"])))
            index += 1
        self.discourse_tab.discourse_table_widget.resizeColumnsToContents()

    def get_json_data(self):
        with open(os.path.join(os.getcwd(),"App","settings.json"),"r+") as f:
            data = json.load(f)
            return data

class UsersTab(QWidget):
    def __init__(self):
        super(UsersTab, self).__init__()
        self.table = QTableWidget()
        self.user_combobox = QComboBox()
        self.user_delete = QPushButton("Del")
        self.user_delete.setIcon(QtGui.QIcon(os.path.join(os.getcwd(),"App","img","user.png")))
        self.language_combobox = QComboBox()
        self.add_language_btn = QPushButton("Add New Language")
        self.add_language_name = QLineEdit()
        self.add_user_name = QLineEdit()
        self.add_user_btn = QPushButton("Add New User")
        self.user_combobox.addItems(["bob","fred","jim","john"])
        self.language_combobox.addItems(["english","indonesian","japanese",])
        user_layout = QHBoxLayout()
        user_layout.addWidget(self.user_combobox)
        user_layout.addWidget(self.user_delete)
        layout = QFormLayout()
        layout.addRow(QLabel(""),QLabel("Note: Selecting a user or language will update settings in other tabs"))
        layout.addRow(QLabel("Users:"),user_layout)
        layout.addRow(self.add_user_btn,self.add_user_name)
        layout.addRow(QLabel(""))
        layout.addRow(QLabel("Language:"),self.language_combobox)
        layout.addRow(self.add_language_btn,self.add_language_name)
        layout.addRow(QLabel(""),QLabel("Note: New languages will be added to the selected user above"))
        self.setLayout(layout)

        
class OtherTab(QWidget):
    def __init__(self):
        super(OtherTab, self).__init__()
        self.dark_theme_checkbox = QCheckBox("Dark Theme")
        self.autofill_checkbox = QCheckBox("Autofill Back Of Flashcard")
        layout = QVBoxLayout()
        layout.addWidget(self.dark_theme_checkbox)
        layout.addWidget(self.autofill_checkbox)
        self.setLayout(layout)
class DictTab(QWidget):
    dictList = {}
    dict_btn = {}
    def __init__(self):
        super(DictTab, self).__init__()
        self.dict_table_widget = QTableWidget()
        self.dict_table_widget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.dict_table_widget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.dict_table_widget.itemChanged.connect(self.add_new_dict_item)
        layout = QVBoxLayout()
        label =QLabel("Enter the full URL to an online dictionary you want to use. \nJust be sure to change the search term to WORD or SENT so that the program knows how to use the URL.\nIf you are unsure just reset to defaults for an example.")
        label.setWordWrap(True)
        layout.addWidget(label)
        self.restore_defaults = QPushButton("Reset to Defaults")
        self.restore_defaults.setMaximumWidth(120)
        layout.addWidget(self.restore_defaults)
        layout.addWidget(self.dict_table_widget)
        self.setLayout(layout)
    
    def add_new_dict_item(self):
        number_of_rows = self.dict_table_widget.rowCount()
        current_index = self.dict_table_widget.currentIndex().row()+1
        if number_of_rows == current_index:
            try:
                tab_name = self.dict_table_widget.item(current_index-1,1).text() 
            except:
                tab_name = None
            try:
                URL = self.dict_table_widget.item(current_index-1,2).text() 
            except:
                URL = None

            if tab_name != None and URL != None:
                self.dict_table_widget.setCellWidget(current_index -1, 0, self.make_dict_btn(current_index-1))
                self.dict_table_widget.setRowCount(current_index+1)

    def make_dict_btn(self,i):
        self.dict_btn[i] = QPushButton("X")
        self.dict_btn[i].setMaximumWidth(50)
        self.dict_btn[i].clicked.connect(lambda: self.dict_table_widget.removeRow(self.dict_table_widget.currentIndex().row()))
        return self.dict_btn[i]

class DiscourseTab(QWidget):
    dis_btn = {}
    dis_color = {}
    def __init__(self):
        super(DiscourseTab, self).__init__()
        self.discourse_table_widget = QTableWidget()
        self.discourse_table_widget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.discourse_table_widget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.discourse_table_widget.setWordWrap(True)
        self.discourse_table_widget.itemChanged.connect(self.add_new_discourse_item)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Here you can change the discourse highlighting rules. \n\nKnown issue: in this version the category names need to be unique. I plan change that at some point "))
        layout.addWidget(self.discourse_table_widget)
        self.setLayout(layout)

    def add_new_discourse_item(self):
        number_of_rows = self.discourse_table_widget.rowCount()
        current_index = self.discourse_table_widget.currentIndex().row()
        if number_of_rows == current_index + 1:
            try:
                cat_key = self.discourse_table_widget.item(current_index,1).text() 
            except:
                cat_key = None
            try:
                cat_list = self.discourse_table_widget.item(current_index,3).text() 
            except:
                cat_list = None

            if cat_key != None and cat_list != None:
                self.discourse_table_widget.setCellWidget(current_index, 0, self.make_dis_btn(current_index))
                self.discourse_table_widget.setCellWidget(current_index, 2, self.make_dis_color_widget(current_index,"255,0,0"))
                self.discourse_table_widget.setRowCount(current_index+2)

    def make_dis_btn(self,i):
        self.dis_btn[i] = QPushButton("X")
        self.dis_btn[i].setMaximumWidth(50)
        self.dis_btn[i].clicked.connect(lambda: self.discourse_table_widget.removeRow(self.discourse_table_widget.currentIndex().row()))
        return self.dis_btn[i]

    def make_dis_color_widget(self,i,color):
        self.dis_color[i] = QPushButton("Color")
        self.dis_color[i].setStyleSheet(f"background-color : rgb({color})")
        self.dis_color[i].clicked.connect(lambda: self.set_color(self.discourse_table_widget.currentIndex().row()))
        return self.dis_color[i]

    def set_color(self,i):
        new_color = QColorDialog.getColor()
        new_color = str(new_color.getRgb()[:-1]).strip()
        self.dis_color[i].setStyleSheet(f"background-color : rgb{new_color}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SettingsPage()
    window.show()
    sys.exit(app.exec())