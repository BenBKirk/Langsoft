from PyQt5.QtWidgets import * #QApplication, QWidget, QFrame, QLineEdit, QHBoxLayout, QVBoxLayout, QSplitter, QTableWidget, QTableWidgetItem, QAbstractItemView, QTabWidget, QToolBar
from PyQt5 import QtGui
from PyQt5.QtCore import Qt


class FileOperationsBar(QToolBar):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Operations")
        self.create_actions()
        self.add_actions()
        
    def create_actions(self):
        self.open_file_action = QAction("Open", self)
        self.save_action = QAction("save",self)
        self.blank_file_action = QAction("blank",self)
    
    def add_actions(self):
        self.addAction(self.open_file_action)
        self.addAction(self.save_action)
        self.addAction(self.blank_file_action)
    
    def add_shortcuts(self):
        self.open_file_action.setShortcut("Ctrl+O")
        self.save_action.setShortcut("Ctrl+S")
        self.blank_file_action.setShortcut("Ctrl+N")

class AudioPlayerBar(QToolBar):
    def __init__(self):
        super().__init__()
        self.create_actions()
        self.add_actions()

    def create_actions(self):
        self.skip_back_3_action = QAction("<- 3s",self)
        self.skip_forward_3_action = QAction("3s ->",self)
        self.skip_back_10_action = QAction("<- 10s",self)
        self.skip_forward_10_action = QAction("10s ->",self)

        self.play_pause_action = QAction("Play/Pause", self)
    
    def add_actions(self):
        self.addAction(self.skip_back_10_action)
        self.addAction(self.skip_back_3_action)
        self.addAction(self.play_pause_action)
        self.addAction(self.skip_forward_3_action)
        self.addAction(self.skip_forward_10_action)
    
    def add_shortcuts(self):
        pass

class SearchBar(QToolBar):
    def __init__(self):
        super().__init__()
        self.create_actions()
        self.add_actions()

    def create_actions(self):
        self.search_field = QLineEdit()
        self.search_action = QAction("Search", self)
    
    def add_actions(self):
        self.addWidget(self.search_field)
        self.addAction(self.search_action)








    # def old_gui(self):
    #     spacer_widget = QWidget()
    #     spacer_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
    #     spacer_widget2 = QWidget()
    #     spacer_widget2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
    #     blank_file_action = QAction("blank",self)
    #     blank_file_action.setToolTip("new blank file")
    #     recent_file_action = QAction("recent_file",self)
    #     recent_file_action.setToolTip("open recent file")
    #     folder_action = QAction("open",self)
    #     folder_action.setToolTip("Open a File")
    #     folder_action.setShortcut('Ctrl+o')
    #     save_action = QAction("save",self)
    #     save_action.setToolTip("save this file")
    #     save_action.setShortcut('Ctrl+s')
    #     helpaction = QAction("help",self) 
    #     helpaction.setToolTip("How To Use This Program")
    #     self.play_action = QAction("play",self)
    #     skip_back_action = QAction("<- 3s",self)
    #     skip_forward_action = QAction("3s ->",self)
    #     skip_back_action_futher = QAction("<- 10s",self)
    #     skip_forward_action_futher = QAction("10s ->",self)
    #     settings_action = QAction("settings",self)
    #     format_action = QAction("format",self)
    #     format_action.setToolTip("Format selected text")
    #     search_action = QAction("search",self)
    #     search_action.setToolTip("Search for a word")
    #     self.vocab_grammar_toggle = QAction("toggle_v",self)
    #     self.vocab_grammar_toggle.setToolTip("Toggle between grammar and vocabulary highlights")
    #     self.searchbar_lineedit = QLineEdit()
    #     self.searchbar_lineedit.setFixedHeight(40)
    #     self.searchbar_lineedit.setFont(QtGui.QFont("Calibri",10))
    #     self.toolbar.addAction(folder_action)
    #     # self.toolbar.addWidget(QLabel(" ")) 
    #     self.toolbar.addAction(save_action)
    #     # self.toolbar.addWidget(QLabel(" ")) 
    #     self.toolbar.addAction(blank_file_action)
    #     # self.toolbar.addWidget(QLabel(" ")) 
    #     self.toolbar.addAction(recent_file_action)
    #     # self.toolbar.addWidget(QLabel(" ")) 
    #     # self.toolbar.addWidget(spacer_widget)
    #     self.toolbar.addAction(skip_back_action_futher)
    #     self.toolbar.addAction(skip_back_action)
    #     self.toolbar.addAction(self.play_action)
    #     self.toolbar.addAction(skip_forward_action)
    #     self.toolbar.addAction(skip_forward_action_futher)
    #     # self.toolbar.addWidget(spacer_widget2)
    #     # self.toolbar.addWidget(self.searchbar_lineedit)
    #     self.toolbar.addAction(search_action)
    #     # self.toolbar.addWidget(QLabel(" ")) 
    #     self.toolbar.addAction(self.vocab_grammar_toggle)
    #     # self.toolbar.addWidget(QLabel(" ")) 
    #     self.toolbar.addAction(format_action)
    #     # self.toolbar.addWidget(QLabel(" ")) 
    #     self.toolbar.addAction(helpaction)
    #     # self.toolbar.addWidget(QLabel(" ")) 
    #     self.toolbar.addAction(settings_action)
    #     self.audio_slider = QSlider()
    #     self.audio_slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    #     self.audio_slider.setOrientation(Qt.Horizontal)
    #     self.audio_slider.setFixedHeight(30)
    #     self.audio_pos_label = QLabel("0:00:00")
    #     self.audio_dur_label = QLabel("0:00:00")
    #     layout_for_audio_slider = QHBoxLayout()
    #     layout_for_audio_slider.addWidget(self.audio_pos_label)
    #     layout_for_audio_slider.addWidget(self.audio_slider)
    #     layout_for_audio_slider.addWidget(self.audio_dur_label)
    #     self.widget_for_audio_slider = QWidget()
    #     self.widget_for_audio_slider.setLayout(layout_for_audio_slider)
    #     self.widget_for_audio_slider.setFixedHeight(40)
    #     # self.browser = CustomTextBrowser()
    #     # self.browser.setFont(QtGui.QFont("Calibri",14))
    #     # self.browser.setWordWrapMode(QtGui.QTextOption.WordWrap)
    #     layout_for_browser_and_buttons = QVBoxLayout()
    #     layout_for_browser_and_buttons.addWidget(self.toolbar)
    #     layout_for_browser_and_buttons.addWidget(self.widget_for_audio_slider)
    #     # layout_for_browser_and_buttons.addWidget(self.browser)
    #     self.setLayout(layout_for_browser_and_buttons)

if __name__ == "__main__":

    """this is just test code"""
    import sys
    app = QApplication(sys.argv)
    window = QMainWindow()
    toolb = FileOperationsBar()
    window.addToolBar(toolb)
    window.addToolBar(AudioPlayerBar())
    window.addToolBar(SearchBar())

    window.show()
    sys.exit(app.exec_())