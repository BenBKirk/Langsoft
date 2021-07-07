
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPlainTextEdit, QVBoxLayout
from PyQt5.QtCore import *#QRegExp, QRegularExpression, QRegularExpressionMatch, QRegularExpressionMatchIterator, QRegularExpressionMatch
from PyQt5.QtGui import *#QColor, QRegExpValidator, QSyntaxHighlighter, QTextCharFormat

class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)
        self.state = {"vocab":[(0,0,"ini")],"fmt":QTextCharFormat()}


    def set_dict(self, dict):
        self.state = dict


    def highlightBlock(self,text):
        # fmt = QTextCharFormat()
        # fmt.setUnderlineColor(Qt.red)
        # fmt.setUnderlineStyle(QTextCharFormat.SingleUnderline)


        print("running")

        for item in self.state["vocab"]:
            regex_string = "\\b" + str(item[2]) + "\\b"
            expression = QRegularExpression(regex_string,QRegularExpression.CaseInsensitiveOption)
            i = QRegularExpressionMatchIterator(expression.globalMatch(text))
            while i.hasNext():
                match = QRegularExpressionMatch(i.next())
                QSyntaxHighlighter.setFormat(self,match.capturedStart(),match.capturedLength(),self.state["fmt"])






        # new_list = []
        # for item in self.list:
        #     new_list.append("\\b" + item + "\\b")
        # regex_string = "|".join(new_list)

        # expression = QRegularExpression(regex_string)
        # i = QRegularExpressionMatchIterator(expression.globalMatch(text))
        # while i.hasNext():
        #     match = QRegularExpressionMatch(i.next())
        #     QSyntaxHighlighter.setFormat(self,match.capturedStart(),match.capturedLength(),fmt)













    #     self._highlight_lines = {}

    # def highlight_line(self, line_num, fmt):
    #     if isinstance(line_num, int) and line_num >= 0 and isinstance(fmt, QTextCharFormat):
    #         self._highlight_lines[line_num] = fmt
    #         block = self.document().findBlockByLineNumber(line_num)
    #         self.rehighlightBlock(block)

    # def clear_highlight(self):
    #     self._highlight_lines = {}
    #     self.rehighlight()

    # def highlightBlock(self, text):
    #     blockNumber = self.currentBlock().blockNumber()
    #     fmt = self._highlight_lines.get(blockNumber)
    #     if fmt is not None:
    #         self.setFormat(0, len(text), fmt)

# class AppDemo(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.resize(1200, 800)

#         mainLayout = QVBoxLayout()

#         validator = QRegExpValidator(QRegExp(r'[0-9 ]+'))

#         self.lineEdit = QLineEdit()
#         self.lineEdit.setStyleSheet('font-size: 30px; height: 50px;')
#         self.lineEdit.setValidator(validator)
#         self.lineEdit.textChanged.connect(self.onTextChanged)
#         mainLayout.addWidget(self.lineEdit)

#         self.textEditor = QPlainTextEdit()
#         self.textEditor.setStyleSheet('font-size: 30px; color: green')
#         mainLayout.addWidget(self.textEditor)

#         for i in range(1, 21):
#             self.textEditor.appendPlainText('Line {0}'.format(i))

#         self.highlighter = SyntaxHighlighter(self.textEditor.document())
#         self.setLayout(mainLayout)

#     def onTextChanged(self, text):
#         fmt = QTextCharFormat()
#         fmt.setBackground(QColor('yellow'))

#         self.highlighter.clear_highlight()

#         try:
#             lineNumber = int(text) - 1
#             self.highlighter.highlight_line(lineNumber, fmt)
#         except ValueError:
#             pass

# app = QApplication(sys.argv)        
# demo = AppDemo()
# demo.show()
# sys.exit(app.exec_())