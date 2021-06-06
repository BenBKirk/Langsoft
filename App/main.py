"""
This is the main logic of the APP
"""
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QInputDialog, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtGui import QTextCursor, QTextDocument, QIcon, QTextCharFormat
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from UI.main_UI import *
from bs4 import BeautifulSoup
import os
import fitz
import json
import re
import uuid
from gen_anki_deck import AnkiDeckGenerator
from settings_page import SettingsPage
from format_selected_text import FormatSelectedText
import mammoth
from html2docx import html2docx
from API.google_trans_API import GoogleTranslate
from flashcard_list_manager import FlashcardManager
from help_page import HelpWindow
import datetime


class MainWindow(MainUIWidget):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.json_settings = {}
        self.set_global_settings()
        self.start_tabs() # this being called after the settings, allows time to read the json settings file
        # Create classes instances:
        self.audio_player = QMediaPlayer()
        self.anki_gen = AnkiDeckGenerator()
        self.settings = SettingsPage()
        self.translator = GoogleTranslate()
        self.flashcards_list = FlashcardManager()
        self.format_widget = FormatSelectedText()
        self.help_page = HelpWindow()
        #connections
        self.browser.clicked.connect(self.browser_clicked)
        self.browser.hightlight.connect(self.highlight)
        self.browser.clear_highlighting.connect(self.clear_highlighting)
        self.toolbar.actionTriggered[QAction].connect(self.handle_toolbar_click)
        self.toolbar2.actionTriggered[QAction].connect(self.handle_toolbar_click)
        # self.font_size_box.valueChanged.connect(self.change_font_size)
        self.make_flash_btn.clicked.connect(self.add_flashcard)
        self.audio_player.durationChanged.connect(self.update_slider_duration)
        self.audio_player.positionChanged.connect(self.update_slider_position)
        self.audio_slider.valueChanged.connect(self.audio_player.setPosition)
        self.settings.save_button.clicked.connect(self.save_settings_to_json)
        self.settings.dark_theme_checkbox.stateChanged.connect(self.toggle_theme)
        self.format_widget.font_options.currentTextChanged.connect(self.change_font_type)
        # self.format_widget.font_size_box.valueChanged.connect(self.change_font_size)
        self.format_widget.clear_formating_btn.clicked.connect(self.clear_formating)
        self.format_widget.clear_highlighting_btn.clicked.connect(self.clear_highlighting)
        # other
        self.dark_theme_palette = self.setup_dark_theme()
        self.check_ui_settings()
        # keyboard shortcuts
        self.lookup_shortcut = QShortcut(QtGui.QKeySequence("Ctrl+Up"),self)
        self.lookup_shortcut.activated.connect(self.browser_clicked)
        self.make_flashcard_shortcut = QShortcut(QtGui.QKeySequence("Ctrl+Down"),self)
        self.make_flashcard_shortcut.activated.connect(self.add_flashcard)
        self.toggle_audio_shortcut = QShortcut(QtGui.QKeySequence("Alt+Up"),self)
        self.toggle_audio_shortcut.activated.connect(self.toggle_play_audio)
        self.skip_back_shortcut = QShortcut(QtGui.QKeySequence("Alt+Left"),self)
        self.skip_back_shortcut.activated.connect(self.skip_back)
        self.skip_forward_shortcut = QShortcut(QtGui.QKeySequence("Alt+Right"),self)
        self.skip_forward_shortcut.activated.connect(self.skip_forward)
    
    def clear_formating(self):
        cursor = self.browser.textCursor()
        the_format = QTextCharFormat()
        the_format.setFontPointSize(14)
        the_format.setFontWeight(0)
        the_format.setBackground(QtGui.QBrush(QtGui.QColor("Transparent")))
        cursor.setCharFormat(the_format)

    
    def highlight(self,color):
        cursor = self.browser.textCursor()
        the_format = QTextCharFormat()
        the_format.setBackground(QtGui.QBrush(QtGui.QColor(color)))
        cursor.mergeCharFormat(the_format)
    
    def clear_highlighting(self):
        cursor = self.browser.textCursor()
        the_format = QTextCharFormat()
        # the_format.setBackground(None)
        the_format.setBackground(QtGui.QBrush(QtGui.QColor("Transparent")))
        cursor.mergeCharFormat(the_format)
    
    def change_font_type(self):
        if self.browser.textCursor().hasSelection():
            font = self.format_widget.font_options.currentText()
            cursor = self.browser.textCursor()
            the_format = QTextCharFormat()
            weight = cursor.charFormat().fontWeight()
            the_format.setFont(QtGui.QFont(font))
            the_format.setFontWeight(weight)
            cursor.mergeCharFormat(the_format)


    def set_global_settings(self):
        with open(os.path.join(os.getcwd(),"App","settings.json"),"r+") as f:
            data = json.load(f)
            self.json_settings = data

    
    def display_msg(self,title,text):
        msgBox = QMessageBox()
        msgBox.setText(text)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.setWindowTitle(title)
        msgBox.exec()
        
    def browser_clicked(self):
        if self.browser.textCursor().hasSelection():
            self.get_sel_in_context()
        else:
            self.get_word_in_context()

    def get_word_in_context(self):
        cursor = self.browser.textCursor()
        pos_of_click = cursor.position()
        cursor.select(QTextCursor.WordUnderCursor)
        if cursor.hasSelection():
            word = cursor.selectedText()
            context = self.get_context(cursor)
            split_context = re.split('(\W)', context)
            for i, w in enumerate(split_context):
                if w == word:
                    split_context[i] = "<b>" + split_context[i] + "</b>"
            context_bold = "".join(split_context)
            self.autofill_flashcard(context_bold)
            self.handle_lookup(word, context)

    def get_sel_in_context(self):
        cursor = self.browser.textCursor()
        selection = self.browser.textCursor().selectedText()
        context = self.get_context(cursor)
        context_bold = context.replace(selection, "<b>" + selection + "</b>")
        self.autofill_flashcard(context_bold)
        self.handle_lookup(selection, context)

    def get_context(self,cursor):
        steps_to_move = 15 # <--- this could be changed in the settings
        not_reached_upper_limit = True
        not_reached_lower_limit = True
        for i in range(steps_to_move):
            cursor.movePosition(QTextCursor.WordLeft,QTextCursor.MoveAnchor)
            if cursor.atBlockStart():
                not_reached_upper_limit = False
                break
        for i in range(steps_to_move*2):
            cursor.movePosition(QTextCursor.WordRight,QTextCursor.KeepAnchor)
            if cursor.atBlockEnd():
                not_reached_lower_limit = False
                break
        context = cursor.selectedText()
        if not_reached_lower_limit:
            context = context.strip() + "..."
        if not_reached_upper_limit:
            context = "..." + context
        return context

    def autofill_flashcard(self,context):
        self.flash_front.clear()
        self.flash_front.setHtml(context)


    def handle_lookup(self, selection, context):
        if selection != "":
            for i, tab in enumerate(self.json_settings["tabs"]):
                self.my_tabs[i].setUrl(QUrl(tab[1].replace("WORD",selection).replace("SENT",context)))
        if self.json_settings["autofill_flashcards"] == True:
            self.flash_back.clear()
            try:
                translation = self.translator.translate(selection)
                self.flash_back.insertPlainText(translation)
            except Exception as e:
                print(f"there was an error with the autofill api: {e}")

    def handle_toolbar_click(self,action):
        action = action.text()
        if action == 'play':
            self.toggle_play_audio()
        if action == 'open':
            try:
                self.open_file()
            except Exception as e:
                self.display_msg("Error","Failed to open file.\n" + str(e))
        if action == 'save':
            try:
                self.save_file()
            except Exception as e:
                self.display_msg("Error","Failed to save file.\n" + str(e))
        if action == 'download':
            self.download_flashcards()
        if action == 'skip_back':
            self.skip_back()
        if action == 'skip_forward':
            self.skip_forward()
        if action == 'settings':
            self.settings.dict_table_widget.blockSignals(True)
            self.settings.load_settings(False)
            self.settings.dict_table_widget.blockSignals(False)
            self.settings.show()
        if action == 'list':
            self.flashcards_list.list_table_widget.clear()
            self.flashcards_list.setup_table_widget()
            self.flashcards_list.show()
        if action == 'help':
            self.help_page.show()

        if action == 'highlight':
            self.highlight_grammar_terms()
        if action == 'format':
            self.format_widget.show()

    def save_file(self):
        file_path = QFileDialog.getSaveFileName(self, 'Save File','',"HTML Files (*.html);; TXT Files (*.txt) ;; DOCX Files (*.docx)")[0]
        file_type = self.get_file_extension_from_path(file_path)
        filename = self.get_filename_from_path(file_path)
        if file_path:
            if file_type == '.txt':
                file_data = self.browser.toPlainText()
                with open(file_path, 'w', encoding='utf8', errors='ignore') as f:
                        f.write(file_data)
            if file_type == '.html':
                file_data = self.browser.toHtml()
                with open(file_path, 'w', encoding='utf8', errors='ignore') as f:
                        f.write(file_data)
            if file_type == '.docx':
                file_data = self.browser.toHtml()
                file_data = html2docx(file_data,title=filename).getvalue()
                with open(file_path, 'wb') as f:
                        f.write(file_data)
    
    def open_file(self):
        file_path = QFileDialog.getOpenFileName(self,'select a text file to open')[0]
        resources_path = self.get_folder_from_path(file_path)
        filetype = self.get_file_extension_from_path(file_path)
        self.browser.document().setMetaInformation(QTextDocument.DocumentUrl, QtCore.QUrl.fromLocalFile(resources_path).toString())
        if filetype == ".txt":
            with open(file_path,'r') as f:
                data = f.read()
                self.browser.clear()
                self.browser.insertPlainText(data)
            self.load_audio(file_path)
            return
        if filetype == ".html" or filetype == ".htm" or filetype == ".mhtml" or filetype == ".mht":
            with open(file_path,'r',encoding='utf8', errors='ignore') as f: #                 
                data = f.read()
                # print(data)
                self.browser.clear()
                self.browser.insertHtml(data)
            self.load_audio(file_path)
            return
        if filetype == ".pdf":
            with fitz.open(file_path) as doc:
                pages = []
                for i in range(doc.page_count):
                    pages.append(doc.load_page(i)) #TODO: should load all pages
                for page in pages:
                    justHtml = page.get_text("html")
                    self.browser.clear()
                    self.browser.insertHtml(justHtml)
                self.load_audio(file_path)
                return

        if filetype == ".docx":
            with open(file_path,'rb') as f:
                # data = f.read()
                justHtml = mammoth.convert_to_html(f)
                self.browser.clear()
                self.browser.insertHtml(justHtml.value)
            self.load_audio(file_path)
            return
        # if not returned before
        self.display_msg("Error",f'Could not recognize file: "{filetype}"')
        

    def add_flashcard(self): # this appends card to json file
        pos = self.audio_player.position()
        dur = self.audio_player.duration()
        start_time = self.get_start_time(pos,5000)
        end_time = self.get_end_time(pos,5000,dur)
        
        front = self.flash_front.toHtml()
        back = self.flash_back.toHtml()
        front_html = BeautifulSoup(front,"html.parser")
        back_html = BeautifulSoup(back,"html.parser")
        front = front_html.body
        back = back_html.body
        front_text = front.getText()
        back_text = back.getText() 
        image = back_html.find('img')
        try:
            source = image['src']
            image.decompose()
        except:
           source = ""

        if front_text == "\n":
            self.display_msg("Oops!","No text was found for the Flashcard.")
            return 0
        if back_text == "\n" and image is None:
            self.display_msg("Oops!","No text or images were found for back of the Flashcard.")
            return 0
        flash_dict = {"front":str(front), "back":str(back),"img":source}
        path = "App\\flashcards.json"
        self.flash_front.clear()
        self.flash_back.clear()
        if not os.path.exists(path):
            self.reset_flashcard_json()
        with open(path,"r+") as f:
            data = json.load(f)
            data["cards"].append(flash_dict)
            f.seek(0)
            json.dump(data,f)

    def download_flashcards(self): #this creates anki deck
        filepath = QFileDialog.getSaveFileName(self, 'Download Anki Deck','',"Anki File (*.apkg)")[0]
        if filepath == "":
            return 0
        deck_name = self.get_filename_from_path(filepath)

        with open("App\\flashcards.json","r+") as f:
            data = json.load(f)
        if data["cards"] == []:
            self.display_msg("Oops!", "There are no cards to make an anki deck with.\nUse the flashcard generator in the top right corner to make some.")
            return 0
        self.anki_gen.start_everything(data,deck_name,filepath)
        self.reset_flashcard_json()

    def reset_flashcard_json(self):
        # create/clear flashcards.json
        path = "App\\flashcards.json"
        blank = {"cards":[]}
        if os.path.exists(path):
            os.remove(path)
        with open("App\\flashcards.json",'w+') as f:
            json.dump(blank,f)
    
    def load_audio(self, filePath):
        # check if audio file exists
        expected_filepath_wav = str(self.get_folder_from_path(filePath)) + str(self.get_filename_from_path(filePath)) + ".wav"
        expected_filepath_mp3 = str(self.get_folder_from_path(filePath)) + str(self.get_filename_from_path(filePath)) + ".mp3"
        if os.path.exists(expected_filepath_wav):
            self.audio_player.setMedia(QMediaContent(QUrl.fromLocalFile(expected_filepath_wav)))
        if os.path.exists(expected_filepath_mp3):
            self.audio_player.setMedia(QMediaContent(QUrl.fromLocalFile(expected_filepath_mp3)))
        else:
            self.audio_player.setMedia(QMediaContent(None))
     
    def toggle_play_audio(self):
        state = self.audio_player.state()
        if state == 1:
            self.audio_player.pause()
            if self.json_settings["dark_theme"]:
                self.play_action.setIcon(QIcon("App\\img\\play_dark.png"))
            else:
                self.play_action.setIcon(QIcon("App\\img\\play.png"))
        if state == 0 or state == 2:
            self.audio_player.play()
            if self.json_settings["dark_theme"]:
                self.play_action.setIcon(QIcon("App\\img\\pause_dark.png"))
            else:
                self.play_action.setIcon(QIcon("App\\img\\pause.png"))
        
    def skip_forward(self):
        skip_amount = 3000
        pos = self.audio_player.position()
        new_pos = pos + skip_amount
        self.audio_player.setPosition(new_pos)

    def skip_back(self):
        skip_amount = 3000
        pos = self.audio_player.position()
        new_pos = pos - skip_amount
        self.audio_player.setPosition(new_pos)
    
    def update_slider_duration(self,duration):
        self.audio_slider.setMaximum(duration)
    
    def update_slider_position(self,position):
        self.audio_slider.blockSignals(True)
        self.audio_slider.setValue(position)
        self.audio_slider.blockSignals(False)
        # get audio timestamp
        min_mil_sec = 5000
        current_pos_mil = position
        duration = self.audio_player.duration()
        start_time = self.get_start_time(current_pos_mil,min_mil_sec)
        end_time = self.get_end_time(current_pos_mil,min_mil_sec,duration)
        new_string = f"Timestamps: {datetime.timedelta(seconds=round(start_time/1000))}--{datetime.timedelta(seconds=round(end_time/1000))}"
        self.flash_audio_label.setText(new_string)
    
    def get_start_time(self,pos,min_mil):
        if pos < min_mil:
            return 0
        else:
            return pos - min_mil
    def get_end_time(self,pos,min_mil,dur):
        if pos < dur - min_mil:
            return pos + min_mil
        else:
            return dur




    def get_filename_from_path(self, path):
        filename = os.path.basename(path)
        name = filename.split('.')[0]
        return name
    
    def get_file_extension_from_path(self, path):
        filename = os.path.basename(path)
        extension = "." + filename.split('.')[1]
        return extension

    def get_folder_from_path(self, path):
        folder = os.path.dirname(path)
        return folder + "/"

    def save_settings_to_json(self):
        # get the data from table etc
        tab_settings = []
        number_of_rows_dict = self.settings.dict_table_widget.rowCount() -1 
        for i in range(number_of_rows_dict):
            tab_settings.append([self.settings.dict_table_widget.item(i,1).text(),self.settings.dict_table_widget.item(i,2).text()])
        dark_theme = self.settings.dark_theme_checkbox.isChecked()
        autofill_flashcards = self.settings.autofill_checkbox.isChecked()
        # grammar highlighter settings
        
        dis_dict = {}
        number_of_rows_dis = self.settings.discourse_table_widget.rowCount() -1
        for i in range(number_of_rows_dis):
            try:
                cat_key = self.settings.discourse_table_widget.item(i,1).text()
                cat_color = self.settings.dis_color[i].styleSheet()[23:-1]
                cat_list = self.settings.discourse_table_widget.item(i,3).text().split(", ")
                dis_dict[cat_key] = {"color": cat_color,"list": cat_list}
            except:
                pass

        # update json file
        json_data = self.json_settings
        json_data["tabs"] = tab_settings
        json_data["dark_theme"] = dark_theme
        json_data["autofill_flashcards"] = autofill_flashcards
        json_data["discourse_highlighter"] = dis_dict
        self.settings.close()
        os.remove(os.path.join(os.getcwd(),"App","settings.json"))
        with open(os.path.join(os.getcwd(),"App","settings.json"),"w") as f:
            json.dump(json_data,f)
        self.set_global_settings()
        # refresh current instance
        self.tabs.clear()
        self.start_tabs()
    
    def highlight_grammar_terms(self):
        index =0
        for key, value in self.json_settings["discourse_highlighter"].items():
            color_list = value["color"].split(",")
            color_ints = []
            for x in color_list:
                color_ints.append(int(x))
            color_ints.append(255)
            color = QtGui.QColor()
            color.setRgb(color_ints[0],color_ints[1],color_ints[2],color_ints[3])
            regex_for_word_list = "|".join(self.wrap_in_b(value["list"]))
            the_format = QTextCharFormat()
            the_format.setBackground(QtGui.QBrush(color))
            self.apply_highlight(regex_for_word_list,the_format)
            index += 1

    def apply_highlight(self,pattern,the_format):
        cursor = self.browser.textCursor()
        regex = QtCore.QRegExp(pattern,Qt.CaseSensitivity.CaseInsensitive)
        # regex.setCaseSensitivity()
        pos = 0
        index = regex.indexIn(self.browser.toPlainText(),pos)
        while (index != -1):
            cursor.setPosition(index)
            cursor.movePosition(QTextCursor.EndOfWord,1)
            cursor.mergeCharFormat(the_format)
            pos = index + regex.matchedLength()
            index = regex.indexIn(self.browser.toPlainText(),pos)


    def wrap_in_b(self,the_list):
        # this is for the regex (\b means word border)
        new_list = []
        for i in the_list:
            i = f"\\b{i}\\b"
            new_list.append(i)
        return new_list






if __name__ == "__main__":
    app = QApplication(sys.argv)


    app.setStyle("fusion")
    mainApp = MainWindow()
    mainApp.setWindowTitle("Linguini")
    mainApp.setWindowIcon(QtGui.QIcon(os.path.join(os.getcwd(),"App","img","linguini.png")))
    mainApp.showMaximized()
    sys.exit(app.exec_())