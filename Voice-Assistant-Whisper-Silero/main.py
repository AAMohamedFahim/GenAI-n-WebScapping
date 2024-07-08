import streamlit as st
from GPT40_llm import LLM_response
from STT_main import STT_AudioData, silero_vad_main
from TTS_main import text_to_speech
import os
from dotenv import load_dotenv
import base64

# ... (keep the rest of the imports and initial setup)

def main():
    st.title("Voice Assistant")

    uploaded_file = st.file_uploader("Upload an audio file", type=['wav', 'mp3', 'flac'])

    if uploaded_file is not None:
        st.audio(uploaded_file, format='audio/wav')
        file_size = uploaded_file.size
        st.write(f"Uploaded file size: {file_size} bytes")

        if file_size == 0:
            st.error("The uploaded file is empty. Please upload a valid audio file.")
        elif file_size > 5 * 1024 * 1024:  # 5 MB limit
            st.error("The uploaded file is too large. Please upload a file smaller than 5 MB.")
        else:
            if st.button("Process Audio"):
                with st.spinner("Processing audio..."):
                    prompt, reply = process_audio(uploaded_file)

                st.subheader("Transcription:")
                st.write(prompt)

                st.subheader("Assistant's Reply:")
                st.write(reply)

                try:
                    # Generate the voice reply
                    audio_reply = text_to_speech(reply)
                    st.write(f"Type of audio_reply: {type(audio_reply)}")
                    st.write(f"Length of audio_reply: {len(audio_reply) if audio_reply else 'None'}")

                    if audio_reply:
                        # Play the voice reply
                        st.audio(audio_reply, format='audio/wav')

                        # Provide a download link for the audio reply
                        b64_audio = base64.b64encode(audio_reply).decode()
                        href = f'<a href="data:audio/wav;base64,{b64_audio}" download="assistant_reply.wav">Download Assistant\'s Voice Reply</a>'
                        st.markdown(href, unsafe_allow_html=True)
                    else:
                        st.error("Failed to generate audio reply.")
                except Exception as e:
                    st.error(f"Error in audio processing: {str(e)}")

if __name__ == "__main__":
    main()
