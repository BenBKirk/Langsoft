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
from gen_anki_deck import AnkiDeckGenerator
from settings_page import SettingsPage
from format_selected_text import FormatSelectedText
import mammoth
from html2docx import html2docx
from API.google_trans_API import GoogleTranslate
from flashcard_list_manager import FlashcardManager
from help_page import HelpWindow
import datetime
from multi_threading import Worker
from database_helper import Database
from syntax_highlighter import SyntaxHighlighter
import logging
logging.basicConfig(level=logging.DEBUG,filename="app.log",format='%(asctime)s - %(levelname)s - %(message)s')
class MainWindow(MainUIWidget):


    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
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
        self.highlighter = SyntaxHighlighter(self.left_pane.browser.document())
        self.recent_files_widget = QListWidget()
        #connections
        self.left_pane.browser.clicked.connect(self.browser_clicked)
        self.left_pane.browser.hightlight.connect(self.highlight)
        self.left_pane.browser.clear_highlighting.connect(self.format_widget.clear_highlighting)
        self.left_pane.browser.scroll.connect(self.refresh_hightlight_on_screen)
        self.left_pane.browser.verticalScrollBar().sliderMoved.connect(self.refresh_hightlight_on_screen)
        self.left_pane.toolbar.actionTriggered[QAction].connect(self.handle_toolbar_click)
        self.top_right_pane.toolbar.actionTriggered[QAction].connect(self.handle_toolbar_click)
        self.top_right_pane.make_flash_btn.clicked.connect(self.add_flashcard_to_db)
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
        self.format_widget.font_size_box.valueChanged.connect(lambda x: self.left_pane.browser.setFontPointSize(x))
        self.settings.user_tab.user_delete.clicked.connect(self.delete_user)
        # other
        self.dark_theme_palette = self.setup_dark_theme()
        self.run_start_up_settings()
        self.vocab_or_grammar = "vocab"
        # keyboard shortcuts
        self.lookup_shortcut = QShortcut(QtGui.QKeySequence("Ctrl+Up"),self)
        self.lookup_shortcut.activated.connect(self.browser_clicked)
        self.make_flashcard_shortcut = QShortcut(QtGui.QKeySequence("Ctrl+Down"),self)
        self.make_flashcard_shortcut.activated.connect(self.add_flashcard_to_db)
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
        self.current_grammar_rules = self.db.get_grammar_rules(self.current_user["id"])
        self.current_other_settings = self.db.get_other_settings(self.current_user["id"])
        self.current_highlighters = self.db.get_highlighters(self.current_user["id"])
        self.recent_files = self.db.get_recent_files(self.current_user["id"])
        self.current_selection = {"selection":"", "db_findings":[]}
        self.current_flashcard_audio = {"start":None,"end":None}
        # UI
        if self.current_other_settings["dark_theme"]:
            self.setPalette(self.dark_theme_palette)
            self.settings.setPalette(self.dark_theme_palette)
            self.flashcards_list.setPalette(self.dark_theme_palette)
            self.recent_files_widget.setPalette(self.dark_theme_palette)
            self.set_icons(True)
        else:
            self.set_icons(False)
        # online tools
        self.bottom_right_pane.start_tabs(self.current_online_tools)

    def load_settings_to_settings_page(self):
        self.settings.load_online_tool_settings(self.current_online_tools)
        self.settings.load_other_settings(self.current_other_settings)
        self.settings.load_user(self.all_users_names,self.current_user)
        self.settings.load_grammar_rules(self.current_grammar_rules)
    
    def change_current_user(self):
        new_user_name = self.settings.user_tab.user_combobox.currentText()
        self.db.set_last_user(new_user_name)
        self.run_start_up_settings()
        self.load_settings_to_settings_page()
    
    def add_new_user(self):
        new_user_name = self.settings.user_tab.add_user_name.text()
        if self.db.add_new_user(new_user_name):# returns true if user already exists
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
        tools_row_count = self.settings.online_tools_tab.online_tools_table_widget.rowCount() -1
        for row in range(tools_row_count):
            online_tools_list.append([
                self.settings.online_tools_tab.online_tools_table_widget.item(row,1).text(),
                self.settings.online_tools_tab.online_tools_table_widget.item(row,2).text()
                ])
        self.db.save_online_tools(online_tools_list,self.current_user["id"])

        # grammar settings
        grammar_rules_list = []
        rules_row_count = self.settings.grammar_tab.grammar_table_widget.rowCount() -1
        for row in range(rules_row_count):
            grammar_rules_list.append([
                self.settings.grammar_tab.on_widget[row].isChecked(),
                self.settings.grammar_tab.grammar_table_widget.item(row,2).text(),
                self.settings.grammar_tab.color_btn[row].styleSheet()[23:-1],
                self.settings.grammar_tab.opacity_widget[row].value(),
                self.settings.grammar_tab.style_widget[row].currentText(),
                self.settings.grammar_tab.grammar_table_widget.item(row,6).text()
            ])
        self.db.save_grammar_rules(grammar_rules_list,self.current_user["id"])

        
        # other settings
        other_settings = {}
        other_settings["dark_theme"] = self.settings.other_tab.dark_theme_checkbox.isChecked()
        other_settings["autofill_back_of_flashcard"] = self.settings.other_tab.autofill_checkbox.isChecked()
        self.db.save_other_settings(self.current_user["id"], other_settings)
        self.run_start_up_settings()
        self.start_update_highlight_words()
    
    def save_to_vocab(self,confid):
        definition_to_save = self.top_right_pane.flash_back.toPlainText()
        word_to_save = self.current_selection["selection"]
        #check if it is a phrase
        pattern = re.compile("\W")
        if re.search(pattern, word_to_save) != None:
            confid = confid + "-sent"
        # get highlighter id
        for item in self.current_highlighters:
            if item[4] == confid:
                current_confidence = item[0]

        if self.current_selection["db_findings"] != []:
            print("updated word in database")
            self.db.update_word_to_vocab(self.current_selection["db_findings"][0][0],definition_to_save,current_confidence)
            self.start_update_highlight_words()
        elif self.current_selection["selection"] != "":
            self.db.save_word_to_vocabulary(self.current_user["id"],word_to_save, definition_to_save,current_confidence)
            self.start_update_highlight_words()
        else:
            self.display_msg("sorry","No word or phrase selected")
        self.current_selection = {"selection":"", "db_findings":[]}

    def start_update_highlight_words(self):
        # start highlighter in another thread
        worker = Worker(self.update_highlight_words)
        worker.signals.finished.connect(self.refresh_hightlight_on_screen)
        self.thread_pool.start(worker)

    def refresh_hightlight_on_screen(self):
        """The syntax highlighter class only highlights one block at a time and that makes it more responsive,
             this function should be called when the user scrolls. It finds how much of the screen is visible
             and then rehighlights all the blocks it finds"""
        start_pos = self.left_pane.browser.cursorForPosition(QtCore.QPoint(0, 0)).position()
        bottom_right= QtCore.QPoint(self.left_pane.browser.viewport().width() -1,self.left_pane.browser.viewport().height()-1)
        end_pos = self.left_pane.browser.cursorForPosition(bottom_right).position()

        cursor = self.left_pane.browser.textCursor()
        cursor.setPosition(start_pos)
        old_pos = cursor.position()
        while cursor.position() < end_pos:
            block = cursor.block()
            self.highlighter.rehighlightBlock(block)
            cursor.movePosition(QTextCursor.NextBlock)
            if cursor.position() == old_pos:
                break
            else:
                old_pos = cursor.position()
    
    def update_highlight_words(self):
        if self.vocab_or_grammar == "vocab":
            all_dicts = []
            for highlighter in self.current_highlighters:
                hl_id = highlighter[0]
                vocab_for_hl = self.db.get_list_of_vocab_by_highlighter(self.current_user["id"], hl_id)
                hl_color = [float(s) for s in highlighter[2].split(",")] # converts color string to list of floats
                hl_style = highlighter[3]

                if vocab_for_hl != []:
                    color = QtGui.QColor()
                    color.setRgbF(hl_color[0],hl_color[1],hl_color[2],hl_color[3])
                    the_format = QTextCharFormat()
                    if hl_style == "underline":
                        the_format.setUnderlineColor(color) 
                        the_format.setUnderlineStyle(QTextCharFormat.SingleUnderline)
                    elif hl_style == "background":
                        the_format.setBackground(color)
                    
                    all_dicts.append({"vocab":vocab_for_hl,"fmt":the_format})
            self.highlighter.set_state(all_dicts,[])

        elif self.vocab_or_grammar == "grammar":
            print(self.current_grammar_rules)
            all_dicts = []
            for rule in self.current_grammar_rules:
                if rule[2]:
                    regex_list = [word.strip() for word in rule[7].split(',')]
                    the_format = QTextCharFormat()
                    color_from_str = [float(s) for s in rule[4].split(",")]
                    color = QtGui.QColor()
                    print(float(rule[5]))
                    color.setRgbF(color_from_str[0],color_from_str[1],color_from_str[2],float(rule[5]))
                    if rule[6] == "underline":
                        the_format.setUnderlineColor(color)
                        the_format.setUnderlineStyle(QTextCharFormat.SingleUnderline)
                    elif rule[6] == "highlight":
                        the_format.setBackground(color)
                    all_dicts.append({"words":regex_list,"fmt":the_format})
            self.highlighter.set_state([],all_dicts)


    def toggle_vocab_grammar(self):
        if self.vocab_or_grammar == "vocab":
            self.vocab_or_grammar = "grammar"
            self.left_pane.vocab_grammar_toggle.setText("toggle_g")
        elif self.vocab_or_grammar =="grammar":
            self.vocab_or_grammar = "vocab"
            self.left_pane.vocab_grammar_toggle.setText("toggle_v")

        if self.vocab_or_grammar == "vocab" and self.current_other_settings["dark_theme"]:
            self.left_pane.vocab_grammar_toggle.setIcon(QIcon(os.path.join("src","img","toggle_v_dark.png")))
        elif self.vocab_or_grammar == "grammar" and self.current_other_settings["dark_theme"]:
            self.left_pane.vocab_grammar_toggle.setIcon(QIcon(os.path.join("src","img","toggle_g_dark.png")))
        elif self.vocab_or_grammar == "vocab" and not self.current_other_settings["dark_theme"]:
            self.left_pane.vocab_grammar_toggle.setIcon(QIcon(os.path.join("src","img","toggle_v.png")))
        elif self.vocab_or_grammar == "grammar" and not self.current_other_settings["dark_theme"]:
            self.left_pane.vocab_grammar_toggle.setIcon(QIcon(os.path.join("src","img","toggle_g.png")))
        self.start_update_highlight_words()
        


        
    def highlight(self,color):
        cursor = self.left_pane.browser.textCursor()
        the_format = QTextCharFormat()
        the_format.setBackground(QtGui.QBrush(QtGui.QColor(color)))
        cursor.mergeCharFormat(the_format)

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
        cursor.select(QTextCursor.WordUnderCursor)
        if cursor.hasSelection():
            word = cursor.selectedText()
            context = self.get_context(cursor)
            split_context = re.split('(\W)', context)
            for i, w in enumerate(split_context):
                if w == word:
                    split_context[i] = "<b>" + split_context[i] + "</b>"
            context_bold = "".join(split_context)
            self.autofill_searchbar(word)
            self.autofill_flashcard(context_bold)
            self.handle_lookup(word, context)

    def get_sel_in_context(self):
        cursor = self.left_pane.browser.textCursor()
        selection = self.left_pane.browser.textCursor().selectedText()
        context = self.get_context(cursor)
        context_bold = context.replace(selection, "<b>" + selection + "</b>")
        self.autofill_searchbar(selection)
        self.autofill_flashcard(context_bold)
        self.handle_lookup(selection.strip(), context)

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
        #check database first
        try:
            db_findings = self.db.look_up_sel_in_db(selection,self.current_user["id"])
        except Exception as e:
            logging.exception("while looking for definition in db")

        for i, row in enumerate(self.current_online_tools):
            self.bottom_right_pane.my_tabs[i].setUrl(QUrl(row[2].replace("WORD",selection).replace("SENT",context)))
        if db_findings != []:
            self.top_right_pane.flash_back.clear()
            self.top_right_pane.flash_back.insertPlainText(db_findings[0][3])
        elif self.current_other_settings["autofill_back_of_flashcard"]:
            self.top_right_pane.flash_back.clear()
            try:
                translation = self.translator.translate(selection)
                self.top_right_pane.flash_back.insertPlainText(translation)
            except Exception as e:
                logging.exception("google translate autofill api")
                print(f"there was an error with the autofill api: {e}")
        self.current_selection = {"selection":selection,"db_findings":db_findings}

    def handle_toolbar_click(self,action):
        action = action.text()
        if action == 'play':
            self.toggle_play_audio()
        elif action == 'open':
            try:
                self.open_file()
            except Exception as e:
                logging.exception("when opening file")
                self.display_msg("Error","Failed to open file.\n" + str(e))
        elif action == 'save':
            try:
                self.save_file()
            except Exception as e:
                logging.exception("when saving file")
                self.display_msg("Error","Failed to save file.\n" + str(e))
        elif action == 'download':
            self.download_flashcards()
        elif action == 'skip_back':
            self.skip_back()
        elif action == 'skip_forward':
            self.skip_forward()
        elif action == 'settings':
            self.load_settings_to_settings_page()
            self.settings.show()
        elif action == 'list':
            self.flashcards_list.set_up(self.current_user["id"])
            self.flashcards_list.show()
        elif action == 'help':
            self.help_page.show()
        elif action == 'highlight':
            self.start_update_highlight_words()
        elif action == 'format':
            self.format_widget.show()
        elif action == 'toggle_v' or action == 'toggle_g':
            self.toggle_vocab_grammar()
        elif action == 'no_sound':
            self.set_audio_for_flashcard()
        elif action == 'blank':
            self.new_blank_document()

        elif action == 'recent_file':
            self.open_recent_file_window()


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
    
    def open_file(self,filepath_passed=None):
        if not filepath_passed:
            filepath = QFileDialog.getOpenFileName(self,'select a text document')[0]
            if not filepath:
                return
        else:
            filepath = filepath_passed
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
            self.db.add_recent_file(filepath,self.current_user["id"])
        else:
            self.left_pane.browser.insertPlainText(data)
            self.db.add_recent_file(filepath,self.current_user["id"])
        self.load_audio(filepath)
        self.start_update_highlight_words()
    
    def set_audio_for_flashcard(self):
        if self.audio_player.isAudioAvailable():
            pos = self.audio_player.position()
            dur = self.audio_player.duration()
            start_time = self.get_start_time(pos,5000)
            end_time = self.get_end_time(pos,5000,dur)
            self.current_flashcard_audio = {"start":start_time,"end":end_time}
            if self.current_other_settings["dark_theme"]:
                self.top_right_pane.add_sound_action.setIcon(QIcon(os.path.join("src", "img", "sound_dark.png")))
            else:
                self.top_right_pane.add_sound_action.setIcon(QIcon(os.path.join("src", "img", "sound.png")))
        else:
            self.current_flashcard_audio = {"start":None,"end":None}
            if self.current_other_settings["dark_theme"]:
                self.top_right_pane.add_sound_action.setIcon(QIcon(os.path.join("src", "img", "no_sound_dark.png")))
            else:
                self.top_right_pane.add_sound_action.setIcon(QIcon(os.path.join("src", "img", "no_sound.png")))
            self.display_msg("sorry","No Audio Found")

    def add_flashcard_to_db(self):
        audio_start = self.current_flashcard_audio["start"]
        audio_end = self.current_flashcard_audio["end"]
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
            img_source = image['src']
            image.decompose()
        except:
           img_source = ""

        if front_text == "\n":
            self.display_msg("Oops!","No text was found for the Flashcard.")
            return 0
        if back_text == "\n" and image is None:
            self.display_msg("Oops!","No text or images were found for back of the Flashcard.")
            return 0

        flashcard = {
            "front":str(front),
            "back":str(back),
            "back_image":img_source,
            "audio_start":audio_start,
            "audio_end":audio_end
            }
        try:
            self.db.add_flashcard_to_db(flashcard,self.current_user["id"])
        except:
            logging.exception("adding flashcard to db")
        self.top_right_pane.flash_front.clear()
        self.top_right_pane.flash_back.clear()
        self.current_flashcard_audio = {"start":None,"end":None}
        self.top_right_pane.add_sound_action.setIcon(QIcon(os.path.join("src","img","")))
        if self.current_other_settings["dark_theme"]:
            self.top_right_pane.add_sound_action.setIcon(QIcon(os.path.join("src", "img", "no_sound_dark.png")))
        else:
            self.top_right_pane.add_sound_action.setIcon(QIcon(os.path.join("src", "img", "no_sound.png")))


    def download_flashcards(self): #this creates anki deck
        filepath = QFileDialog.getSaveFileName(self, 'Download Anki Deck','',"Anki File (*.apkg)")[0]
        if filepath == "":
            return 0
        deck_name = self.get_filename_from_path(filepath)

        flashcards_list = self.db.get_flashcards_from_db(self.current_user["id"])

        if flashcards_list == []:
            self.display_msg("Oops!", "There are no cards to make an anki deck with.\nUse the flashcard generator in the top right corner to make some.")
            return 0
        try:
            self.anki_gen.start_everything(flashcards_list,deck_name,filepath)
            self.db.delete_all_flashcards_for_user(self.current_user["id"])
            self.display_msg("Ok",f"The anki deck was successfully created and saved in this location: \n {filepath}")
        except Exception as e:
            self.display_msg("oh dear",f"there was an error trying to export your flashcards.\nWhy don't you try again? \n\nError Message: {e}")
            logging.exception("while trying to export flashcards")
        

    
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
            if self.current_other_settings["dark_theme"]:
                self.left_pane.play_action.setIcon(QIcon(os.path.join("src", "img", "play_dark.png")))
            else:
                self.left_pane.play_action.setIcon(QIcon(os.path.join("src", "img", "play.png")))
        if state == 0 or state == 2:
            self.audio_player.play()
            if self.current_other_settings["dark_theme"]:
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
        extension_to_remove = self.get_file_extension_from_path(filename)
        name = filename.replace(extension_to_remove, '')
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
    
    def new_blank_document(self):
        self.left_pane.browser.clear()
        self.audio_player.setMedia(QMediaContent(None))

    def open_recent_file_window(self):
        self.recent_files_widget.clear()
        self.recent_files_widget.itemClicked.connect(self.recent_file_item_clicked)
        self.recent_files_widget.setWindowTitle("Recent Files")
        self.recent_files_widget.resize(400,500)
        self.recent_files = self.db.get_recent_files(self.current_user["id"])
        if self.recent_files:
            for filepath in self.recent_files:
                name = self.get_filename_from_path(filepath[1])
                date = filepath[2][:16]
                self.recent_files_widget.addItem(f"{date} -- {name}")
        else:
            self.recent_files_widget.addItem("You haven't opened or saved any files recently")
        self.recent_files_widget.move(QtGui.QCursor.pos())
        self.recent_files_widget.show()
    
    def recent_file_item_clicked(self):
        file_clicked = self.recent_files[self.recent_files_widget.currentIndex().row()][1]
        self.open_file(file_clicked)
        self.recent_files_widget.hide()
    
    def delete_user(self):
        name = self.current_user["name"]
        if name == "default_user":
            self.display_msg("hmmm","You are not allowed to delete this user.")
            return
        answer = QMessageBox.question(self,"Sure?",f'Are you are you want to delete "{name}"?', QMessageBox.Yes | QMessageBox.No)
        if answer == QMessageBox.Yes:
            try:
                self.db.delete_user(self.current_user["id"])
                self.settings.user_tab.user_combobox.blockSignals(True)
                self.current_user = {"id":1,"name":"default_user"}
                self.run_start_up_settings()
                self.load_settings_to_settings_page()   
                self.settings.user_tab.user_combobox.blockSignals(False)
            except Exception as e:
                logging.exception("while trying to delete user")
                self.display_msg("oh crumbs..",f"error while trying to delete user.\n{e}")
        self.settings.raise_()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    mainApp = MainWindow()
    mainApp.setWindowTitle("Langsoft")
    mainApp.setWindowIcon(QtGui.QIcon(os.path.join(os.getcwd(),"src","img","langsoft.png")))
    mainApp.showMaximized()
    try:
        sys.exit(app.exec_())
    except Exception as e:
        logging.exception("app crashed")
