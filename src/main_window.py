
"""Purpose of this class is to bring all the diffent widgets together and provide the main window."""

from PyQt5.QtWidgets import QApplication, QMainWindow, QSplitter, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QPoint
from web_browser.web_viewer import WebViewer
from text_browser.text_browser_tab import TextBrowserTab
from word_definer.word_definer import WordDefiner
from pathlib import Path
from database_folder.database import DatabaseCreator
from database_folder.user import User
from word_definer.definition_finder import DefinitionFinder
from palette import DarkPalette


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
        # self.split_right_side.addWidget(self.word_definer)
        self.split_right_side.addWidget(self.web_viewer)
        self.split_right_side.setSizes([100,500])
        self.split_middle.addWidget(self.tab)
        self.split_middle.addWidget(self.split_right_side)
        self.split_middle.setSizes([1000,500])
        self.setCentralWidget(self.split_middle)
        self.tab.forward_click_signal_from_text_browser.connect(lambda x: self.handle_word_clicked_signal(x[0],x[1],x[2]))
        self.word_definer.word_saved_signal.connect(self.update_syntax_highlighting)
    
    def enable_dark_theme(self):
        self.dark_palette = DarkPalette()
        self.setPalette(self.dark_palette)
     
    def handle_word_clicked_signal(self, selection,context,pos):
        width = self.word_definer.width()
        height = self.word_definer.height()
        self.word_definer.move(pos.x()-width/2,pos.y()-height/2 -100)
        self.word_definer.show()
        self.word_definer.activateWindow()
        #raise the window to front
        self.word_definer.raise_()
        self.web_viewer.update_selection_context(selection,context)
        self.definition_finder = DefinitionFinder()
        self.definition_finder.lookup(selection)
        self.word_definer.look_up_word(selection) # TODO: use the definition_finder instead
 
    def update_syntax_highlighting(self):
        """forces the syntax_highlighter to load data again. called when a word is saved"""
        self.word_definer.hide()
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

