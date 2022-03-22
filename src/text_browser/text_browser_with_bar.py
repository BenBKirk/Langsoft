

from PyQt5.QtWidgets import QApplication, QWidget, QSplitter, QHBoxLayout, QVBoxLayout, QSlider, QSizePolicy
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
# from PyQt5.QtGui import 

from text_browser.custom_text_browser import CustomTextBrowser
from toolbars import FileOperationsBar, AudioPlayerBar, AudioSliderBar, CustomiseBar
from file_operations.file_manager import FileManager


class TextBrowserWithBar(QWidget):
    open_files_signal = pyqtSignal(list)
    def __init__(self):
        super().__init__()
        self.file_opts_bar = FileOperationsBar()
        self.file_opts_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.audio_player_bar = AudioPlayerBar()
        self.audio_player_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.audio_slider = AudioSliderBar()
        self.audio_player = QMediaPlayer()
        self.text_browser = CustomTextBrowser()
        self.customise_bar = CustomiseBar()
        self.create_bar()
        self.combine_bar_with_text_browser()
        self.file_opts_bar.open_file_action.triggered.connect(self.handle_open_file_btn_clicked)

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
    
    def handle_open_file_btn_clicked(self):
        file_manager = FileManager()
        selected_files = file_manager.prompt_user_for_files_to_open()
        if selected_files is not None:
            self.open_files_signal.emit(selected_files)
    
    def load_text(self,text,is_html):
        self.text_browser.clear()
        if is_html:
            self.text_browser.setHtml(text)
        else:
            self.text_browser.insertPlainText(text)
        self.text_browser.moveCursor(QTextCursor.Start)
    
    def load_audio(self,audio):
        pass
    

    


        





