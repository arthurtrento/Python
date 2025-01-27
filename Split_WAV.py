from pydub import AudioSegment
import math
import os

# Carregar o arquivo .wav
audio = AudioSegment.from_wav(r'G:/Other computers/Meu computador/Python/TRT/Qualidade chamados/Avaliacoes/Audio_ligacoes/sd3.wav')

# Dividir a duração total do arquivo em 10 partes
duration_in_ms = len(audio)
part_duration = math.ceil(duration_in_ms / 10)  # Duração de cada parte

# Criar pasta para salvar as partes
output_folder = "partes_audio"
os.makedirs(output_folder, exist_ok=True)

# Dividir o arquivo em 10 partes
for i in range(10):
    start_time = i * part_duration
    end_time = min((i + 1) * part_duration, duration_in_ms)
    
    part = audio[start_time:end_time]
    
    # Salvar a parte como novo arquivo .wav
    part.export(f"{output_folder}/parte_{i + 1}.wav", format="wav")

print("Divisão concluída!")