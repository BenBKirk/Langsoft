
# import sys
# from PyQt5.QtWidgets import# QSyntaxHighlighter
# from PyQt5.QtCore import #QSyntaxHighlighter
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor
from PyQt5.QtCore import QRegularExpression, QRegularExpressionMatchIterator, QRegularExpressionMatch, Qt
from database_folder.vocabulary import Vocabulary
from database_folder.highlighters import Highlighters

class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent): # the parent here is QTextDocument object
        super(SyntaxHighlighter, self).__init__(parent)
        self.vocab = ["test","ben"]
        self.test_format =  QTextCharFormat()
        self.test_format.setUnderlineColor(Qt.red)
        self.test_format.setUnderlineStyle(QTextCharFormat.SingleUnderline)
        self.test_format.setBackground(Qt.yellow)
        self.get_data_from_database()

    def get_data_from_database(self):
        vocab = Vocabulary()
        highlighter = Highlighters()
        self.highlighters_by_user_id = highlighter.fetch_all_highlighters_by_user_id()
        self.vocab_by_highlighter = {}
        for hl in self.highlighters_by_user_id:
            self.vocab_by_highlighter[hl[0]] = vocab.fetch_vocab_by_highlighter_id(hl[0])

    def highlightBlock(self,text): 
        """ we are overriding this build-in method.
            appy syntax highlighting to the given block of text """
        for highlighter in self.highlighters_by_user_id:
            the_format = self.make_format(highlighter)
            id = highlighter[0]
            try:
                the_vocab = self.vocab_by_highlighter[id]
            except KeyError:
                the_vocab = []

            for word in the_vocab:
                regex_expression = QRegularExpression(f"\\b{word}\\b",QRegularExpression.CaseInsensitiveOption)
                i = QRegularExpressionMatchIterator(regex_expression.globalMatch(text))
                while i.hasNext():
                    match = QRegularExpressionMatch(i.next())
                    old_format = self.format(match.capturedStart())
                    old_format.merge(the_format)
                    self.setFormat(match.capturedStart(),match.capturedLength(),old_format)


    def make_format(self,highlighter):
        hl_color = [float(s) for s in highlighter[2].split(",")] # converts color string to list of floats
        color = QColor()
        color.setRgbF(hl_color[0],hl_color[1],hl_color[2],hl_color[3]) # this is ugly but I will need to change the db first
        style = highlighter[3]
        the_format = QTextCharFormat()
        if style == "underline":
            the_format.setUnderlineColor(color)
            the_format.setUnderlineStyle(QTextCharFormat.SingleUnderline) 
        elif style == "background":
            the_format.setBackground(color)
        return the_format
            

        # if self.vocab != []:
        #     for dict in self.vocab:
        #         for item in dict["vocab"]:
        #             regex_string = "\\b" + str(item[2]) + "\\b"
        #             expression = QRegularExpression(regex_string,QRegularExpression.CaseInsensitiveOption)
        #             i = QRegularExpressionMatchIterator(expression.globalMatch(text))
        #             while i.hasNext():
        #                 match = QRegularExpressionMatch(i.next())
        #                 old_format = self.format(match.capturedStart())
        #                 old_format.merge(dict["fmt"])
        #                 self.setFormat(match.capturedStart(),match.capturedLength(),old_format)

    #     elif self.grammar != []:
    #         for dict in self.grammar:
    #             for item in dict["words"]:
    #                 regex_string = "\\b" + str(item) + "\\b"
    #                 expression = QRegularExpression(regex_string,QRegularExpression.CaseInsensitiveOption)
    #                 i = QRegularExpressionMatchIterator(expression.globalMatch(text))
    #                 while i.hasNext():
    #                     match = QRegularExpressionMatch(i.next())
    #                     old_format = self.format(match.capturedStart())
    #                     old_format.merge(dict["fmt"])
    #                     self.setFormat(match.capturedStart(),match.capturedLength(),old_format)




