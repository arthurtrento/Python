import whisper
from datetime import datetime


begin = datetime.now()

model = whisper.load_model("medium")
#result = model.transcribe(r'G:/Outros computadores/Meu computador/Python/TRT/Qualidade chamados/Avaliacoes/Audio_ligacoes/sd3.wav') 

result = model.transcribe(r'G:/Other computers/Meu computador/Python/TRT/Qualidade chamados/Avaliacoes/Audio_ligacoes/Audios/sd4.wav')

print(result["text"])

end = datetime.now()

print(end - begin)