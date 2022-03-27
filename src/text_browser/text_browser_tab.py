
from PyQt5.QtWidgets import QTabWidget, QApplication, QWidget, QMessageBox, QPushButton, QLabel
from PyQt5.QtCore import Qt, pyqtSignal

from file_operations.file_manager import FileManager
from .text_browser_with_bar import TextBrowserWithBar


class TextBrowserTab(QTabWidget):
    forward_click_signal_from_text_browser = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setMovable(True)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.do_you_really_want_to_close)
        self.add_new_tab_btn = QPushButton("+")
        self.setCornerWidget(self.add_new_tab_btn, Qt.TopLeftCorner)
        self.add_new_tab_btn.setMinimumSize(self.add_new_tab_btn.sizeHint())
        self.add_new_tab_btn.clicked.connect(lambda :self.add_new_tab())
        self.add_new_tab()
        self.tabBar().setContentsMargins(0,0,0,0)
    
    def do_you_really_want_to_close(self,index):
        # msg_box = QMessageBox()
        # msg_box.setIcon(QMessageBox.Question)
        # msg_box.setText("Do you really want to close this tab?")
        # msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        # if msg_box.exec() == QMessageBox.Yes:
        #     self.removeTab(index)
        self.removeTab(index)
    
    def add_new_tab(self,name=None):
        new_tab = TextBrowserWithBar()
        new_tab.text_browser.clicked_signal.connect(lambda x: self.forward_click_signal_from_text_browser.emit(x))
        new_tab.open_files_signal.connect(self.open_files_in_tabs)
        if name is not None:
            name = name
        else:
            name = f"Tab {self.count()+1}"
        self.addTab(new_tab,name)
        return new_tab # in case we need to keep reference to it
  
    def open_files_in_tabs(self, files):
        """
        The first file will be opened in the current tab
        and any other tabs will be opened in a new tab.
        """
        if len(files) == 0:
            return
        file_manager = FileManager()
        first_file = files[0]
        current_tab = self.currentWidget()
        current_tab_index = self.currentIndex()
        self.setTabText(current_tab_index, file_manager.get_file_name_from_path(first_file[0]))
        text, is_html = file_manager.read_text_file(first_file[0])
        current_tab.load_text(text, is_html)
        if first_file[1] is not None:
            current_tab.load_audio(first_file[1])

        if len(files) == 1:
            return
        for file in files[1:]:# slice to slip the first file
            name = file_manager.get_file_name_from_path(file[0])
            new_tab = self.add_new_tab(name)
            text, is_html = file_manager.read_text_file(file[0])
            new_tab.load_text(text, is_html)
            if file[1] is not None:
                new_tab.load_audio(file[1])

if __name__ == "__main__":
    """this is just test code"""
    import sys
    app = QApplication(sys.argv)
    window = TextBrowserTab()
    window.show()
    sys.exit(app.exec())

