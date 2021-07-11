"""
UI only
"""
import sys
from PyQt5.QtWidgets import * 
from PyQt5 import QtGui
from PyQt5 import QtCore
import json
import os 
import logging
logging.basicConfig(level=logging.DEBUG,filename="app.log",format='%(asctime)s - %(levelname)s - %(message)s')

class SettingsPage(QWidget):
    def __init__(self):
        super(SettingsPage, self).__init__()
        self.user_tab = UsersTab()
        self.online_tools_tab = OnlineToolsTab()
        self.other_tab = OtherTab()
        self.grammar_tab = GrammarTab()
        self.font_L = QtGui.QFont("Ubuntu",12, 200)
        self.font_S = QtGui.QFont("Ubuntu",7)
        self.resize(800,700)
        vbox = QVBoxLayout()
        self.tabs = QTabWidget()
        self.tabs.addTab(self.user_tab,"Users")
        self.tabs.addTab(self.online_tools_tab,"Online Tools (URLs)")
        self.tabs.addTab(self.grammar_tab,"Grammar Highlighter")
        self.tabs.addTab(self.other_tab,"Other")
        vbox.addWidget(self.tabs)
        self.save_button = QPushButton("Save")
        self.save_button.setFont(self.font_L)
        self.save_button.setMaximumWidth(100)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFont(self.font_L)
        self.cancel_button.setMaximumWidth(100)
        hbox = QHBoxLayout()
        hbox.addWidget(self.cancel_button)
        hbox.addWidget(self.save_button)
        widget_for_buttons = QWidget()
        widget_for_buttons.setLayout(hbox)
        vbox.addWidget(widget_for_buttons)
        self.setLayout(vbox)
        self.setWindowTitle("Settings")
        self.setWindowIcon(QtGui.QIcon(os.path.join("src", "img", "settings.png")))

    def load_online_tool_settings(self,online_tools):
        self.online_tools_tab.online_tools_table_widget.clear()
        self.online_tools_tab.online_tools_table_widget.setRowCount(len(online_tools)+1)
        self.online_tools_tab.online_tools_table_widget.setColumnCount(3)
        self.online_tools_tab.online_tools_table_widget.setHorizontalHeaderLabels(["Del","Tab Name", "URL"])
        for i,val in enumerate(online_tools):
            del_btn = self.online_tools_tab.make_delete_btn(i)
            self.online_tools_tab.online_tools_table_widget.setCellWidget(i,0, del_btn)
            self.online_tools_tab.online_tools_table_widget.setItem(i,1,QTableWidgetItem(val[1]))
            self.online_tools_tab.online_tools_table_widget.setItem(i,2,QTableWidgetItem(val[2]))
        self.online_tools_tab.online_tools_table_widget.resizeColumnsToContents()
    
    def load_other_settings(self,other_settings):
        self.other_tab.dark_theme_checkbox.setChecked(other_settings["dark_theme"])
        self.other_tab.autofill_checkbox.setChecked(other_settings["autofill_back_of_flashcard"])
    
    def load_user(self,all_users,current_user):
        self.user_tab.user_combobox.blockSignals(True)
        self.user_tab.user_combobox.clear()
        self.user_tab.user_combobox.addItems(all_users)
        self.user_tab.user_combobox.setCurrentText(current_user["name"])
        self.user_tab.user_combobox.blockSignals(False)
    
    def load_grammar_rules(self,grammar_rules):
        self.grammar_tab.grammar_table_widget.clear()
        self.grammar_tab.grammar_table_widget.setRowCount(len(grammar_rules)+1)
        self.grammar_tab.grammar_table_widget.setColumnCount(7)
        self.grammar_tab.grammar_table_widget.setHorizontalHeaderLabels(["Del","On","Rule Name","Color","Opacity","Style","List/Regex"])
        for i,rule in enumerate(grammar_rules):
            del_btn = self.grammar_tab.make_del_btn(i)
            self.grammar_tab.grammar_table_widget.setCellWidget(i,0, del_btn)
            on_widget = self.grammar_tab.make_on_widget(i,rule[2])
            self.grammar_tab.grammar_table_widget.setCellWidget(i,1,on_widget)
            self.grammar_tab.grammar_table_widget.setItem(i,2,QTableWidgetItem(rule[3]))
            color_btn = self.grammar_tab.make_gram_color_widget(i,rule[4])
            self.grammar_tab.grammar_table_widget.setCellWidget(i,3,color_btn)
            opacity_widget = self.grammar_tab.make_opacity_widget(i,rule[5])
            self.grammar_tab.grammar_table_widget.setCellWidget(i,4,opacity_widget)
            style_widget = self.grammar_tab.make_style_widget(i,rule[6])
            self.grammar_tab.grammar_table_widget.setCellWidget(i,5,style_widget)
            self.grammar_tab.grammar_table_widget.setItem(i,6,QTableWidgetItem(rule[7]))
        self.grammar_tab.grammar_table_widget.resizeColumnsToContents()



class UsersTab(QWidget):
    def __init__(self):
        super(UsersTab, self).__init__()
        self.table = QTableWidget()
        self.user_combobox = QComboBox()
        self.user_delete = QPushButton("Delete")
        # self.user_delete.setIcon(QtGui.QIcon(os.path.join(os.getcwd(),"src","img","user.png")))
        self.add_user_name = QLineEdit()
        self.add_user_btn = QPushButton("Add New User")
        user_layout = QHBoxLayout()
        user_layout.addWidget(self.user_combobox)
        user_layout.addWidget(self.user_delete)
        layout = QFormLayout()
        layout.addRow(QLabel(""),QLabel("Having more than one users allows you to have different settings for different people or different languages."))
        layout.addRow(QLabel("Users:"),user_layout)
        layout.addRow(self.add_user_btn,self.add_user_name)
        layout.addRow(QLabel("Note: Default settings will be copied to new users as a starting point but can be customised."))
        layout.addRow(QLabel(""))
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
class OnlineToolsTab(QWidget):
    online_tools_list = {}
    online_tools_delete_btn = {}
    def __init__(self):
        super(OnlineToolsTab, self).__init__()
        self.online_tools_table_widget = QTableWidget()
        self.online_tools_table_widget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.online_tools_table_widget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.online_tools_table_widget.itemChanged.connect(self.add_new_dict_item)
        layout = QVBoxLayout()
        label =QLabel("Enter the full URL to an online dictionary you want to use. \nJust be sure to change the search term to WORD or SENT so that the program knows how to use the URL.\nIf you are unsure just reset to defaults for an example.")
        label.setWordWrap(True)
        layout.addWidget(label)
        self.restore_defaults = QPushButton("Load Defaults/Example Settings")
        # self.restore_defaults.setMaximumWidth(120)
        layout.addWidget(self.restore_defaults)
        layout.addWidget(self.online_tools_table_widget)
        self.setLayout(layout)
    
    def add_new_dict_item(self):
        number_of_rows = self.online_tools_table_widget.rowCount()
        current_index = self.online_tools_table_widget.currentIndex().row()+1
        if number_of_rows == current_index:
            try:
                tab_name = self.online_tools_table_widget.item(current_index-1,1).text() 
            except:
                logging.exception("adding new online tool")
                tab_name = None
            try:
                URL = self.online_tools_table_widget.item(current_index-1,2).text() 
            except:
                logging.exception("adding new online tool")
                URL = None

            if tab_name != None and URL != None:
                self.online_tools_table_widget.setCellWidget(current_index -1, 0, self.make_delete_btn(current_index-1))
                self.online_tools_table_widget.setRowCount(current_index+1)

    def make_delete_btn(self,i):
        self.online_tools_delete_btn[i] = QPushButton("X")
        self.online_tools_delete_btn[i].setMaximumWidth(50)
        self.online_tools_delete_btn[i].clicked.connect(lambda: self.online_tools_table_widget.removeRow(self.online_tools_table_widget.currentIndex().row()))
        return self.online_tools_delete_btn[i]

class GrammarTab(QWidget):
    del_btn = {}
    color_btn = {}
    opacity_widget = {}
    style_widget = {}
    on_widget = {}
    def __init__(self):
        super(GrammarTab, self).__init__()
        self.grammar_table_widget = QTableWidget()
        self.grammar_table_widget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.grammar_table_widget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.grammar_table_widget.setWordWrap(True)
        self.grammar_table_widget.itemChanged.connect(self.add_new_grammar_item)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Here you can change the grammar/discourse highlighting rules."))
        layout.addWidget(self.grammar_table_widget)
        self.setLayout(layout)

    def add_new_grammar_item(self):
        number_of_rows = self.grammar_table_widget.rowCount()
        current_index = self.grammar_table_widget.currentIndex().row()
        if number_of_rows == current_index + 1:
            try:
                rule_name = self.grammar_table_widget.item(current_index,2).text() 
            except:
                # logging.exception("adding discourse rule")
                rule_name = None
            try:
                word_list = self.grammar_table_widget.item(current_index,6).text() 
            except:
                # logging.exception("adding discourse rule")
                word_list = None

            if rule_name != None:# and word_list != None:
                self.grammar_table_widget.blockSignals(True)
                self.grammar_table_widget.setCellWidget(current_index, 0, self.make_del_btn(current_index))
                self.grammar_table_widget.setCellWidget(current_index, 1, self.make_on_widget(current_index,True))
                self.grammar_table_widget.setItem(current_index,2,QTableWidgetItem(rule_name))
                self.grammar_table_widget.setCellWidget(current_index, 3, self.make_gram_color_widget(current_index,"255,0,0"))
                self.grammar_table_widget.setCellWidget(current_index, 4, self.make_opacity_widget(current_index,0.8))
                self.grammar_table_widget.setCellWidget(current_index, 5, self.make_style_widget(current_index,"highlight"))
                self.grammar_table_widget.setItem(current_index,6,QTableWidgetItem(word_list))
                self.grammar_table_widget.setRowCount(current_index+2)
                self.grammar_table_widget.blockSignals(False)

    def make_del_btn(self,i):
        self.del_btn[i] = QPushButton("X")
        self.del_btn[i].setMaximumWidth(50)
        self.del_btn[i].clicked.connect(lambda: self.grammar_table_widget.removeRow(self.grammar_table_widget.currentIndex().row()))
        return self.del_btn[i]

    def make_gram_color_widget(self,i,color):
        self.color_btn[i] = QPushButton("Color")
        self.color_btn[i].setStyleSheet(f"background-color : rgb({color})")
        self.color_btn[i].clicked.connect(lambda: self.set_color(self.grammar_table_widget.currentIndex().row()))
        return self.color_btn[i]
    
    def make_on_widget(self,i,val):
        self.on_widget[i] = QCheckBox()
        self.on_widget[i].setChecked(val)
        return self.on_widget[i]
    
    def make_opacity_widget(self,i,opacity):
        self.opacity_widget[i] = QDoubleSpinBox()
        self.opacity_widget[i].setValue(opacity)
        self.opacity_widget[i].setSingleStep(0.1)
        return self.opacity_widget[i]
    
    def make_style_widget(self,i,style):
        self.style_widget[i] = QComboBox()
        self.style_widget[i].addItems(["underline","highlight"])
        self.style_widget[i].setCurrentText(style)
        return self.style_widget[i]

    def set_color(self,i):
        new_color = QColorDialog.getColor()
        new_color = str(new_color.getRgb()[:-1]).strip()
        self.color_btn[i].setStyleSheet(f"background-color : rgb{new_color}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SettingsPage()
    window.show()
    sys.exit(app.exec())