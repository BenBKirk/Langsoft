
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPlainTextEdit, QVBoxLayout
from PyQt5.QtCore import *#QRegExp, QRegularExpression, QRegularExpressionMatch, QRegularExpressionMatchIterator, QRegularExpressionMatch
from PyQt5.QtGui import *#QColor, QRegExpValidator, QSyntaxHighlighter, QTextCharFormat

class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)
        self.vocab = []
        self.grammar = []

    def set_state(self, vocab, grammar):
        self.vocab = vocab
        self.grammar = grammar


    def highlightBlock(self,text):
        # sorry this is very messy :(
        if self.vocab != []:
            for dict in self.vocab:
                for item in dict["vocab"]:
                    regex_string = "\\b" + str(item[2]) + "\\b"
                    expression = QRegularExpression(regex_string,QRegularExpression.CaseInsensitiveOption)
                    i = QRegularExpressionMatchIterator(expression.globalMatch(text))
                    while i.hasNext():
                        match = QRegularExpressionMatch(i.next())
                        old_format = self.format(match.capturedStart())
                        old_format.merge(dict["fmt"])
                        self.setFormat(match.capturedStart(),match.capturedLength(),old_format)
        elif self.grammar != []:
            for dict in self.grammar:
                for item in dict["words"]:
                    regex_string = "\\b" + str(item) + "\\b"
                    expression = QRegularExpression(regex_string,QRegularExpression.CaseInsensitiveOption)
                    i = QRegularExpressionMatchIterator(expression.globalMatch(text))
                    while i.hasNext():
                        match = QRegularExpressionMatch(i.next())
                        old_format = self.format(match.capturedStart())
                        old_format.merge(dict["fmt"])
                        self.setFormat(match.capturedStart(),match.capturedLength(),old_format)




