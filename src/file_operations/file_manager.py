
import os
from PyQt5.QtWidgets import QFileDialog

class FileManager:
    """
    responsible for reading and writing files
    """
    def __init__(self):
        self.supported_text_files = [".txt", ".html", ".docx", ".pdf"]
        self.supported_audio_files = [".mp3", ".wav", ".flac"]
    
    def open_files(self):
        files = self.prompt_user_for_files()
        sorted_files = self.sort_file_selection(files)
        print(sorted_files)

    def prompt_user_for_files(self):
        files = QFileDialog.getOpenFileNames() #("open a file", "", "All Files (*);;Text Files (*.txt);;Audio Files (*.mp3)")
        if files:
            return files[0]
    
    def sort_into_audio_and_text_files(self,files):
        text_files_found = []
        audio_files_found = []
        for file in files:
            extension = self.get_file_extension_from_path(file)
            if extension in self.supported_text_files:
                text_files_found.append(file)
            elif extension in self.supported_audio_files:
                audio_files_found.append(file)
            else:
                print(f"File type not supported. {file}")
        return text_files_found, audio_files_found
    
    def sort_into_pairs(self,text_files_found, audio_files_found):
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
        
    def sort_file_selection(self,files):
        text_files_found, audio_files_found = self.sort_into_audio_and_text_files(files)
        audio_text_pairs = self.sort_into_pairs(text_files_found, audio_files_found)
        return audio_text_pairs
    
    def search_for_matching_audio(self,folder,text_file):
        for file in os.listdir(folder):
            if self.get_file_name_from_path(file) == self.get_file_name_from_path(text_file):
                if self.get_file_extension_from_path(file) in self.supported_audio_files:
                    return file
        return None
    
    def search_for_matching_text(self,folder,audio_file):
        for file in os.listdir(folder):
            if self.get_file_name_from_path(file) == self.get_file_name_from_path(audio_file):
                if self.get_file_extension_from_path(file) in self.supported_text_files:
                    return file
        return None

    def pair_matching_audio(self,text_file,list_of_audio_files):
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


        



    # def is_supported_audio_file(self,file):
    #     if file in self.sup
    #     pass

    # def is_supported_text_file(self,file):
    #     pass
