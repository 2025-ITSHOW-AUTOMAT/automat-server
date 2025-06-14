from ace_step import AceStep
import torch
import io
import soundfile as sf

def generate_ace_step(prompts: list[str], duration: int) -> bytes:
    try:
        model = AceStep()

        combined_prompt = " ".join(prompts)
        audio_tensor = model.generate(prompt=combined_prompt, duration=duration)

        audio_np = audio_tensor.cpu().numpy()
        buffer = io.BytesIO()
        sf.write(buffer, audio_np, 44100, format='wav')
        buffer.seek(0)

        return buffer.read()
        
    except Exception as e:
        print("Error generating WAV:", e)
        raise
