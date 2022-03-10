
"""Purpose of this class is to bring all the diffent widgets together and provide the main window."""

from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QPushButton, QToolBar, QAction, QFrame, QHBoxLayout, QVBoxLayout, QSplitter, QTableWidget, QTableWidgetItem, QAbstractItemView, QWidget, QToolBar, QMenuBar, QSizePolicy
from PyQt5.QtCore import Qt, QSize
from text_browser.custom_text_browser import CustomTextBrowser
from web_browser.web_viewer import WebViewer
from text_browser.text_browser_with_bar import TextBrowserWithBar
from word_definer.word_definer import WordDefiner
from pathlib import Path
from database.database import DatabaseCreator
from database.user import User


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.user_id = User().get_user_id()
        db_name = "database.db"
        if not Path(db_name).is_file():
            self.create_database(name=db_name)
        self.menu_bar = QMenuBar()
        show_split_screen = QAction("Show Split Screen", self)
        show_split_screen.triggered.connect(self.show_split_screen)
        hide_split_screen = QAction("Hide Split Screen", self)
        hide_split_screen.triggered.connect(self.hide_split_screen)

        self.file_menu_bar = self.menu_bar.addMenu("File")
        self.file_menu_bar.addAction(show_split_screen)
        self.file_menu_bar.addAction(hide_split_screen)

        self.setMenuWidget(self.menu_bar)

        self.text_browser_with_bar_1 = TextBrowserWithBar()
        self.text_browser_with_bar_2 = TextBrowserWithBar()
        self.text_browser_with_bar_1.text_browser.clicked_signal.connect(lambda x: self.handle_word_clicked_signal(selection=x[0],context=x[1])) 
        self.text_browser_with_bar_2.text_browser.clicked_signal.connect(lambda x: self.handle_word_clicked_signal(selection=x[0], context=x[1]))
        self.web_viewer = WebViewer()
        self.word_editor = WordDefiner()

        self.create_dock_widgets()

        self.split = QSplitter()
        # self.split.setMinimumWidth(100)
        self.split.addWidget(self.text_browser_with_bar_1)
        self.split.addWidget(self.text_browser_with_bar_2)
        self.split.setCollapsible(self.split.indexOf(self.text_browser_with_bar_1), False)
        self.split.setCollapsible(self.split.indexOf(self.text_browser_with_bar_2), False)

        self.setCentralWidget(self.split)

    
    def create_dock_widgets(self):
        self.word_editor_dock = QDockWidget("Define & Highlight", self)
        self.word_editor_dock.setWidget(self.word_editor)
        # self.word_editor_dock.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding)
        self.addDockWidget(Qt.RightDockWidgetArea, self.word_editor_dock)

        self.web_viewer_dock = QDockWidget("Web Dictionaries", self)
        self.web_viewer_dock.setWidget(self.web_viewer)
        self.addDockWidget(Qt.RightDockWidgetArea, self.web_viewer_dock)
    
    def hide_split_screen(self):
        self.text_browser_with_bar_2.hide()
    
    def show_split_screen(self):
        self.text_browser_with_bar_2.show()

        
    def create_database(self,name):
        DatabaseCreator(name=name).create_db()
    
    def handle_word_clicked_signal(self, selection,context):
        self.web_viewer.update_selection_context(selection,context)
        self.word_editor.set_selection_text(selection)



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

