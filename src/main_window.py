
"""Purpose of this class is to bring all the diffent widgets together and provide the main window."""

from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QPushButton, QToolBar, QAction, QFrame, QHBoxLayout, QVBoxLayout, QSplitter, QTableWidget, QTableWidgetItem, QAbstractItemView, QWidget, QToolBar, QMenuBar, QSizePolicy 
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from text_browser.custom_text_browser import CustomTextBrowser
from web_browser.web_viewer import WebViewer
from text_browser.text_browser_with_bar import TextBrowserWithBar
from text_browser.text_browser_tab import TextBrowserTab
from word_definer.word_definer import WordDefiner
from pathlib import Path
from database_folder.database import DatabaseCreator
from database_folder.user import User


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.user_id = User().get_user_id()
        db_name = "database.db"
        if not Path(db_name).is_file():
            DatabaseCreator(name=db_name).create_db()
        self.web_viewer = WebViewer()
        self.word_definer = WordDefiner()
        self.tab = TextBrowserTab()
        self.split_middle = QSplitter(Qt.Horizontal)
        self.split_right_side = QSplitter(Qt.Vertical)
        self.split_right_side.addWidget(self.word_definer)
        self.split_right_side.addWidget(self.web_viewer)
        self.split_middle.addWidget(self.tab)
        self.split_middle.addWidget(self.split_right_side)
        self.split_middle.setSizes([1000,500])
        self.setCentralWidget(self.split_middle)
        self.tab.forward_signal_from_text_browser.connect(lambda x: self.handle_word_clicked_signal(x[0],x[1]))
        self.word_definer.word_saved_signal.connect(self.update_syntax_highlighting)

     
    def handle_word_clicked_signal(self, selection,context):
        self.web_viewer.update_selection_context(selection,context)
        self.word_definer.look_up_word(selection)

    def update_syntax_highlighting(self):
        for i in range(self.tab.count()):
            self.tab.widget(i).text_browser.syntax_highlighter.get_data_from_database()
            self.tab.widget(i).text_browser.syntax_highlighter.rehighlight()



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    window = MainWindow()
    window.setWindowTitle("Langsoft")
    window.setWindowIcon(QIcon("./Langsoft.ico"))
    window.show()
    sys.exit(app.exec())

