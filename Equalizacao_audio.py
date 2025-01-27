from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.effects import normalize
from datetime import date, datetime


begin = datetime.now()
print('Hora de início:',begin)

# Carregar o arquivo .wav
#audio = AudioSegment.from_wav(f'G:/Other computers/Meu computador/Python/TRT/Qualidade chamados/Avaliacoes/Audio_ligacoes/Audios/{file}')   #casa
audio = AudioSegment.from_wav(f'G:/Outros computadores/Meu computador/Python/TRT/Avaliacao_qualidade/Avaliacao_audios/20241022_073229-21996074070-800-1729593124.324457.wav')  #TRT
#audio = AudioSegment.from_wav(f'C:/Python/Avaliacao_qualidade/Avaliacao_audios/Calls/file.wav')  #SERVER


# Divide o áudio em segmentos, removendo momentos de silêncio
chunks = split_on_silence(
    audio,
    min_silence_len=500,   # Mínimo de milissegundos considerados como silêncio
    silence_thresh=-40,     # Limite de volume para considerar silêncio
    keep_silence=200               # Adiciona um pouco de silêncio entre segmentos (opcional)
)

# Junta os segmentos em um único áudio, sem silêncio
processed_audio = AudioSegment.empty()
for chunk in chunks:
    processed_audio += chunk

# Converte para mono e 16kHz
#audio = processed_audio.set_frame_rate(8000).set_channels(1)

#Aumenta o volume do áudio em 10db
#audio = audio + 10
audio = processed_audio + 10

#Normaliza o volume
audio = normalize(audio)

final_audio = (f'G:/Outros computadores/Meu computador/Python/TRT/Avaliacao_qualidade/Avaliacao_audios/final_audio.wav')  #TRT

audio.export(final_audio, format="wav")

end= datetime.now()
print('Hora do término',end)

print(end - begin)