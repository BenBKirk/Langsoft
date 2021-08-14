"""
This is responsible for making and saving the anki deck
"""
import genanki
from mimetypes import guess_extension
from urllib.request import urlretrieve, urlopen
import uuid
import os 
import shutil
import subprocess as sp

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
        {'name': 'audio'},
        {'name': 'image'},
      ],
      templates=[
        {
          'name': 'Card 1',
          'qfmt': '{{Question}}{{audio}}',
          'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}{{image}}',
        },
     ],
     css=style)

  def start_everything(self,flashcard_list,deckName,filePath):
    self.my_deck = genanki.Deck(
      2059400110,
      deckName)
    
    working_dir = os.getcwd()
    images_dir = os.path.join(working_dir,"flashcard_images")
    audio_dir = os.path.join(working_dir,"flashcard_audio")

    if os.path.exists(images_dir):
      shutil.rmtree(images_dir)
    os.mkdir(images_dir)

    if os.path.exists(audio_dir):
      shutil.rmtree(audio_dir)
    os.mkdir(audio_dir)

    for card in flashcard_list:
      self.make_card(card[2],card[3],card[4],card[5],card[6],card[7])

    my_package = genanki.Package(self.my_deck) 
    my_package.media_files = self.media_path_list
    my_package.write_to_file(filePath)
    

  def make_card(self,front,back,img,audio_path,audio_start,audio_end):

    the_fields = [front,back]

    if audio_start is not None:
      full_audio_path, local_audio_path = self.create_audio_clip(audio_path,audio_start,audio_end)
      self.media_path_list.append(full_audio_path)
      the_fields.append(f"[sound:{local_audio_path}]")
    else:
      the_fields.append("")#"[sound:]")

    if img != "":
      full_img_path, local_img_path = self.download_image(img)
      self.media_path_list.append(full_img_path)
      the_fields.append('<img src="' + local_img_path + '">')
    else:
      the_fields.append("")#"img src=''>")

    my_card = genanki.Note(
      model = self.my_model,
      fields = the_fields
      )

    self.my_deck.add_note(my_card)
  
  def download_image(self, img):
    remote_file = urlopen(img).info()
    extension = guess_extension(remote_file['content-type'])
    unique_name = str(uuid.uuid4()) + str(extension)
    full_path = os.path.join(os.getcwd(),"flashcard_images",unique_name)
    urlretrieve(img,full_path)
    return [full_path,unique_name]

  def create_audio_clip(self,audio_path,start,end):
    unique_name = str(uuid.uuid4()) + ".mp3"
    full_path = os.path.join(os.getcwd(),"flashcard_audio",unique_name)
    start = start // 1000
    end = end // 1000

    process = sp.Popen(#["ffmpeg", "-i", "5a Perbandingan Ambon dan Jawa.mp3", "-ss", "100", "-to", "110", "output.mp3"])
      [
        "ffmpeg",
        "-i", audio_path,
        "-ss", str(start),
        "-to", str(end),
        "-c", "copy",
        full_path
      ],
      stdout=sp.PIPE,
      stderr=sp.PIPE
    )
    stdout, stderr = process.communicate()
    # print(stdout.decode(), stderr.decode())
    return [full_path, unique_name]










