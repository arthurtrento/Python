import logging
from pydub import AudioSegment
import os
import re


#Install FFMPEG on Windows: https://phoenixnap.com/kb/ffmpeg-windows 
AudioSegment.converter = "C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe" 
AudioSegment.ffmpeg = "C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe"
AudioSegment.ffprobe ="C:\\Program Files\\ffmpeg\\bin\\ffprobe.exe"


def convert(file):

  print(file) 
  logging.info(f"{file}")
  dirname = os.path.abspath("C:\\Music") #Alterar a pasta, caso necessário
  fullpath = dirname + r"\\" + file + ".webm"
  try:
      songWebm = AudioSegment.from_file(fullpath, "webm")
      print("Success Imported")
      logging.info("Success Imported")
  except: 
      print("Error Imported")
      logging.info("Error Imported")
      pass
  
  substExt = re.sub('.webm', '.flac', fullpath)   
  fullpathFlac = re.sub(r'C:\\Music', r'C:\\Music-FLAC', substExt) #Alterar a pasta, caso necessário 
  #songFlac = os.listdir("C:\\Music-FLAC")
  try:
      songWebm.export(fullpathFlac, format="flac", bitrate="2000k", tags={"album": file, "artist": file})
      print("Success Converted")
      logging.info("Success Converted")
      os.remove(os.path.join("c:\\Music", fullpath))
      print("-----------------------------------------------------------")
      logging.info("-----------------------------------------------------------")
  except:  
      print("Error convert") 
      logging.info("Error convert") 
      print("-----------------------------------------------------------")
      logging.info("-----------------------------------------------------------")
      pass
      try:
        os.remove(os.path.join("c:\\Music", fullpath))
      except:
        pass