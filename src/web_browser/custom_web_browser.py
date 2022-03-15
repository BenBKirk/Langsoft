from PyQt5.QtWidgets import QMainWindow, QApplication, QAction
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QProcessEnvironment, QProcess, Qt
from PyQt5.QtGui import QTextCursor, QPalette, QPaintEvent
import os
from palette import DarkPalette


class CustomWebBrowser(QWebEngineView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def contextMenuEvent(self, event):
        self.menu = self.page().createStandardContextMenu()
        copy_word_to_def = QAction("Copy Word to Definition", self)
        if self.hasSelection():
            self.menu.addAction(copy_word_to_def)
        # self.menu.popup(event.globalPos())
        action = self.menu.exec(event.globalPos())
        if action == copy_word_to_def:
            print(self.selectedText())
            # TODO add a signal here

class MainWindow(QMainWindow): 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs) 

        self.browser = CustomWebBrowser()
        self.setCentralWidget(self.browser)
    
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.browser.setUrl(QUrl("http://www.google.com"))
    window.show()
    sys.exit(app.exec_())
