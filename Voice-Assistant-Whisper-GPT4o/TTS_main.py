from gtts import gTTS
import pygame
import streamlit as st
def text_to_speech(text, lang='en', output_file='output.mp3'):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(output_file)
        print(f"Audio content written to file '{output_file}'")
        pygame.mixer.init()
        pygame.mixer.music.load(output_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        print("Audio played successfully")
    except Exception as e:
        print(f"An error occurred: {e}")
        
# if __name__ == "__main__":
#     text = "i am fine. and you?"
#     output_file = "hello.mp3"
#     text_to_speech(text, output_file=output_file)
