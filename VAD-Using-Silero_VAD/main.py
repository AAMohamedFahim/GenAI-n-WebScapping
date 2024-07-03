import torch
import torchaudio
import sounddevice as sd
model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                              model='silero_vad',
                              force_reload=True)
(get_speech_timestamps,
 save_audio,
 read_audio,
 VADIterator,
 collect_chunks) = utils

def record_audio(duration, samplerate=16000):
    print("Recording...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
    sd.wait()
    print("Recording finished")
    return audio.flatten()
duration = 15
audio = record_audio(duration)

print(f"Audio shape: {audio.shape}")
print(f"Audio min: {audio.min()}, max: {audio.max()}")

wav = torch.tensor(audio)

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

print(f"Number of speech segments detected: {len(speech_timestamps)}")

if len(speech_timestamps) > 0:
    voice_only = collect_chunks(speech_timestamps, wav)
    save_audio("voice_only.wav", voice_only, sampling_rate=16000)
    print("Voice-only audio saved as 'voice_only.wav'")
    for i, ts in enumerate(speech_timestamps):
        print(f"Segment {i+1}: start={ts['start']/16000:.2f}s, end={ts['end']/16000:.2f}s")
else:
    print("No speech detected in the audio. Try speaking louder or adjusting the microphone.")

torchaudio.save("full_recording.wav", wav.unsqueeze(0), 16000)
print("Full recording saved as 'full_recording.wav' for debugging")
