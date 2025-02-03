import os
import shutil
import webbrowser
import logging
from logging.handlers import TimedRotatingFileHandler
import socket
import psutil

# create a logger named fLogger
logger = logging.getLogger("fLogger")
# set logging level
logger.setLevel(logging.INFO)
# create a log handler
# backupCount=100 means, only latest 100 log files will be retained and older log files will be deleted
# interval=1 means the log rotation interval is 1
# when='d' means the rotating interval will be in terms of days
# so logs will be rotated every 24 hours(1 day) in this example
# Following are the options for 'when' parameter
# S - Seconds, M - Minutes, H - Hours, D - Days, 
# midnight - roll over at midnight, W{0-6} - roll over on a certain day; 0 - Monday
fileHandler = TimedRotatingFileHandler(
    r"\\trt1corp\SERVICE-DESK-STEFANINI\Logs_salas_sessao\Logs.log", backupCount=30, when='D', interval=1)
# use namer function of the handler to keep the .log extension at the end of the file name
fileHandler.namer = lambda name: name.replace(".log", "") + ".log"
# create a log formatter object and assign to the log handler
logFormatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt='%d/%m/%Y %H:%M')
fileHandler.setFormatter(logFormatter)
# add log handler to logger object
logger.addHandler(fileHandler)

host = socket.gethostname()
ip = socket.gethostbyname(socket.gethostname())

logger.info(f"Nome da máquina:{host} - IP:{ip}")

#Teste a conexão a internet
try:
  host = socket.gethostbyname('www.google.com')
  s = socket.create_connection((host, 80), 2)
  #logger.info(f"OK - internet")
except:
    pass
    logger.error(f"Sem acesso a internet")

#Verifica o percentual utilizado do HD
disk = psutil.disk_usage('/')

if disk.percent > 90:
    logger.warning(f"Utilizaçao do disco: {disk.percent}% - VERIFICAR")
else:
    pass
    logger.info(f"OK - Uso do disco: {disk.percent}%") 

#Abre o Shodo
try:
   os.startfile("C:/Program Files (x86)/Shodo/shodo.exe")
   #logger.info(f"OK - Shodo")
except:
    pass
    logger.warning(f"Não abriu o Shodo")

procura_cookies = 'cookies.sqlite'
procura_preferencias = 'content-prefs.sqlite'
procura_formularios = 'formhistory.sqlite'
procuras_locais = 'places.sqlite'

path_firefox = r"C:/Users/pleno.pje/AppData/Roaming/Mozilla/Firefox/Profiles"   

for dirPath, dirNames, fileNames in os.walk(path_firefox):
     for i in fileNames:
        #Limpa cookies do Firefox
        try:
          if procura_cookies in i:
             os.remove(os.path.join(dirPath, i))
             #logger.info(f"OK - cookies") 
        except:
            pass
            logger.warning(f"Não apagou os Cookies do Firefox")
        #Limpa as preferência do Firefox
        try:
          if procura_preferencias in i:
             os.remove(os.path.join(dirPath, i))
             #logger.info(f"OK - preferências")
        except:
            pass
            logger.warning(f"Não apagou os Preferências do Firefox")
        #Limpa formulários do Firefox
        try:
          if procura_formularios in i:
             os.remove(os.path.join(dirPath, i))
             #logger.info(f"OK - formulários")
        except:
            pass
            logger.warning(f"Não apagou os Formulários do Firefox")
        #Limpa procuras locais do Firefox
        try: 
          if procuras_locais in i:
             os.remove(os.path.join(dirPath, i))
             #logger.info(f"OK - locais")
        except:
            pass
            logger.warning(f"Não apagou os Locais do Firefox")

#Limpa Cache do Chrome
try:
   shutil.rmtree('C:/Users/pleno.pje/AppData/Local/Google/Chrome/User Data/Default/Cache')
   shutil.rmtree('C:/Users/pleno.pje/AppData/Local/Google/Chrome/User Data/Default/Code Cache')
   shutil.rmtree('C:/Users/pleno.pje/AppData/Local/Google/Chrome/User Data/Default/DawnCache')
   #logger.info(f"OK - Cache Chrome")
except:
    pass
    logger.warning(f"Não apagou o Cache do Chrome")

# Limpa os cookies no Windows
try:
   os.system("RunDll32.exe InetCpl.cpl,ClearMyTracksByProcess 8")
   #logger.info(f"OK - Cache Windows")
except:
   pass
   logger.warning(f"Não apagou os Cookies do Windows")

try:
  firefox = webbrowser.Mozilla("C:\\Program Files\\Mozilla Firefox\\firefox.exe")
  firefox.open('https://pje.trt1.jus.br/segundograu/login.seam')
  firefox.open('http://www.google.com')
  firefox.open("https://accounts.google.com/v3/signin/identifier?dsh=S2130936901%3A1676658346671047&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&hd=trt1.jus.br" #Quebra de linha, continua embaixo
  "/n&ltmpl=default&rip=1&sacu=1&service=mail&flowName=GlifWebSignIn&flowEntry=ServiceLogin&ifkv=AWnogHdt1CJeQKJ_4QnjVBzU2EY89uFDpC0N3OLgTliTOP-Z61RRfLzJ2FuLbaI9FNy3kqTfl6kCTA")  
  firefox.open('https://127.0.0.1:9000/#bemvindo')
  #logging.info(f"OK - Firefox")
except:
   pass
   logger.warning(f"Não abriu o Firefox")

#Abre o Zoom
try:
   os.startfile("C:/Program Files (x86)/Zoom/bin/Zoom.exe")
   #logger.info(f"OK - Zoom")
except:
    pass
    logger.warning(f"Não abriu o Zoom")
