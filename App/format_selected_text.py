
import sys
from PyQt5.QtWidgets import * 
from PyQt5 import QtGui
from PyQt5 import QtCore

class FormatSelectedText(QWidget):
    def __init__(self):
        super(FormatSelectedText, self).__init__()
        self.resize(400,150)
        self.setWindowTitle("Format Selected Text")
        self.setWindowIcon(QtGui.QIcon("App\\img\\format.png"))
        self.font_options = QComboBox()
        self.font_options.addItems(["Arial","Times New Roman","Comic Sans","Calibri","Ubuntu"])
        self.font_size_box = QSpinBox()
        self.font_size_box.setValue(14)
        self.font_size_box.setFixedWidth(50)
        self.clear_formating_btn = QPushButton("Clear Formating")
        self.clear_highlighting_btn = QPushButton("Clear Hightlighting")

        layout = QGridLayout()
        layout.addWidget(self.clear_formating_btn,0,0)
        layout.addWidget(self.clear_highlighting_btn,0,1)
        layout.addWidget(self.font_options,1,0)
        # layout.addWidget(self.font_size_box,1,1)
        self.setLayout(layout)
    
    def change_font_ftn(self):
        if self.browser.textCursor().hasSelection():
            cursor = self.browser.textCursor()
            selection = cursor.selectedText()
            print(selection)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FormatSelectedText()
    window.show()
    sys.exit(app.exec())