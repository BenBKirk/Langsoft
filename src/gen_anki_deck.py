"""
This is responsible for making and saving the anki deck
"""
import genanki
from mimetypes import guess_extension
from urllib.request import urlretrieve, urlopen
import uuid
import os 
import shutil

class AnkiDeckGenerator:
  def __init__(self):
    super().__init__()
    self.media_path_list = []
    style = """
    .card {
    font-family: times;
    font-size: 30px;
    text-align: center;
    color: black;
    background-color: white;
    }
    .card1 { background-color:Lavender }
    """
    self.my_model = genanki.Model(
      1607392328,
      'Langsoft',
      fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
        {'name': 'MyMedia'},
      ],
      templates=[
        {
          'name': 'Card 1',
          'qfmt': '{{Question}}',
          'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}{{MyMedia}}',
        },
     ],
     css=style)

  def start_everything(self,flashcard_list,deckName,filePath):
    self.my_deck = genanki.Deck(
      2059400110,
      deckName)
    
    working_dir = os.getcwd()
    images_dir = os.path.join(working_dir,"flashcard_images")

    if os.path.exists(images_dir):
      shutil.rmtree(images_dir)
    os.mkdir(images_dir)

    for card in flashcard_list:
      self.make_card(card[2],card[3],card[4])

    my_package = genanki.Package(self.my_deck) 
    my_package.media_files = self.media_path_list
    my_package.write_to_file(filePath)
    

  def make_card(self,front,back,img):
    if img != "":
      full_path, local_path = self.download_image(img)
  
      my_card = genanki.Note(
        model=self.my_model,
        fields=[front,back,'<img src="' + local_path + '">'])
      self.media_path_list.append(full_path)
    else:
      my_card = genanki.Note(
        model=self.my_model,
        fields=[front,back,""])

    self.my_deck.add_note(my_card)
  
  def download_image(self, img):
    remote_file = urlopen(img).info()
    extension = guess_extension(remote_file['content-type'])
    unique_name = str(uuid.uuid4()) + str(extension)
    full_path = os.path.join(os.path.join(os.getcwd(),"flashcard_images",unique_name))
    urlretrieve(img,full_path)
    return [full_path,unique_name]











