import streamlit as st
import requests
import os
# from dotenv import load_dotenv
import speech_recognition as sr

# load_dotenv()

def STT_AudioFile(file, model, headers):
    data = file.read()
    response = requests.post(model, headers=headers, data=data)
    return response.json()

def STT_rec_voice(headers, model):
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        st.write("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        st.write("Audio captured successfully.")

    audio_wav = audio.get_wav_data()
    response = requests.post(model, headers=headers, data=audio_wav)
    return response.json()

def main():
    st.title("Speech-to-Text Interface")
    
    MMS = "https://api-inference.huggingface.co/models/facebook/mms-1b-all"
    whisper = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
    token = "Bearer " + "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"
    headers = {"Authorization": token}
    
    model_selection = st.selectbox("Select Your Model", ["Whisper", "MMS"])
    
    if model_selection == "Whisper":
        model = whisper
    elif model_selection == "MMS":
        model = MMS
    
    input_option = st.selectbox("Enter Your Input Option", ["Audio File", "From Microphone"])
    
    if input_option == "Audio File":
        file = st.file_uploader("Upload Audio File", type=["ogg", "wav", "mp3"])
        if file is not None:
            if st.button("Transcribe"):
                response = STT_AudioFile(file, model, headers)
                st.write("TEXT: ", response)
    
    elif input_option == "From Microphone":
        if st.button("Transcribe"):
            response = STT_rec_voice(headers, model)
            st.write("TEXT: ", response)

if __name__ == "__main__":
    main()
