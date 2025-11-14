# src/audio_webrtc.py

import os
import uuid
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from streamlit_webrtc import AudioProcessorBase

import av

class AudioSaver(AudioProcessorBase):
    def __init__(self) -> None:
        self.frames = []

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        self.frames.append(frame)
        return frame

def save_audio_file(frames, output_dir="audio_input"):
    import wave

    filename = f"recorded_{uuid.uuid4().hex[:6]}.wav"
    filepath = os.path.join(output_dir, filename)

    if not frames:
        return None

    samples = b''.join([f.planes[0].to_bytes() for f in frames])

    with wave.open(filepath, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit PCM
        wf.setframerate(48000)
        wf.writeframes(samples)

    return filepath
