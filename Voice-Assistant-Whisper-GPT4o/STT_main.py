import os
import streamlit as st
import requests
import soundfile as sf
import speech_recognition as sr
from io import BytesIO
# from dotenv import load_dotenv
from Silero_VAD import silero_vad_main

# load_dotenv()

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

def STT_rec_voice(headers, model):
    audio_data = capture_audio_from_microphone()
    vad_audio_data = silero_vad_main(audio_data)
    response = STT_AudioData(vad_audio_data, model, headers)
    return response

# def STT_audio_file(file_name,model,headers):
#     with open(file_name, "rb") as f:
#             audio_data = f.read()
#     vad_audio_data = silero_vad_main(audio_data)
#     response = STT_AudioData(vad_audio_data, model, headers)
#     return response

def main():
    # MMS = "https://api-inference.huggingface.co/models/facebook/mms-1b-all"
    whisper = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
    token = "Bearer " + st.secrets['HF_TOKEN']
    headers = {"Authorization": token}
    
    # model_selection = int(input("Select Your Model:\n1---Whisper\n2---MMS\n"))
    # if model_selection == 1:
    model = whisper
    # model = MMS
    # elif model_selection == 2:
    # else:
    #     print("Select correct option")
    #     return
        
    input_option = int(input("Enter Your Input Option:\n1---Audio File\n2---From Microphone\n"))
    
    if input_option == 1:
        file_name = "tam-voice.ogg"
        with open(file_name, "rb") as f:
            audio_data = f.read()
        vad_audio_data = silero_vad_main(audio_data)
        response = STT_AudioData(vad_audio_data, model, headers)
        print("TEXT:", response)
        
    elif input_option == 2:
        response = STT_rec_voice(headers, model)
        print("TEXT:", response)
    else:
        print("Select correct option")

if __name__ == "__main__":
    main()
