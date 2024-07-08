import torch
import torchaudio
from io import BytesIO
import streamlit as st

model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad', force_reload=True)
(get_speech_timestamps, save_audio, read_audio, VADIterator, collect_chunks) = utils

def silero_vad_main(audio_data):
    try:
        st.write(f"Audio data size: {len(audio_data)} bytes")
        wav, sr = torchaudio.load(BytesIO(audio_data))
        st.write(f"Audio loaded successfully. Shape: {wav.shape}, Sample rate: {sr}")
        
        if sr != 16000:
            resampler = torchaudio.transforms.Resample(orig_freq=sr, new_freq=16000)
            wav = resampler(wav)
            st.write("Audio resampled to 16kHz")
        
        wav = wav.flatten()
        
        threshold = 0.2
        min_speech_duration_ms = 100
        min_silence_duration_ms = 50
        
        speech_timestamps = get_speech_timestamps(
            wav,
            model,
            threshold=threshold,
            sampling_rate=16000,
            min_speech_duration_ms=min_speech_duration_ms,
            min_silence_duration_ms=min_silence_duration_ms
        )
        
        if len(speech_timestamps) > 0:
            voice_only = collect_chunks(speech_timestamps, wav)
            buffer = BytesIO()
            torchaudio.save(buffer, voice_only.unsqueeze(0), 16000, format='wav')
            buffer.seek(0)
            vad_audio_data = buffer.read()
            st.write("Voice-only audio extracted.")
            return vad_audio_data
        else:
            st.write("No speech detected in the audio. Try speaking louder or adjusting the microphone.")
            return audio_data
    except Exception as e:
        st.error(f"Error in silero_vad_main: {str(e)}")
        return audio_data
