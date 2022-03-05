
from PyQt5.QtWidgets import * #QApplication, QWidget, QFrame, QLineEdit, QHBoxLayout, QVBoxLayout, QSplitter, QTableWidget, QTableWidgetItem, QAbstractItemView, QTabWidget, QToolBar
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import QUrl

class WebViewer(QWidget):
    def __init__(self,url_list):
        super().__init__()
        self.selection = ""
        self.context = ""
        self.url_list = url_list
        self.tabs_dict = {}
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def create_tab(self,index, name,url):
        """
        creates web engine and appends it to my_tabs dict 
        """
        self.tabs_dict[index] = QWebEngineView() 
        self.tabs_dict[index].setUrl(QUrl(url))
        self.tabs.addTab(self.tabs_dict[index],name)

    def create_tabs(self,online_tools):
        self.tabs.clear()
        for i, row in enumerate(online_tools): 
            self.create_tab(i,row[1],row[2].replace("WORD","").replace("SENT","")) #replacing with empty so that the web pages start with a search term.
    
    def update_url_for_search(self,selection,context):
        self.selection = selection
        self.context = context
        #depending of which tab is selected, look up the word in that tab
        index = self.tabs.currentIndex()

        self.tabs.currentWidget().setUrl(QUrl(f"https://www.google.com/search?q={selection}"))

if __name__ == "__main__":
    """This code is just to test the web viewer"""

    import sys
    app = QApplication(sys.argv)
    window = WebViewer()
    # example data
    window.create_tabs([["Google","Google","https://www.google.com/search?q=WORD"],["Wikipedia","Wikipedia","https://en.wikipedia.org/wiki/WORD"],["YouTube","YouTube","https://www.youtube.com/results?search_query=WORD"]])

    window.show()
    sys.exit(app.exec())