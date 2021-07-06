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
import time
import datetime
from multi_threading import Worker
from database_helper import Database


class MainWindow(MainUIWidget):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # self.json_settings = {}
        # self.set_global_settings()
        # self.bottom_right_pane.start_tabs(self.json_settings) # this being called after the settings, allows time to read the json settings file
        # Create classes instances:
        self.audio_player = QMediaPlayer()
        self.anki_gen = AnkiDeckGenerator()
        self.settings = SettingsPage()
        self.translator = GoogleTranslate()
        self.flashcards_list = FlashcardManager()
        self.format_widget = FormatSelectedText(self.left_pane.browser)
        self.help_page = HelpWindow()
        self.db = Database()
        self.thread_pool = QtCore.QThreadPool()
        #connections
        self.left_pane.browser.clicked.connect(self.browser_clicked)
        self.left_pane.browser.hightlight.connect(self.highlight)
        self.left_pane.browser.clear_highlighting.connect(self.format_widget.clear_highlighting)
        self.left_pane.browser.hover.connect(self.hover_over_word)
        self.left_pane.toolbar.actionTriggered[QAction].connect(self.handle_toolbar_click)
        self.top_right_pane.toolbar.actionTriggered[QAction].connect(self.handle_toolbar_click)
        self.top_right_pane.make_flash_btn.clicked.connect(self.add_flashcard)
        self.audio_player.durationChanged.connect(self.update_slider_duration)
        self.audio_player.positionChanged.connect(self.update_slider_position)
        self.left_pane.audio_slider.valueChanged.connect(self.audio_player.setPosition)
        self.settings.save_button.clicked.connect(self.save_settings_to_db)
        self.settings.other_tab.dark_theme_checkbox.stateChanged.connect(self.toggle_theme)
        self.settings.user_tab.user_combobox.currentTextChanged.connect(self.change_current_user)
        self.settings.user_tab.add_user_btn.clicked.connect(self.add_new_user)
        self.settings.cancel_button.clicked.connect(self.settings.close)
        self.top_right_pane.unknown_btn.clicked.connect(lambda: self.save_to_vocab("unknown"))
        self.top_right_pane.semi_known_btn.clicked.connect(lambda: self.save_to_vocab("semi-known"))
        self.top_right_pane.known_btn.clicked.connect(lambda: self.save_to_vocab("known"))
        # other
        self.dark_theme_palette = self.setup_dark_theme()
        self.run_start_up_settings()
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
    


    # startup settings - last user, darktheme...
    def run_start_up_settings(self):
        self.current_user = self.db.get_last_user()
        self.all_users_names = self.db.get_all_users()
        self.current_online_tools = self.db.get_online_tools(self.current_user["id"])
        self.current_discourse_settings = self.db.get_discourse_settings(self.current_user["id"])
        self.current__other_settings = self.db.get_other_settings(self.current_user["id"])
        self.current_highlighters = self.db.get_highlighters(self.current_user["id"])
        self.recent_files = self.db.get_recent_files(self.current_user["id"])
        # UI
        if self.current__other_settings["dark_theme"]:
            self.setPalette(self.dark_theme_palette)
            self.set_icons(True)
        else:
            self.set_icons(False)
        # online tools
        self.bottom_right_pane.start_tabs(self.current_online_tools)


    def load_settings_to_settings_page(self):
        self.settings.load_online_tool_settings(self.current_online_tools)
        self.settings.load_other_settings(self.current__other_settings)
        self.settings.load_user(self.all_users_names,self.current_user)
    
    def change_current_user(self):
        new_user_name = self.settings.user_tab.user_combobox.currentText()
        self.db.set_last_user(new_user_name)
        self.run_start_up_settings()
        self.load_settings_to_settings_page()
    
    def add_new_user(self):
        new_user_name = self.settings.user_tab.add_user_name.text()
        if self.db.add_new_user(new_user_name):
            self.display_msg("Oops!","That user name already exists")
        else:
            self.db.set_last_user(new_user_name)
            self.run_start_up_settings()
            self.settings.user_tab.add_user_name.clear()
            self.load_settings_to_settings_page()
    
    def save_settings_to_db(self):
        self.settings.close()
        # online tools
        online_tools_list = []
        row_count = self.settings.online_tools_tab.online_tools_table_widget.rowCount() -1
        for row in range(row_count):
            online_tools_list.append([self.settings.online_tools_tab.online_tools_table_widget.item(row,1).text(),self.settings.online_tools_tab.online_tools_table_widget.item(row,2).text()])
        self.db.save_online_tools(online_tools_list,self.current_user["id"])
        # discourse settings
        #TODO:
        # other settings
        other_settings = {}
        other_settings["dark_theme"] = self.settings.other_tab.dark_theme_checkbox.isChecked()
        other_settings["autofill_back_of_flashcard"] = self.settings.other_tab.autofill_checkbox.isChecked()
        self.db.save_other_settings(self.current_user["id"], other_settings)
        self.run_start_up_settings()
    
    def save_to_vocab(self,confid):
        for item in self.current_highlighters:
            if item[4] == confid:
                current_confidence = item[0]
        word_to_save = self.current_selection
        definition_to_save = self.top_right_pane.flash_back.toPlainText()
        self.db.save_word_to_vocabulary(self.current_user["id"],word_to_save, definition_to_save,current_confidence)

    def start_highlight_in_thread(self):
        #clear formatting
        cursor = self.left_pane.browser.textCursor()
        cursor.select(QTextCursor.Document)
        clear_format = QtGui.QTextCharFormat()
        clear_format.setBackground(QtGui.QBrush(QtGui.QColor("Transparent")))
        clear_format.setUnderlineStyle(QTextCharFormat.NoUnderline)
        cursor.mergeCharFormat(clear_format)
        # start highlighter in another thread
        worker = Worker(self.highlight_terms,self.left_pane.browser.toPlainText())
        worker.signals.word_to_mark.connect(self.apply_highlight)
        self.thread_pool.start(worker)
    
    def highlight_terms(self,plain_text,word_to_mark_callback):
        for highlighter in self.current_highlighters:
            hl_id = highlighter[0]
            vocab_for_hl = self.db.get_list_of_vocab(self.current_user["id"], hl_id)
            hl_color = [int(s) for s in highlighter[2].split(",")] # converts color string to list of ints
            hl_style = highlighter[3]

            if vocab_for_hl != []:
                color = QtGui.QColor()
                color.setRgbF(hl_color[0],hl_color[1],hl_color[2],hl_color[3])
                the_format = QTextCharFormat()
                if hl_style == "underline":
                    the_format.setUnderlineColor(color) 
                    the_format.setUnderlineStyle(QTextCharFormat.SingleUnderline)
                elif hl_style == "background":
                    the_format.setBackground(QtGui.QBrush(color))
                for term in vocab_for_hl:
                    term = term[2]
                    # term = f"\\b{term}\\b"
                    pattern = re.compile(term,re.IGNORECASE)
                    for m in re.finditer(pattern,plain_text):
                        start, end = m.span()
                        length_of_selection = end - start
                        dict_to_emit = {"pos":start, "length":length_of_selection,"format":the_format}
                        word_to_mark_callback.emit(dict_to_emit)
                        time.sleep(0.0000001)

    def apply_highlight(self,mark_dict):
        cursor = self.left_pane.browser.textCursor()
        cursor.setPosition(mark_dict["pos"])
        for i in range(mark_dict["length"]):
            cursor.movePosition(QTextCursor.NextCharacter,QTextCursor.KeepAnchor)
        cursor.mergeCharFormat(mark_dict["format"])
        
    def highlight(self,color):
        cursor = self.left_pane.browser.textCursor()
        the_format = QTextCharFormat()
        the_format.setBackground(QtGui.QBrush(QtGui.QColor(color)))
        cursor.mergeCharFormat(the_format)

    def hover_over_word(self,pos): # TODO: Should this be constantly running in another thread?
        text_cursor = QTextCursor()
        text_cursor = self.left_pane.browser.cursorForPosition(pos)
        # find start of highlight
        the_format = text_cursor.charFormat()
        is_highlighted = the_format.fontUnderline()
        while is_highlighted:
            text_cursor.movePosition(QTextCursor.PreviousCharacter,QTextCursor.MoveAnchor)
            the_format = text_cursor.charFormat()
            is_highlighted = the_format.fontUnderline()
        #should be at the beginning of the highlight
        #find end of highlight 
        is_highlighted = True
        while is_highlighted:
            text_cursor.movePosition(QTextCursor.NextCharacter,QTextCursor.KeepAnchor)
            the_format = text_cursor.charFormat()
            is_highlighted = the_format.fontUnderline()
        text_cursor.movePosition(QTextCursor.PreviousCharacter,QTextCursor.KeepAnchor)
        #should be at end of highlight
        sel = text_cursor.selectedText()
        text_cursor.clearSelection()

        if sel !="":
            # sel = text_cursor.selectedText()
            #at the moment this seems to be ok without being in another thread, but what would it be like with 20000 times more words in database?
            list_of_matchs = self.db.look_up_sel_in_db(sel)
            if list_of_matchs != []:
                defin = list_of_matchs[0][3]
                self.left_pane.browser.setToolTipDuration(2000)
                self.left_pane.browser.setToolTip(f"{defin}")
            else:
                self.left_pane.browser.setToolTip("")
        else:
            self.left_pane.browser.setToolTip("")

    # def set_global_settings(self):
    #     with open(os.path.join(os.getcwd(),"src","settings.json"),"r+") as f:
    #         data = json.load(f)
    #         self.json_settings = data

    def display_msg(self,title,text):
        msgBox = QMessageBox()
        msgBox.setText(text)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.setWindowTitle(title)
        msgBox.exec()
        
    def browser_clicked(self):
        if self.left_pane.browser.textCursor().hasSelection():
            self.get_sel_in_context()
        else:
            self.get_word_in_context()

    def get_word_in_context(self):
        cursor = self.left_pane.browser.textCursor()
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
            self.current_selection = word
            self.autofill_searchbar(word)
            self.autofill_flashcard(context_bold)
            self.handle_lookup(word, context)

    def get_sel_in_context(self):
        cursor = self.left_pane.browser.textCursor()
        selection = self.left_pane.browser.textCursor().selectedText()
        context = self.get_context(cursor)
        context_bold = context.replace(selection, "<b>" + selection + "</b>")
        self.current_selection = selection
        self.autofill_searchbar(selection)
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
    
    def autofill_searchbar(self,search_term):
        self.left_pane.searchbar_lineedit.setText(search_term)

    def autofill_flashcard(self,context):
        self.top_right_pane.flash_front.clear()
        self.top_right_pane.flash_front.setHtml(context)

    def handle_lookup(self, selection, context):
        if selection != "":
            for i, row in enumerate(self.current_online_tools):
                self.bottom_right_pane.my_tabs[i].setUrl(QUrl(row[2].replace("WORD",selection).replace("SENT",context)))
        if self.current__other_settings["autofill_back_of_flashcard"]:
            self.top_right_pane.flash_back.clear()
            try:
                translation = self.translator.translate(selection)
                self.top_right_pane.flash_back.insertPlainText(translation)
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
            self.load_settings_to_settings_page()
            self.settings.show()
        if action == 'list':
            self.flashcards_list.list_table_widget.clear()
            self.flashcards_list.setup_table_widget()
            self.flashcards_list.show()
        if action == 'help':
            self.help_page.show()
        if action == 'highlight':
            self.start_highlight_in_thread()
        if action == 'format':
            self.format_widget.show()

    def save_file(self):
        filepath = QFileDialog.getSaveFileName(self, 'Save File','',"HTML Files (*.html);; TXT Files (*.txt) ;; DOCX Files (*.docx)")[0]
        if filepath:
            file_type = self.get_file_extension_from_path(filepath)
            filename = self.get_filename_from_path(filepath)
            if file_type == '.txt':
                file_data = self.left_pane.browser.toPlainText()
                with open(filepath, 'w', encoding='utf8', errors='ignore') as f:
                        f.write(file_data)
            elif file_type == '.html':
                file_data = self.left_pane.browser.toHtml()
                with open(filepath, 'w', encoding='utf8', errors='ignore') as f:
                        f.write(file_data)
            elif file_type == '.docx':
                file_data = self.left_pane.browser.toHtml()
                file_data = html2docx(file_data,title=filename).getvalue()
                with open(filepath, 'wb') as f:
                        f.write(file_data)
            else:
                self.display_msg("Error", f'Only ".txt", ".html", and ".docx" file extensions are supported.')
            self.db.add_recent_file(filepath,self.current_user["id"])
    
    def open_file(self):
        filepath = QFileDialog.getOpenFileName(self,'select a text document')[0]
        if not filepath:
            return
        resources_path = self.get_folder_from_path(filepath)
        filetype = self.get_file_extension_from_path(filepath)
        self.left_pane.browser.document().setMetaInformation(QTextDocument.DocumentUrl, QtCore.QUrl.fromLocalFile(resources_path).toString())
        is_html = True
        if filetype == ".txt":
            with open(filepath,'r') as f:
                data = f.read()
                is_html = False
        elif filetype == ".html" or filetype == ".htm" or filetype == ".mhtml" or filetype == ".mht":
            with open(filepath,'r',encoding='utf8', errors='ignore') as f:
                data = f.read()
        elif filetype == ".docx":
            with open(filepath,'rb') as f:
                data = mammoth.convert_to_html(f).value
        elif filetype == ".pdf":
            with fitz.open(filepath) as doc:
                pages = []
                for i in range(doc.page_count):
                    pages.append(doc.load_page(i))
                for page in pages:
                    data = page.get_text("html")
                    self.left_pane.browser.clear()
                    self.left_pane.browser.insertHtml(data)
            self.load_audio(filepath)
            self.db.add_recent_file(filepath,self.current_user["id"])
        else:
            self.display_msg("Error",f'Could not recognize file: "{filetype}"')
            return
        self.left_pane.browser.clear()
        if is_html:
            self.left_pane.browser.insertHtml(data)
            self.db.add_recent_file(filepath)
        else:
            self.left_pane.browser.insertPlainText(data)
        self.load_audio(filepath)

        

    def add_flashcard(self): # this appends card to json file
        pos = self.audio_player.position()
        dur = self.audio_player.duration()
        start_time = self.get_start_time(pos,5000)
        end_time = self.get_end_time(pos,5000,dur)
        
        front = self.top_right_pane.flash_front.toHtml()
        back = self.top_right_pane.flash_back.toHtml()
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
        flash_dict = {"front":str(front), "back":str(back),"img":source,"audio":[start_time,end_time]}
        cards_path = os.path.join("src", "flashcards.json")
        self.top_right_pane.flash_front.clear()
        self.top_right_pane.flash_back.clear()
        if not os.path.exists(cards_path):
            self.reset_flashcard_json()
        with open(cards_path,"r+") as f:
            data = json.load(f)
            data["cards"].append(flash_dict)
            f.seek(0)
            json.dump(data,f)

    def download_flashcards(self): #this creates anki deck
        filepath = QFileDialog.getSaveFileName(self, 'Download Anki Deck','',"Anki File (*.apkg)")[0]
        if filepath == "":
            return 0
        deck_name = self.get_filename_from_path(filepath)

        with open(os.path.join("src", "flashcards.json"),"r+") as f:
            data = json.load(f)
        if data["cards"] == []:
            self.display_msg("Oops!", "There are no cards to make an anki deck with.\nUse the flashcard generator in the top right corner to make some.")
            return 0
        self.anki_gen.start_everything(data,deck_name,filepath)
        self.reset_flashcard_json()

    def reset_flashcard_json(self):
        # create/clear flashcards.json
        cards_path = os.path.join("src", "flashcards.json")
        blank = {"cards":[]}
        if os.path.exists(cards_path):
            os.remove(cards_path)
        with open(cards_path,'w+') as f:
            json.dump(blank,f)
    
    def load_audio(self, filePath):
        # check if audio file exists
        expected_filepath_wav = str(self.get_folder_from_path(filePath)) + str(self.get_filename_from_path(filePath)) + ".wav"
        expected_filepath_mp3 = str(self.get_folder_from_path(filePath)) + str(self.get_filename_from_path(filePath)) + ".mp3"
        if os.path.exists(expected_filepath_wav):
            self.audio_player.setMedia(QMediaContent(QUrl.fromLocalFile(expected_filepath_wav)))
        elif os.path.exists(expected_filepath_mp3):
            self.audio_player.setMedia(QMediaContent(QUrl.fromLocalFile(expected_filepath_mp3)))
        else:
            self.audio_player.setMedia(QMediaContent(None))
     
    def toggle_play_audio(self):
        state = self.audio_player.state()
        if state == 1:
            self.audio_player.pause()
            if self.json_settings["dark_theme"]:
                self.left_pane.play_action.setIcon(QIcon(os.path.join("src", "img", "play_dark.png")))
            else:
                self.left_pane.play_action.setIcon(QIcon(os.path.join("src", "img", "play.png")))
        if state == 0 or state == 2:
            self.audio_player.play()
            if self.json_settings["dark_theme"]:
                self.left_pane.play_action.setIcon(QIcon(os.path.join("src", "img", "pause_dark.png")))
            else:
                self.left_pane.play_action.setIcon(QIcon(os.path.join("src", "img", "pause.png")))
        
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
        self.left_pane.audio_slider.setMaximum(duration)
    
    def update_slider_position(self,position):
        self.left_pane.audio_slider.blockSignals(True)
        self.left_pane.audio_slider.setValue(position)
        self.left_pane.audio_slider.blockSignals(False)
        # get audio timestamp
        min_mil_sec = 5000
        current_pos_mil = position
        duration = self.audio_player.duration()
        start_time = self.get_start_time(current_pos_mil,min_mil_sec)
        end_time = self.get_end_time(current_pos_mil,min_mil_sec,duration)
        new_string = f"Timestamps: {datetime.timedelta(seconds=round(start_time/1000))}--{datetime.timedelta(seconds=round(end_time/1000))}"

        # self.flash_audio_label.setText(new_string)
    
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
        parts = os.path.splitext(path)
        if len(parts) == 2:
            return parts[1]
        else:
            return None

    def get_folder_from_path(self, path):
        folder = os.path.dirname(path)
        return folder + "/"
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    mainApp = MainWindow()
    mainApp.setWindowTitle("Langsoft")
    mainApp.setWindowIcon(QtGui.QIcon(os.path.join(os.getcwd(),"src","img","langsoft.png")))
    mainApp.showMaximized()
    sys.exit(app.exec_())