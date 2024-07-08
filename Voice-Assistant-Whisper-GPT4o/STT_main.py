import os
import requests
import soundfile as sf
import speech_recognition as sr
from io import BytesIO
from dotenv import load_dotenv
from Silero_VAD import silero_vad_main

load_dotenv()

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
    try:
        response = requests.post(model, headers=headers, data=audio_data)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error in STT API request: {e}")
        return None

def STT_rec_voice(headers, model):
    audio_data = capture_audio_from_microphone()
    vad_audio_data = silero_vad_main(audio_data)
    if vad_audio_data is None:
        return None
    response = STT_AudioData(vad_audio_data, model, headers)
    return response

def STT_audio_file(file_name, model, headers):
    try:
        with open(file_name, "rb") as f:
            audio_data = f.read()
        vad_audio_data = silero_vad_main(audio_data)
        if vad_audio_data is None:
            return None
        response = STT_AudioData(vad_audio_data, model, headers)
        return response
    except IOError as e:
        print(f"Error reading audio file: {e}")
        return None

def main():
    whisper = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
    token = "Bearer " + os.environ['HuggingFaceToken']
    headers = {"Authorization": token}
    
    model = whisper
    
    input_option = int(input("Enter Your Input Option:\n1---Audio File\n2---From Microphone\n"))
    
    if input_option == 1:
        file_name = input("Enter the path to your audio file: ")
        response = STT_audio_file(file_name, model, headers)
        if response:
            print("TEXT:", response)
        else:
            print("Failed to process audio file.")
        
    elif input_option == 2:
        response = STT_rec_voice(headers, model)
        if response:
            print("TEXT:", response)
        else:
            print("Failed to process microphone input.")
    else:
        print("Select correct option")

if __name__ == "__main__":
    main()
