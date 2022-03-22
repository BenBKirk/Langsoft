
import os
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import fitz
import mammoth

class FileManager:
    """ responsible for reading, writing and converting files."""
    def __init__(self):
        self.supported_text_files = [".txt", ".html", ".docx", ".pdf"]
        self.supported_audio_files = [".mp3", ".wav", ".flac"]
    
    def prompt_user_for_files_to_open(self):
        """ prompts user for files and sorts them, returning a list of lists """
        files = QFileDialog.getOpenFileNames()[0] #("open a file", "", "All Files (*);;Text Files (*.txt);;Audio Files (*.mp3)")
        if files is not None:
            sorted_files = self.sort_chosen_files(files)
            return sorted_files
        else:
            return None
   
    def load_audio_file_to_audio_player(self,path,audio_player=None):
        if audio_player:
            self.audio_player = audio_player
        else:
            print("no audio player specified")

    def read_text_file(self,path):
        """reads from the file and returns the txt html and bool"""
        file_type = self.get_file_extension_from_path(path)
        if file_type == ".txt":
            with open(path, "r") as f:
                return f.read(),False
        else: # will be converted into html if needed
            text = self.convert_non_txt_format_to_html(file_type,path)
            if text:
                return text, True
            else:
                print(f"could not open file {path}\n Not a supported file type")
    
    def convert_non_txt_format_to_html(self,file_type,path):
        supported_html_files = [".html", ".htm"]
        if file_type in supported_html_files: 
            with open(path, "r", encoding='utf8', errors='ignore') as f:
                text = f.read()
                return text
        elif file_type == ".docx":
            return self.convert_docx_to_html(path)
        elif file_type == ".pdf":
            return self.convert_pdf_to_html(path)
        else:
            return None

    def convert_pdf_to_html(self,path):
        with fitz.open(path, 'r', encoding='utf8', errors='ignore') as doc:
            pages = []
            for i in range(doc.page_count()):
                pages.append(doc.load_page(i).get_text("html"))
            return "\n".join(pages)

    def convert_docx_to_html(self,path):
        with open(path, 'rb') as docx_file:
            result = mammoth.convert_to_html(docx_file)
            return result.value
     
    def sort_chosen_files(self,files):
        """ returns list of lists like this [[example.txt, example.mp3], [example2.txt, example2.mp3]] """
        text_files_found, audio_files_found = self.sort_into_audio_and_text_files(files)
        audio_text_pairs = self.sort_into_pairs(text_files_found, audio_files_found)
        return audio_text_pairs
    
    def sort_into_audio_and_text_files(self,files):
        """return two lists, one for audio and one for text"""
        text_files_found = []
        audio_files_found = []
        for file in files:
            extension = self.get_file_extension_from_path(file)
            if extension in self.supported_text_files:
                text_files_found.append(file)
            elif extension in self.supported_audio_files:
                audio_files_found.append(file)
            else:
                QMessageBox.warning(None, "File Type Not Supported", f"{file} is not a supported file type")
                print(f"File type not supported. {file}")
        return text_files_found, audio_files_found
    
    def sort_into_pairs(self,text_files_found, audio_files_found):
        """sorts text files and audio files into pairs and searches for any missing audio or text in the same folder"""
        audio_text_pairs = []
        for text_file in text_files_found:
            matching_audio = self.pair_matching_audio(text_file,audio_files_found)
            if matching_audio == None:
                matching_audio = self.search_for_matching_audio(self.get_dir_from_path(text_file),text_file)
                if matching_audio == None:
                    print(f"No matching audio found for {text_file}")
            else:
                audio_files_found.remove(matching_audio)
            audio_text_pairs.append((text_file,matching_audio)) # note the audio here could be none
        for audio_file in audio_files_found:
            matching_text = self.search_for_matching_text(self.get_dir_from_path(audio_file),audio_file)
            if matching_text == None:
                print(f"No matching text found for {audio_file}")
            else:
                audio_text_pairs.append((matching_text,audio_file)) # note the text here should never be none
        return audio_text_pairs
        
    def search_for_matching_audio(self,folder,text_file):
        for file in os.listdir(folder):
            if self.get_file_name_from_path(file) == self.get_file_name_from_path(text_file):
                if self.get_file_extension_from_path(file) in self.supported_audio_files:
                    return os.path.join(folder,file)
        return None
    
    def search_for_matching_text(self,folder,audio_file):
        for file in os.listdir(folder):
            if self.get_file_name_from_path(file) == self.get_file_name_from_path(audio_file):
                if self.get_file_extension_from_path(file) in self.supported_text_files:
                    return os.path.join(folder,file)
        return None

    def pair_matching_audio(self,text_file,list_of_audio_files):
        """find selected audio file with the same name as the audio file."""
        name = self.get_file_name_from_path(text_file)
        for audio_file in list_of_audio_files:
            if self.get_file_name_from_path(audio_file) == name:
                return audio_file
        return None

    def get_file_extension_from_path(self,path):
        parts = os.path.splitext(path)
        if len(parts) == 2:
            return parts[1]

    def get_file_name_from_path(self,path):
        return os.path.basename(path).replace(self.get_file_extension_from_path(path), "")
    
    def get_dir_from_path(self,path):
        return os.path.dirname(path)


        
# Here's [Python3] code for replacing HTML images specified with URLs to base64:
# import base64
# import mimetypes
# import requests
# from bs4 import BeautifulSoup

# def make_html_images_inline(html: str) -> str:
#     soup = BeautifulSoup(html, 'html.parser')

#     for img in soup.find_all('img'):
#         img_src = img.attrs['src']

#         if not img_src.startswith('http'):
#             continue

#         mimetype = mimetypes.guess_type(img_src)[0]
#         img_b64 =  base64.b64encode(requests.get(img_src).content)

#         img.attrs['src'] = \
#             "data:%s;base64,%s" % (mimetype, img_b64.decode('utf-8'))

#     return str(soup)
