import whisper

model = whisper.load_model("base")

audio = whisper.load_audio(r'G:/Other computers/Meu computador/Python/TRT/Qualidade chamados/Avaliacoes/Audio_ligacoes/sd.wav')
audio = whisper.pad_or_trim(audio)

mel = whisper.log_mel_spectrogram(audio).to(model.device)

_, probs = model.detect_language(mel)
print(f"Detected language: {max(probs, key=probs.get)}")

options = whisper.DecodingOptions()
result = whisper.decode(model, mel, options)

print(result.text)