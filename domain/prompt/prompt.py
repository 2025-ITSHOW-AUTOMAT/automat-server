from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
from fastapi import APIRouter, HTTPException, Body
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
from collections import Counter

from domain.prompt.emotionPrompt import analyze_emotion
from domain.prompt.translate import translate_prompt
import os

router = APIRouter()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base", use_fast=True)
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def generate_prompt(image_path) -> str:
    raw_image = Image.open(image_path).convert("RGB")
    inputs = processor(raw_image, return_tensors="pt")
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)

    emotion = analyze_emotion(image_path)

    prompt = f"A {emotion} scene: {caption}."
    return prompt

def prompt_openai(base_prompts: list):
    final = []
    genres = []
    
    system_message = (
        "You are a creative assistant that generates very short, concise song prompts "
        "based on image descriptions. Each prompt should be one sentence and include a fitting music genre."
    )
    
    for base_prompt in base_prompts:
        user_message = (
            f"Write a short, one-line song prompt (max 20 words) based on the following description, "
            f"and include a suitable genre at the beginning. Keep it concise and creative.\n\n"
            f"Description: {base_prompt}"
        )
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            max_tokens=60,
            temperature=0.8,
        )
        content = response.choices[0].message.content.strip()

        if ":" in content:
            genre, prompt = content.split(":", 1)
            genre = genre.strip().lower()
            prompt = prompt.strip()
        else:
            genre = "unknown"
            prompt = content.strip()

        genres.append(genre)
        final.append((genre, prompt))

    most_common_genre = Counter(genres).most_common(1)[0][0]

    song_prompts = [
        f"{most_common_genre} style music, {prompt}" for _, prompt in final
    ]

    return song_prompts

@router.post("/generate/song_prompt")
def generate_song_prompt(image_paths: list[str] = Body(...)):
    for image_path in image_paths:
        if not os.path.exists(image_path):
            raise HTTPException(status_code=404, detail=f"{image_path} not found")

    try:
        base_prompts = [generate_prompt(p) for p in image_paths]
        combined_prompt = " ".join(base_prompts)
        song_prompts = prompt_openai([combined_prompt])
        translate_prompts = [translate_prompt(p) for p in base_prompts]

        return {
            "base_prompts": base_prompts,
            "song_prompts": song_prompts,
            "translate_prompts": translate_prompts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))