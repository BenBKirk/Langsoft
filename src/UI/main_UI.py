"""
THIS IS THE MAIN UI OF THE APP
"""
import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import * #QApplication, QWidget, QFrame, QLineEdit, QHBoxLayout, QVBoxLayout, QSplitter, QTableWidget, QTableWidgetItem, QAbstractItemView, QTabWidget, QToolBar
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import QUrl, QSize, Qt
from PyQt5.QtGui import QIcon
from .custom_text_browser import CustomTextBrowser
import os

class MainUIWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.top = 1000
        self.left = 1000
        self.width = 1000
        self.height = 600
        self.left_pane = LeftPane()
        self.top_right_pane = TopRightPane()
        self.bottom_right_pane = BottomRightPane()
        split_down_middle = QSplitter(Qt.Horizontal)
        split_right_side = QSplitter(Qt.Vertical)
        split_right_side.addWidget(self.top_right_pane)
        split_right_side.addWidget(self.bottom_right_pane)
        split_right_side.setSizes([5,2000])
        split_down_middle.addWidget(self.left_pane)
        split_down_middle.addWidget(split_right_side)
        split_down_middle.setSizes([1000,200])
        vbox = QVBoxLayout()
        vbox.addWidget(split_down_middle)
        self.setLayout(vbox)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.left_pane.browser.setFocus()
    
    def setup_dark_theme(self):
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53,53,53))
        palette.setColor(QtGui.QPalette.WindowText, Qt.white)
        palette.setColor(QtGui.QPalette.Base, QtGui.QColor(15,15,15))
        palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53,53,53))
        palette.setColor(QtGui.QPalette.ToolTipBase, Qt.white)
        palette.setColor(QtGui.QPalette.ToolTipText, Qt.white)
        palette.setColor(QtGui.QPalette.Text, Qt.white)
        palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53,53,53))
        palette.setColor(QtGui.QPalette.ButtonText, Qt.white)
        palette.setColor(QtGui.QPalette.BrightText, Qt.red)
        palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142,45,197).lighter())
        palette.setColor(QtGui.QPalette.HighlightedText, Qt.black)
        return palette
    

    
    def check_ui_settings(self):
        if self.json_settings["dark_theme"] ==  True:
            self.setPalette(self.dark_theme_palette)
            self.settings.setPalette(self.dark_theme_palette)
            self.flashcards_list.setPalette(self.dark_theme_palette)
            self.set_icons(True)
        else:
            self.set_icons(False)
        
    def set_icons(self,dark):
        if dark:
            for x in self.left_pane.toolbar.actions() + self.top_right_pane.toolbar.actions():
                name = x.text()
                path = os.path.join(os.getcwd(),"src","img",name + "_dark.png")
                x.setIcon(QIcon(path))
        else:
            for x in self.left_pane.toolbar.actions() + self.top_right_pane.toolbar.actions():
                name = x.text()
                path = os.path.join(os.getcwd(),"src","img",name + ".png")
                x.setIcon(QIcon(path))

    def toggle_theme(self,state):
        if state == 2:
            self.setPalette(self.dark_theme_palette)
            self.settings.setPalette(self.dark_theme_palette)
            self.flashcards_list.setPalette(self.dark_theme_palette)
            self.set_icons(True)
        else:
            self.setPalette(QtGui.QPalette())
            self.settings.setPalette(QtGui.QPalette())
            self.flashcards_list.setPalette(QtGui.QPalette())
            self.set_icons(False)


class LeftPane(QWidget):
    def __init__(self):
        super().__init__()
        self.toolbar = QToolBar()
        spacer_widget = QWidget()
        spacer_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        spacer_widget2 = QWidget()
        spacer_widget2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        blank_file_action = QAction("blank",self)
        blank_file_action.setToolTip("new blank file")
        recent_file_action = QAction("recent_file",self)
        recent_file_action.setToolTip("open recent file")
        folder_action = QAction("open",self)
        folder_action.setToolTip("Open a File")
        folder_action.setShortcut('Ctrl+o')
        save_action = QAction("save",self)
        save_action.setToolTip("save this file")
        save_action.setShortcut('Ctrl+s')
        helpaction = QAction("help",self) 
        helpaction.setToolTip("How To Use This Program")
        self.play_action = QAction("play",self)
        skip_back_action = QAction("skip_back",self)
        skip_forward_action = QAction("skip_forward",self)
        settings_action = QAction("settings",self)
        highlight_action = QAction("highlight",self)
        highlight_action.setToolTip("Highlight Discourse Features")
        format_action = QAction("format",self)
        format_action.setToolTip("Format selected text")
        search_action = QAction("search",self)
        search_action.setToolTip("Search for a word")
        self.searchbar_lineedit = QLineEdit()
        self.searchbar_lineedit.setFixedHeight(40)
        self.searchbar_lineedit.setFont(QtGui.QFont("Calibri",10))
        self.toolbar.addAction(folder_action)
        self.toolbar.addWidget(QLabel(" ")) 
        self.toolbar.addAction(save_action)
        self.toolbar.addWidget(QLabel(" ")) 
        self.toolbar.addAction(blank_file_action)
        self.toolbar.addWidget(QLabel(" ")) 
        self.toolbar.addAction(recent_file_action)
        self.toolbar.addWidget(QLabel(" ")) 
        self.toolbar.addWidget(spacer_widget)
        self.toolbar.addAction(skip_back_action)
        self.toolbar.addAction(self.play_action)
        self.toolbar.addAction(skip_forward_action)
        self.toolbar.addWidget(spacer_widget2)
        self.toolbar.addWidget(self.searchbar_lineedit)
        self.toolbar.addAction(search_action)
        self.toolbar.addWidget(QLabel(" ")) 
        self.toolbar.addAction(format_action)
        self.toolbar.addWidget(QLabel(" ")) 
        self.toolbar.addAction(highlight_action)
        self.toolbar.addWidget(QLabel(" ")) 
        self.toolbar.addAction(helpaction)
        self.toolbar.addWidget(QLabel(" ")) 
        self.toolbar.addAction(settings_action)
        self.audio_slider = QSlider()
        self.audio_slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.audio_slider.setOrientation(Qt.Horizontal)
        self.audio_slider.setFixedHeight(30)
        self.browser = CustomTextBrowser()
        self.browser.setFont(QtGui.QFont("Calibri",14))
        self.browser.setWordWrapMode(QtGui.QTextOption.WordWrap)
        layout_for_browser_and_buttons = QVBoxLayout()
        layout_for_browser_and_buttons.addWidget(self.toolbar)
        layout_for_browser_and_buttons.addWidget(self.audio_slider)
        layout_for_browser_and_buttons.addWidget(self.browser)
        self.setLayout(layout_for_browser_and_buttons)

class TopRightPane(QWidget):
    def __init__(self):
        super().__init__()
        self.flash_front = QTextEdit()
        self.flash_front.setFont(QtGui.QFont("Calibri",10))
        self.flash_front.setMinimumHeight(60)
        self.flash_back = QTextEdit()
        self.flash_back.setFont(QtGui.QFont("Calibri",10))
        self.flash_back.setMinimumHeight(60)
        self.make_flash_btn = QPushButton(text="Make Flashcard")
        self.make_flash_btn.setFont(QtGui.QFont("Calibri",12,200))
        self.make_flash_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.make_flash_btn.setFixedHeight(40)
        list_of_flashcards_action = QAction("list",self)
        list_of_flashcards_action.setToolTip("List of Flashcards")
        download_flashcards_action = QAction("download",self)
        download_flashcards_action.setToolTip("Download Flashcards as Anki deck")
        add_sound_action = QAction("no_sound",self)
        add_sound_action.setToolTip("Add audio to flashcard")
        spacer_widget3 = QWidget()
        spacer_widget3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        spacer_widget4 = QWidget()
        spacer_widget4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolbar = QToolBar()
        self.toolbar.setFixedHeight(50)
        self.toolbar.addAction(list_of_flashcards_action)
        self.toolbar.addAction(add_sound_action)
        self.toolbar.addWidget(spacer_widget3) 
        self.toolbar.addWidget(self.make_flash_btn)
        self.toolbar.addWidget(spacer_widget4) 
        self.toolbar.addAction(download_flashcards_action)
        label1 = QLabel("Selection in context = Front of flashcard:")
        label1.setFixedHeight(10)
        label2 = QLabel("Translation/Definition = Back of flashcard:")
        label2.setFixedHeight(10)
        label3 = QLabel("Track word/phrase in all texts by selecting how well you know it. Note:the difinition above well be saved too.")
        label3 = QLabel("Click a button below to save and highlight the selection along with your definition")
        label3.setFixedHeight(15)
        self.unknown_btn = QPushButton("1.Unknown")
        self.semi_known_btn = QPushButton("2.Semi-Known")
        self.known_btn = QPushButton("3.Known")
        # self.confidence_btn4 = QPushButton("4.Well-Known")
        self.unknown_btn.setStyleSheet(f"background-color : rgb(255,0,0)")
        self.semi_known_btn.setStyleSheet(f"background-color : rgb(255,255,0)")
        self.known_btn.setStyleSheet(f"background-color : rgb(0,255,0)")
        # self.confidence_btn4.setStyleSheet(f"background-color : rgb(255,255,255)")
        color_btn_layout = QHBoxLayout()
        color_btn_layout.addWidget(self.unknown_btn)    
        color_btn_layout.addWidget(self.semi_known_btn)
        color_btn_layout.addWidget(self.known_btn)
        # color_btn_layout.addWidget(self.confidence_btn4)
        widget_for_btn_layout = QWidget()
        widget_for_btn_layout.setLayout(color_btn_layout)
        split_top_right = QSplitter(Qt.Vertical)
        split_top_right.addWidget(label1)
        split_top_right.addWidget(self.flash_front)
        split_top_right.addWidget(label2)
        split_top_right.addWidget(self.flash_back)
        split_top_right.addWidget(label3)
        split_top_right.addWidget(widget_for_btn_layout)#
        split_top_right.addWidget(self.toolbar)

        layout = QVBoxLayout()
        layout.addWidget(split_top_right)
        self.setLayout(layout)
class BottomRightPane(QWidget):
    def __init__(self):
        super().__init__()
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def add_tab(self,index, name,url):
        self.my_tabs[index] = QWebEngineView() 
        self.my_tabs[index].setUrl(QUrl(url))
        self.tabs.addTab(self.my_tabs[index],name)

    def start_tabs(self,online_tools):
        print(online_tools)
        self.tabs.clear()
        self.my_tabs = {}
        for i, row in enumerate(online_tools): 
            self.add_tab(i,row[1],row[2].replace("WORD","").replace("SENT","")) #replacing with empty so that the web pages start with a search term.

 
if __name__ == "__main__":
    from custom_text_browser import CustomTextBrowser
    import sys
    app = QApplication(sys.argv)
    window = MainUIWidget()
    window.showMaximized()
    sys.exit(app.exec())