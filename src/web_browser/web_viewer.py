
from PyQt5.QtWidgets import * #QApplication, QWidget, QFrame, QLineEdit, QHBoxLayout, QVBoxLayout, QSplitter, QTableWidget, QTableWidgetItem, QAbstractItemView, QTabWidget, QToolBar
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import QUrl
from database.online_tools import OnlineTools
from database.user import User
from web_browser.custom_web_browser import CustomWebBrowser

class WebViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.user_id = User().get_user_id()
        self.selection = ""
        self.context = ""
        self.online_tools = OnlineTools() #this loads the setting from db
        self.online_tools.set_online_tools()
        self.web_engine_dict = {}
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.currentChanged.connect(self.update_active_tab)
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)
    
        self.create_tabs(self.online_tools.list_of_titles,self.online_tools.list_of_urls)


    def create_tab(self,index, name,url):
        self.web_engine_dict[index] = CustomWebBrowser()# QWebEngineView()
        # self.web_engine_dict[index].setUrl(QUrl(url))
        self.tabs.addTab(self.web_engine_dict[index],name)

    def create_tabs(self,list_of_titles,list_of_urls):
        self.tabs.clear()
        for i, title in enumerate(list_of_titles):
            self.create_tab(index=i,name=title,url=list_of_urls[i].replace("WORD","").replace("SENT","")) #replacing with empty so that the web pages start without a search term.
    
    def update_selection_context(self,selection,context):
        self.selection = selection
        self.context = context
        self.update_active_tab()
    
    def update_active_tab(self):
        index = self.tabs.currentIndex()
        url = self.tabs.currentWidget().url().toString()
        new_url = self.online_tools.list_of_urls[index].replace("WORD",self.selection).replace("SENT",self.context)
        if new_url != url: # need to update
            self.tabs.currentWidget().setUrl(QUrl(new_url))

if __name__ == "__main__":
    """This code is just to test the web viewer"""
    import sys
    app = QApplication(sys.argv)
    window = WebViewer()
    # example data
    window.update_selection_context("apple","banana")
    window.update_active_tab()

    window.show()
    sys.exit(app.exec())