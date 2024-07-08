from gtts import gTTS
from io import BytesIO

def text_to_speech(text, lang='en'):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        audio_io = BytesIO()
        tts.write_to_fp(audio_io)
        audio_io.seek(0)
        return audio_io.getvalue()
    except Exception as e:
        print(f"An error occurred in text_to_speech: {e}")
        return None
