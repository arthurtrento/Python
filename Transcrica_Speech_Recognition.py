import os
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks

# Função para dividir o áudio em partes de 30 segundos
def divide_audio_in_chunks(audio_path, chunk_length_ms=30000):
    # Carregar o áudio
    audio = AudioSegment.from_wav(audio_path)
    # Dividir em partes de 30 segundos
    chunks = make_chunks(audio, chunk_length_ms)
    return chunks

# Função para transcrever um pedaço de áudio
def transcribe_audio_chunk(audio_chunk, recognizer, language='en-US'):
    # Salvar o pedaço em um arquivo temporário
    temp_chunk_path = "temp_chunk.wav"
    audio_chunk.export(temp_chunk_path, format="wav")
    
    # Ler o áudio com o recognizer
    with sr.AudioFile(temp_chunk_path) as source:
        audio_data = recognizer.record(source)
        try:
            # Transcrever o áudio
            return recognizer.recognize_google(audio_data, language=language)
        except sr.UnknownValueError:
            return "[Inaudível]"
        except sr.RequestError as e:
            return f"[Erro no serviço de reconhecimento de fala: {str(e)}]"

# Função principal para processar arquivos de uma pasta
def process_audio_folder(folder_path, language='en-US'):
    # Inicializar o reconhecedor de fala
    recognizer = sr.Recognizer()

    # Verificar cada arquivo na pasta
    for filename in os.listdir(folder_path):
        if filename.endswith(".wav"):
            # Caminho completo do arquivo
            audio_path = os.path.join(folder_path, filename)
            print(f"Processando arquivo: {filename}")
            
            # Dividir o áudio em pedaços
            audio_chunks = divide_audio_in_chunks(audio_path)
            
            # Criar arquivo de transcrição
            transcription_file = os.path.join(folder_path, f"{filename[:-4]}.txt")
            with open(transcription_file, "w") as f:
                for i, chunk in enumerate(audio_chunks):
                    #print(f"{audio_chunks}\n")
                    transcription = transcribe_audio_chunk(chunk, recognizer, language)
                    f.write(f"{transcription}\n")
            print(f"Transcrição salva em: {transcription_file}")

# Caminho para a pasta com os arquivos WAV
folder_path = "G:/Other computers/Meu computador/Python/TRT/Qualidade chamados/Avaliacoes/Audio_ligacoes/Audios"
# Executar o processamento
process_audio_folder(folder_path, language='pt-BR')  # Altere para o idioma desejado
