
from PyQt5.QtWidgets import QTabWidget, QApplication, QWidget, QMessageBox, QPushButton, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from .text_browser_with_bar import TextBrowserWithBar


class TextBrowserTab(QTabWidget):
    forward_signal_from_text_browser = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setMovable(True)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.do_you_really_want_to_close)
        self.add_new_tab_btn = QPushButton("+")
        self.setCornerWidget(self.add_new_tab_btn, Qt.TopLeftCorner)
        self.add_new_tab_btn.setMinimumSize(self.add_new_tab_btn.sizeHint())
        self.add_new_tab_btn.clicked.connect(self.add_new_tab)
        self.add_new_tab()
        self.tabBar().setContentsMargins(0,0,0,0)
    
    def do_you_really_want_to_close(self,index):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setText("Do you really want to close this tab?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        if msg_box.exec() == QMessageBox.Yes:
            self.removeTab(index)
    
    def add_new_tab(self):
        new_tab = TextBrowserWithBar()
        new_tab.text_browser.clicked_signal.connect(lambda x: self.forward_signal_from_text_browser.emit(x))
        self.addTab(new_tab,f"Tab {self.count()+1}")

    
    def rename_tab(self, index, name):
        self.setTabText(index, name)
    
    # def get_current_tab_text(self):
    #     return self.widget(self.currentIndex()).text_browser.toPlainText()

if __name__ == "__main__":
    """this is just test code"""
    import sys
    app = QApplication(sys.argv)
    window = TextBrowserTab()
    window.show()
    sys.exit(app.exec())

