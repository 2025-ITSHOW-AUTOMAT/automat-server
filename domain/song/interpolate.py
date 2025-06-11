import torch
from diffusers import StableDiffusionPipeline
from domain.song.utils.spectro import spectro_to_wav

from PIL import Image
import base64
from typing import List

MODEL_ID = "riffusion/riffusion-model-v1"
device = "cuda" if torch.cuda.is_available() else "cpu"

pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16 if device == "cuda" else torch.float32
).to(device)

def generate_interpolated_audio(prompts: List[str], num_steps: int = 5) -> bytes:
    spectrograms = []

    for i in range(len(prompts) - 1):
        for t in range(num_steps):
            alpha = t / num_steps
            blended = prompts[i] if alpha < 0.5 else prompts[i + 1]
            image = pipe(blended, height=512, width=768).images[0]
            spectrograms.append(image)

    spectrograms.append(pipe(prompts[-1], height=512, width=768).images[0])

    total_width = sum([img.width for img in spectrograms])
    combined = Image.new("RGB", (total_width, 512))
    x_offset = 0
    for img in spectrograms:
        combined.paste(img, (x_offset, 0))
        x_offset += img.width

    # WAV 파일로 변환
    wavs = spectro_to_wav(combined)
    return wavs[0].getvalue()

def generate_audio(prompts: List[str], steps: int = 5) -> str:
    audio_bytes = generate_interpolated_audio(prompts, steps)
    return base64.b64encode(audio_bytes).decode("utf-8")
