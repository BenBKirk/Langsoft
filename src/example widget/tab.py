import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class TabBarPlus(QTabBar):
    """Tab bar that has a plus button floating to the right of the tabs."""

    plusClicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Plus Button
        self.plusButton = QPushButton("+")
        self.plusButton.setParent(self)
        self.plusButton.setFixedSize(20, 20)  # Small Fixed size
        self.plusButton.clicked.connect(self.plusClicked.emit)
        self.movePlusButton() # Move to the correct location
    # end Constructor

    def sizeHint(self):
        """Return the size of the TabBar with increased width for the plus button."""
        sizeHint = QTabBar.sizeHint(self) 
        width = sizeHint.width()
        height = sizeHint.height()
        return QSize(width+25, height)
    # end tabSizeHint

    def resizeEvent(self, event):
        """Resize the widget and make sure the plus button is in the correct location."""
        super().resizeEvent(event)

        self.movePlusButton()
    # end resizeEvent

    def tabLayoutChange(self):
        """This virtual handler is called whenever the tab layout changes.
        If anything changes make sure the plus button is in the correct location.
        """
        super().tabLayoutChange()

        self.movePlusButton()
    # end tabLayoutChange

    def movePlusButton(self):
        """Move the plus button to the correct location."""
        # Find the width of all of the tabs
        size = sum([self.tabRect(i).width() for i in range(self.count())])
        # size = 0
        # for i in range(self.count()):
        #     size += self.tabRect(i).width()

        # Set the plus button location in a visible area
        h = self.geometry().top()
        w = self.width()
        if size > w: # Show just to the left of the scroll buttons
            self.plusButton.move(w-54, h)
        else:
            self.plusButton.move(size, h)
    # end movePlusButton
# end class MyClass


class Tabs(QTabWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setAcceptDrops(True)
        # self.tabBar = self.tabBar()
        self.tabBar = TabBarPlus()
        self.setTabBar(self.tabBar)
        self.tabBar.setMouseTracking(True)
        

        self.indexTab = None
        self.setMovable(True)
        self.setTabsClosable(True)
        # btn = QToolButton(self)
        # btn.setText("+")
        # self.addTab(QLabel("this is a test"),"")
        # self.setTabEnabled(0,False)
        # self.tabBar.setTabButton(0, QTabBar.RightSide, btn)

        self.addTab(QWidget(self), 'Tab One')
        self.addTab(QWidget(self), 'Tab Two')
        self.tabCloseRequested.connect(self.removeTab)
    

    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton:
            return

        globalPos = self.mapToGlobal(e.pos())
        tabBar = self.tabBar
        posInTab = tabBar.mapFromGlobal(globalPos)
        self.indexTab = tabBar.tabAt(e.pos())
        tabRect = tabBar.tabRect(self.indexTab)

        pixmap = QPixmap(tabRect.size())
        tabBar.render(pixmap,QPoint(),QRegion(tabRect))
        mimeData = QMimeData()
        drag = QDrag(tabBar)
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap)
        cursor = QCursor(Qt.OpenHandCursor)
        drag.setHotSpot(e.pos() - posInTab)
        drag.setDragCursor(cursor.pixmap(),Qt.MoveAction)
        dropAction = drag.exec_(Qt.MoveAction)


    def dragEnterEvent(self, e):
        e.accept()
        if e.source().parentWidget() != self:
            return

        print(self.indexOf(self.widget(self.indexTab)))
        self.parent.TABINDEX = self.indexOf(self.widget(self.indexTab))


    def dragLeaveEvent(self,e):
        e.accept()


    def dropEvent(self, e):
        print(self.parent.TABINDEX)
        if e.source().parentWidget() == self:
            return

        e.setDropAction(Qt.MoveAction)
        e.accept()
        counter = self.count()

        if counter == 0:
            self.addTab(e.source().parentWidget().widget(self.parent.TABINDEX),e.source().tabText(self.parent.TABINDEX))
        else:
            self.insertTab(counter + 1 ,e.source().parentWidget().widget(self.parent.TABINDEX),e.source().tabText(self.parent.TABINDEX))


class Window(QWidget):
    def __init__(self):

        super().__init__()

        self.TABINDEX = 0
        tabWidgetOne = Tabs(self)
        tabWidgetTwo = Tabs(self)



        layout = QHBoxLayout()

        self.moveWidget = None

        layout.addWidget(tabWidgetOne)
        layout.addWidget(tabWidgetTwo)

        self.setLayout(layout)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())