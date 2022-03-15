
from PyQt5.QtWidgets import QApplication, QWidget, QSplitter, QHBoxLayout, QVBoxLayout# QFrame, QLineEdit, , , QTableWidget, QTableWidgetItem, QAbstractItemView, QTabWidget, QToolBar
from text_browser.custom_text_browser import CustomTextBrowser
from toolbars import FileOperationsBar, AudioPlayerBar


class TextBrowserWithBar(QWidget):
    def __init__(self):
        super().__init__()
        self.file_opts_bar = FileOperationsBar()
        self.audio_player_bar = AudioPlayerBar()
        self.text_browser = CustomTextBrowser()
        self.create_bar()
        self.combine_bar_with_text_browser()

    def create_bar(self):
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.addWidget(self.file_opts_bar)
        self.horizontal_layout.addWidget(self.audio_player_bar)
        self.horizontal_layout.setContentsMargins(0,0,0,0)
    
    def combine_bar_with_text_browser(self):
        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addLayout(self.horizontal_layout)
        self.vertical_layout.addWidget(self.text_browser)
        self.setLayout(self.vertical_layout)
        self.vertical_layout.setContentsMargins(0,0,0,0)



