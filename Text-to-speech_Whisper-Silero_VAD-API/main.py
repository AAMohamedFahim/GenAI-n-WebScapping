import os
import requests
import soundfile as sf
import speech_recognition as sr
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from io import BytesIO
from dotenv import load_dotenv
from Silero_VAD import silero_vad_main

load_dotenv()

app = FastAPI()

# class STTResponse(BaseModel):
#     text: str

def capture_audio_from_microphone():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        print("Audio captured successfully.")
    audio_data = audio.get_wav_data()
    return audio_data

def STT_AudioData(audio_data, model, headers):
    response = requests.post(model, headers=headers, data=audio_data)
    return response.json()
# @app.post("/stt/microphone", response_model=STTResponse)
def stt_from_microphone():
    whisper = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
    token = "Bearer " + os.getenv('HuggingFaceToken')
    headers = {"Authorization": token}
    
    audio_data = capture_audio_from_microphone()
    vad_audio_data = silero_vad_main(audio_data)
    response = STT_AudioData(vad_audio_data, whisper, headers)
    return {"text": response}

@app.post("/stt/audiofile")
def stt_from_audiofile(file: UploadFile = File(...)):
    whisper = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
    token = "Bearer " + os.getenv('HuggingFaceToken')
    headers = {"Authorization": token}
    
    audio_data = file.file.read()
    vad_audio_data = silero_vad_main(audio_data)
    response = STT_AudioData(vad_audio_data, whisper, headers)
    return {"text": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
