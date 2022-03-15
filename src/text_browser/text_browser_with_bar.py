

from PyQt5.QtWidgets import QApplication, QWidget, QSplitter, QHBoxLayout, QVBoxLayout, QSlider, QSizePolicy
from PyQt5.QtCore import Qt
# from PyQt5.QtGui import 

from text_browser.custom_text_browser import CustomTextBrowser
from toolbars import FileOperationsBar, AudioPlayerBar, AudioSliderBar, CustomiseBar


class TextBrowserWithBar(QWidget):
    def __init__(self):
        super().__init__()
        self.file_opts_bar = FileOperationsBar()
        self.file_opts_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.audio_player_bar = AudioPlayerBar()
        self.audio_player_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.audio_slider = AudioSliderBar()
        self.text_browser = CustomTextBrowser()
        self.customise_bar = CustomiseBar()
        self.create_bar()
        self.combine_bar_with_text_browser()

    def create_bar(self):
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.addWidget(self.file_opts_bar)
        self.horizontal_layout.addWidget(self.audio_player_bar)
        self.horizontal_layout.addWidget(self.customise_bar)
        self.horizontal_layout.setContentsMargins(0,0,0,0)

     
    def combine_bar_with_text_browser(self):
        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addLayout(self.horizontal_layout)
        self.vertical_layout.addWidget(self.audio_slider)
        self.vertical_layout.addWidget(self.text_browser)
        self.setLayout(self.vertical_layout)
        self.vertical_layout.setContentsMargins(0,0,0,0)



