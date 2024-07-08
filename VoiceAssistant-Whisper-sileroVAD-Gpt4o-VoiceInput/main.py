import streamlit as st
from GPT40_llm import LLM_response
from STT_main import STT_rec_voice
from TTS_main import text_to_speech
import os
from dotenv import load_dotenv
import base64


load_dotenv()

whisper = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
token = "Bearer " + os.environ['HuggingFaceToken']
headers = {"Authorization": token}

def get_audio_player(audio_data):
    audio_base64 = base64.b64encode(audio_data).decode('utf-8')
    audio_tag = f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_base64}" controls></audio>'
    return audio_tag

def main():
    st.title("Voice Assistant")

    st.write("Click the button below to start recording your voice input.")

    if st.button("Record Voice Input"):
        with st.spinner("Listening..."):
            STT_response = STT_rec_voice(headers, whisper)
        
        prompt = STT_response['text']
        st.write(f"You said: {prompt}")

        with st.spinner("Generating response..."):
            llm_res = LLM_response(prompt)
        
        st.write(f"Assistant's response: {llm_res}")

        with st.spinner("Converting text to speech..."):
            audio_data = text_to_speech(llm_res)
        
        st.markdown(get_audio_player(audio_data), unsafe_allow_html=True)

if __name__ == "__main__":
    main()