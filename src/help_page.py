
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5 import QtCore
import os



class HelpWindow(QWidget):
    def __init__(self):
        super(HelpWindow, self).__init__()
        self.resize(800,800)
        self.setWindowTitle("Help")
        self.setWindowIcon(QtGui.QIcon(os.path.join("src", "img", "help.png")))
        self.help_browser = QTextBrowser()
        # self.help_browser.loadResource(.HtmlResource, QUrl(os.path.join(os.getcwd(),"src","Help File.html")))
        # import html file and put it in text browser
        with open(os.path.join(os.getcwd(),"src","help.html"),"r", encoding='utf8', errors='ignore') as f:
            html = f.read()
            self.help_browser.setHtml(html)

        layout = QVBoxLayout()
        layout.addWidget(self.help_browser)
        self.setLayout(layout)








if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HelpWindow()
    window.show()
    sys.exit(app.exec())