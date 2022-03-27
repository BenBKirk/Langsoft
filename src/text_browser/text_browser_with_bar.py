

from PyQt5.QtWidgets import QApplication, QWidget, QSplitter, QHBoxLayout, QVBoxLayout, QSlider, QSizePolicy
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import Qt, pyqtSignal, QUrl
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
        self.audio_slider_bar = AudioSliderBar()
        self.audio_player = QMediaPlayer()
        self.text_browser = CustomTextBrowser()
        self.customise_bar = CustomiseBar()
        self.create_bar()
        self.combine_bar_with_text_browser()
        self.file_opts_bar.open_file_action.triggered.connect(self.handle_open_file_btn_clicked)
        self.audio_player_bar.play_pause_action.triggered.connect(self.toggle_play_pause)
        self.audio_player_bar.skip_forward_3_action.triggered.connect(lambda: self.skip_audio_forward(3))
        self.audio_player_bar.skip_forward_10_action.triggered.connect(lambda: self.skip_audio_forward(10))
        self.audio_player_bar.skip_back_3_action.triggered.connect(lambda: self.skip_audio_back(3))
        self.audio_player_bar.skip_back_10_action.triggered.connect(lambda: self.skip_audio_back(10))
        self.audio_player.positionChanged.connect(self.audio_slider_bar.set_position)
        self.audio_player.durationChanged.connect(self.audio_slider_bar.set_duration)
        self.audio_slider_bar.audio_slider.valueChanged.connect(self.audio_player.setPosition)

    def create_bar(self):
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.addWidget(self.file_opts_bar)
        self.horizontal_layout.addWidget(self.audio_player_bar)
        self.horizontal_layout.addWidget(self.customise_bar)
        self.horizontal_layout.setContentsMargins(0,0,0,0)

     
    def combine_bar_with_text_browser(self):
        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addLayout(self.horizontal_layout)
        self.vertical_layout.addWidget(self.audio_slider_bar)
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
        print(f"loading audio {audio}")
        self.audio_player.setMedia(QMediaContent(QUrl.fromLocalFile(audio)))
        self.update_audio_player_icon()
        self.audio_player_bar.show()
        self.audio_slider_bar.show()
    
    def toggle_play_pause(self):
        if self.audio_player.state() == QMediaPlayer.PlayingState:
            self.audio_player.pause()
            self.update_audio_player_icon()
            # self.audio_player_bar.play_pause_action.setIcon(self.audio_player_bar.play_icon)
        elif self.audio_player.state() == QMediaPlayer.PausedState or self.audio_player.state() == QMediaPlayer.StoppedState:
            self.audio_player.play()
            self.update_audio_player_icon()
            # self.audio_player_bar.play_pause_action.setIcon(self.audio_player_bar.pause_icon)

    def update_audio_player_icon(self):
        state = self.audio_player.state()
        dark_theme = True # TODO get this from settings
        if state == QMediaPlayer.PausedState or state == QMediaPlayer.StoppedState:
            if dark_theme:
                icon = self.audio_player_bar.paused_icon_dark
            else:
                icon = self.audio_player_bar.paused_icon
        elif state == QMediaPlayer.PlayingState:
            if dark_theme:
                icon = self.audio_player_bar.playing_icon_dark
            else:
                icon = self.audio_player_bar.playing_icon
        self.audio_player_bar.play_pause_action.setIcon(icon)
    
    def skip_audio_forward(self,seconds):
        self.audio_player.setPosition(self.audio_player.position() + seconds * 1000)

    def skip_audio_back(self,seconds):
        self.audio_player.setPosition(self.audio_player.position() - seconds * 1000)



    


        





