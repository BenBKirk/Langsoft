from PyQt5.QtWidgets import * #QApplication, QWidget, QFrame, QLineEdit, QHBoxLayout, QVBoxLayout, QSplitter, QTableWidget, QTableWidgetItem, QAbstractItemView, QTabWidget, QToolBar
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
import os
import datetime


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
        self.set_icons()
        self.playing_icon = QtGui.QIcon(os.path.join("src", "img", "playing.png"))
        self.playing_icon_dark = QtGui.QIcon(os.path.join("src", "img", "playing_dark.png"))
        self.paused_icon = QtGui.QIcon(os.path.join("src", "img", "paused.png"))
        self.paused_icon_dark = QtGui.QIcon(os.path.join("src", "img", "paused_dark.png"))

    def create_actions(self):
        self.skip_back_3_action = QAction("<- 3s",self)
        self.skip_forward_3_action = QAction("3s ->",self)
        self.skip_back_10_action = QAction("<- 10s",self)
        self.skip_forward_10_action = QAction("10s ->",self)
        self.play_pause_action = QAction("play/Pause", self)
    
    def add_actions(self):
        self.addAction(self.skip_back_10_action)
        self.addAction(self.skip_back_3_action)
        self.addAction(self.play_pause_action)
        self.addAction(self.skip_forward_3_action)
        self.addAction(self.skip_forward_10_action)
    
    def set_icons(self):
        path = os.path.join(os.getcwd(),"src", "img","play.png")
        play_icon = QtGui.QIcon(path)
        self.play_pause_action.setIcon(play_icon)
 
    def add_shortcuts(self):
       pass

class AudioSliderBar(QToolBar):
    def __init__(self):
        super().__init__()
        self.create_actions()
        self.add_actions()

    def create_actions(self):
        self.audio_slider = QSlider()
        self.audio_slider.setOrientation(Qt.Horizontal)

        self.audio_pos_label = QLabel("0:00:00")
        self.audio_dur_label = QLabel("0:00:00")
    
    def add_actions(self):
        self.addWidget(self.audio_pos_label)
        self.addWidget(self.audio_slider)
        self.addWidget(self.audio_dur_label)
    
    def set_duration(self, dur):
        self.audio_slider.setRange(0, dur)
        self.audio_dur_label.setText(str(datetime.timedelta(seconds=dur/1000))[:7])
    
    def set_position(self, pos):
        self.audio_slider.blockSignals(True) # block signals to avoid signal loop
        self.audio_slider.setValue(pos)
        self.audio_slider.blockSignals(False)
        self.audio_pos_label.setText(str(datetime.timedelta(seconds=pos/1000))[:7])
    

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

class CustomiseBar(QToolBar):
    def __init__(self):
        super().__init__()
        self.create_actions()
        self.add_actions()

    def create_actions(self):
        self.toggle_grammar_vocab = QAction("Toggle Grammar/Vocab", self)
        self.help = QAction("Help", self)
        self.settings = QAction("Settings", self)
    
    def add_actions(self):
        self.addAction(self.toggle_grammar_vocab)
        self.addAction(self.help)
        self.addAction(self.settings)




if __name__ == "__main__":

    """this is just test code"""
    import sys
    app = QApplication(sys.argv)
    window = QMainWindow()
    toolb = FileOperationsBar()
    window.addToolBar(toolb)
    window.addToolBar(AudioPlayerBar())
    window.addToolBar(SearchBar())
    window.addToolBar(CustomiseBar())

    window.show()
    sys.exit(app.exec_())