import torch
import torchaudio
import streamlit as st
from io import BytesIO
import numpy as np

model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad', force_reload=True)
(get_speech_timestamps, save_audio, read_audio, VADIterator, collect_chunks) = utils

def silero_vad_main(audio_data):
    try:
        # Convert audio data to numpy array
        audio_np = np.frombuffer(audio_data, dtype=np.int16)
        
        # Convert to float32 and normalize
        audio_float = audio_np.astype(np.float32) / 32768.0
        
        # Convert to torch tensor
        wav = torch.from_numpy(audio_float)
        
        # Assume original sample rate is 16000, adjust if different
        sr = 16000
        
        if wav.dim() == 2:
            wav = wav.mean(dim=0)  # Convert stereo to mono if necessary
        
        # Ensure the tensor is on the CPU
        wav = wav.cpu()
        
        threshold = 0.2
        min_speech_duration_ms = 100
        min_silence_duration_ms = 50
        
        speech_timestamps = get_speech_timestamps(
            wav,
            model,
            threshold=threshold,
            sampling_rate=sr,
            min_speech_duration_ms=min_speech_duration_ms,
            min_silence_duration_ms=min_silence_duration_ms
        )
        
        if len(speech_timestamps) > 0:
            voice_only = collect_chunks(speech_timestamps, wav)
            buffer = BytesIO()
            torchaudio.save(buffer, voice_only.unsqueeze(0), sr, format='wav')
            buffer.seek(0)
            vad_audio_data = buffer.read()
            print("Voice-only audio extracted.")
            return vad_audio_data
        else:
            print("No speech detected in the audio. Try speaking louder or adjusting the microphone.")
            return 0
    except Exception as e:
        print(f"An error occurred in silero_vad_main: {str(e)}")
        return None
