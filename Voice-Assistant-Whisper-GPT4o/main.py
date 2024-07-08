
import streamlit as st
from GPT40_llm import LLM_response
from STT_main import STT_AudioData, silero_vad_main
from TTS_main import text_to_speech
import os
# from dotenv import load_dotenv
import base64

# load_dotenv()

whisper = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
token = "Bearer " + st.secrets['HuggingFaceToken']
headers = {
    "Authorization": token,
    'Content-Type': 'audio/wav'
}

def process_audio(audio_file):
    audio_data = audio_file.read()
    vad_audio_data = silero_vad_main(audio_data)
    response = STT_AudioData(vad_audio_data, whisper, headers)
    prompt = response['text']
    reply = LLM_response(prompt)
    return prompt, reply

def main():
    st.title("Voice Assistant")

    uploaded_file = st.file_uploader("Upload an audio file", type=['wav', 'mp3', 'flac'])

    if uploaded_file is not None:
        st.audio(uploaded_file, format='audio/wav')

        if st.button("Process Audio"):
            with st.spinner("Processing audio..."):
                prompt, reply = process_audio(uploaded_file)

            st.subheader("Transcription:")
            st.write(prompt)

            st.subheader("Assistant's Reply:")
            st.write(reply)

            # Generate and play the voice reply
            audio_reply = text_to_speech(reply)
            st.audio(audio_reply, format='audio/wav')

            # Provide a download link for the audio reply
            b64_audio = base64.b64encode(audio_reply).decode()
            href = f'<a href="data:audio/wav;base64,{b64_audio}" download="assistant_reply.wav">Download Assistant\'s Voice Reply</a>'
            st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
