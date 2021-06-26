import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class UsersPage(QWidget):
    def __init__(self):
        super(UsersPage, self).__init__()
        self.resize(400,400)
        self.setWindowTitle("Users")
        self.setWindowIcon(QIcon(os.path.join("App", "img", "user.png")))
        self.dropdown_menu = QComboBox()
        self.dropdown_menu.addItems(["bob","fred","jim"])
        self.new_user_btn = QPushButton("Add New User")
        
        layout = QGridLayout()
        layout.addWidget(QLabel("Users:"),0,0)
        layout.addWidget(self.dropdown_menu,0,1)
        layout.addWidget(self.new_user_btn,0,2)
        self.setLayout(layout)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UsersPage()
    window.show()
    sys.exit(app.exec())