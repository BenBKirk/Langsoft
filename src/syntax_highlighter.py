
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPlainTextEdit, QVBoxLayout
from PyQt5.QtCore import *#QRegExp, QRegularExpression, QRegularExpressionMatch, QRegularExpressionMatchIterator, QRegularExpressionMatch
from PyQt5.QtGui import *#QColor, QRegExpValidator, QSyntaxHighlighter, QTextCharFormat

class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)
        self.state = []

    def set_state(self, dict):
        self.state = dict

    def highlightBlock(self,text):
        if self.state != []:
            for dict in self.state:
                for item in dict["vocab"]:
                    regex_string = "\\b" + str(item[2]) + "\\b"
                    expression = QRegularExpression(regex_string,QRegularExpression.CaseInsensitiveOption)
                    i = QRegularExpressionMatchIterator(expression.globalMatch(text))
                    while i.hasNext():
                        match = QRegularExpressionMatch(i.next())
                        self.setFormat(match.capturedStart(),match.capturedLength(),dict["fmt"])
