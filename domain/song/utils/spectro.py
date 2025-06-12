import numpy as np
import io
import librosa
import soundfile as sf
from PIL import Image

def spectro_to_wav(image: Image.Image) -> bytes:
    img = np.array(image).astype(np.float32) / 255.0
    img = img[:, :, 0]

    mel = img.T
    mel = librosa.db_to_power(mel * 80.0 - 80.0)

    audio = librosa.feature.inverse.mel_to_audio(
        mel,
        sr=44100,
        n_fft=1024,
        hop_length=256,
        n_iter=32,
        win_length=1024
    )

    buffer = io.BytesIO()
    sf.write(buffer, audio, 44100, format='wav')
    buffer.seek(0)
    return buffer.read()