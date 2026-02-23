import whisper
import librosa
import io
from fastapi import UploadFile

model = whisper.load_model("base")

def text_from_audio(file: UploadFile) -> str:
    audio_bytes = io.BytesIO(file.file.read())
    y, sr = librosa.load(audio_bytes, sr=16000,mono=True)
    result = model.transcribe(y, language="en")
    return result["text"]
