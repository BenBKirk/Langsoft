
"""Purpose of this class is to bring all the diffent widgets together and provide the main window."""

from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QPushButton, QToolBar, QAction, QFrame, QHBoxLayout, QVBoxLayout, QSplitter, QTableWidget, QTableWidgetItem, QAbstractItemView, QWidget, QToolBar, QMenuBar 
from PyQt5.QtCore import Qt
from custom_text_browser import CustomTextBrowser
from web_viewer import WebViewer
from text_browser_with_bar import TextBrowserWithBar
from word_editor import WordEditor



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.menu_bar = QMenuBar()
        show_split_screen = QAction("Show Split Screen", self)
        show_split_screen.triggered.connect(self.show_split_screen)
        hide_split_screen = QAction("Hide Split Screen", self)
        hide_split_screen.triggered.connect(self.hide_split_screen)

        # self.menu.addAction("Hide Split Screen", self.hide_split_screen)
        # self.menu.addAction("Show Split Screen", self.show_split_screen)
        self.file_menu_bar = self.menu_bar.addMenu("File")
        self.file_menu_bar.addAction(show_split_screen)
        self.file_menu_bar.addAction(hide_split_screen)

        self.setMenuWidget(self.menu_bar)

        self.text_browser_with_bar_1 = TextBrowserWithBar()
        self.text_browser_with_bar_2 = TextBrowserWithBar()
        self.text_browser_with_bar_1.text_browser.clicked_signal.connect(lambda x: self.web_viewer.update_url_for_search(x[0], x[1]))
        self.web_viewer = WebViewer()
        #load dummy data
        self.web_viewer.create_tabs([["Google","Google","https://www.google.com/search?q=WORD"],["Wikipedia","Wikipedia","https://en.wikipedia.org/wiki/WORD"],["YouTube","YouTube","https://www.youtube.com/results?search_query=WORD"]])
        self.word_editor = WordEditor()

        self.create_dock_widgets()

        self.split = QSplitter()
        # self.split.setMinimumWidth(100)
        self.split.addWidget(self.text_browser_with_bar_1)
        self.split.addWidget(self.text_browser_with_bar_2)
        self.split.setCollapsible(self.split.indexOf(self.text_browser_with_bar_1), False)
        self.split.setCollapsible(self.split.indexOf(self.text_browser_with_bar_2), False)

        self.setCentralWidget(self.split)

    
    def create_dock_widgets(self):
        self.word_editor_dock = QDockWidget("Definition Editor", self)
        self.word_editor_dock.setWidget(self.word_editor)
        self.addDockWidget(Qt.RightDockWidgetArea, self.word_editor_dock)

        self.web_viewer_dock = QDockWidget("Web Dictionaries", self)
        self.web_viewer_dock.setWidget(self.web_viewer)
        self.addDockWidget(Qt.RightDockWidgetArea, self.web_viewer_dock)
    
    def hide_split_screen(self):
        self.text_browser_with_bar_2.hide()
    
    def show_split_screen(self):
        self.text_browser_with_bar_2.show()




    







    


        

    






if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

