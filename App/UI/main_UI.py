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
    myTabs = {}
    def __init__(self):
        super().__init__()
        self.top = 1000
        self.left = 1000
        self.width = 1000
        self.height = 600
        self.left_pane = Left_Pane()

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

        self.toolbar2 = QToolBar()
        list_of_flashcards_action = QAction("list",self)
        list_of_flashcards_action.setToolTip("List of Flashcards")
        download_flashcards_action = QAction("download",self)
        download_flashcards_action.setToolTip("Download Flashcards as Anki deck")
        spacer_widget3 = QWidget()
        spacer_widget3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        spacer_widget4 = QWidget()
        spacer_widget4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolbar2.setFixedHeight(50)
        self.toolbar2.addAction(list_of_flashcards_action)
        self.toolbar2.addWidget(spacer_widget3) 
        self.toolbar2.addWidget(self.make_flash_btn)
        self.toolbar2.addWidget(spacer_widget4) 
        self.toolbar2.addAction(download_flashcards_action)
        # self.setIcons()
        # self.toolBar2.addWidget(QLabel("    ")) 

        #web browsers
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)


        vbox = QVBoxLayout()
        splitter = QSplitter(Qt.Horizontal)
        splitter2 = QSplitter(Qt.Vertical)
        splitter3 = QSplitter(Qt.Vertical)
        label1 = QLabel("context")
        label1.setFixedHeight(10)
        splitter3.addWidget(label1)
        splitter3.addWidget(self.flash_front)
        label2 = QLabel("selection")
        label2.setFixedHeight(10)
        splitter3.addWidget(label2)
        splitter3.addWidget(self.flash_back)
        splitter2.addWidget(splitter3)
        splitter3.addWidget(self.toolbar2) 
        splitter2.addWidget(self.tabs)
        splitter2.setSizes([5,2000])
        splitter.addWidget(self.left_pane)
        splitter.addWidget(splitter2)
        splitter.setSizes([500,500])
        vbox.addWidget(splitter)
        self.setLayout(vbox)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
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
            for x in self.left_pane.toolbar.actions() + self.toolbar2.actions():
                name = x.text()
                path = os.path.join(os.getcwd(),"App","img",name + "_dark.png")
                x.setIcon(QIcon(path))
        else:
            for x in self.toolbar.actions() + self.toolbar2.actions():
                name = x.text()
                path = os.path.join(os.getcwd(),"App","img",name + ".png")
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

    def add_tab(self,index, name,url):
        self.my_tabs[index] = QWebEngineView() 
        self.my_tabs[index].setUrl(QUrl(url))
        self.tabs.addTab(self.my_tabs[index],name)

    def start_tabs(self):
        self.my_tabs = {}
        tabs = self.json_settings     
        # print(tabs)
        for i, tab in enumerate(tabs["tabs"]): 
            self.add_tab(i,tab[0],tab[1].replace("WORD","").replace("SENT",""))

class Left_Pane(QWidget):
    def __init__(self):
        super().__init__()
        self.toolbar = QToolBar()
        spacer_widget = QWidget()
        spacer_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        spacer_widget2 = QWidget()
        spacer_widget2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
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
        self.toolbar.addAction(folder_action)
        self.toolbar.addWidget(QLabel(" ")) 
        self.toolbar.addWidget(QLabel(" ")) 
        self.toolbar.addAction(save_action)
        self.toolbar.addWidget(QLabel(" ")) 
        self.toolbar.addWidget(QLabel(" ")) 
        self.toolbar.addWidget(spacer_widget)
        self.toolbar.addAction(skip_back_action)
        self.toolbar.addAction(self.play_action)
        self.toolbar.addAction(skip_forward_action)
        self.toolbar.addWidget(spacer_widget2)
        # self.toolbar.addWidget(QLabel(" ")) 
        self.toolbar.addAction(format_action)
        self.toolbar.addWidget(QLabel(" ")) 
        self.toolbar.addAction(highlight_action)
        self.toolbar.addWidget(QLabel(" ")) 
        self.toolbar.addAction(helpaction)
        self.toolbar.addWidget(QLabel(" ")) 
        self.toolbar.addAction(settings_action)
        #audio slider
        self.audio_slider = QSlider()
        self.audio_slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.audio_slider.setOrientation(Qt.Horizontal)
        self.audio_slider.setFixedHeight(30)
        #
        self.browser = CustomTextBrowser()
        self.browser.setFont(QtGui.QFont("Calibri",14))
        self.browser.setWordWrapMode(QtGui.QTextOption.WordWrap)
        # widget_for_layout = QWidget()
        layout_for_browser_and_buttons = QVBoxLayout()
        layout_for_browser_and_buttons.addWidget(self.toolbar)
        layout_for_browser_and_buttons.addWidget(self.audio_slider)
        layout_for_browser_and_buttons.addWidget(self.browser)
        self.setLayout(layout_for_browser_and_buttons)

class Top_Right_Pane(QWidget):
    def __init__(self):
        super().__init__()


 
if __name__ == "__main__":
    from custom_text_browser import CustomTextBrowser
    import sys
    app = QApplication(sys.argv)
    window = MainUIWidget()
    window.showMaximized()
    sys.exit(app.exec())