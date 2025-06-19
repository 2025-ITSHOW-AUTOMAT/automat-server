from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
from fastapi import APIRouter, HTTPException, Body
from dotenv import load_dotenv
load_dotenv()
from collections import Counter

from domain.prompt.emotionPrompt import analyze_emotion
from domain.prompt.translate import translate_prompt
from io import BytesIO
import requests
import os

router = APIRouter()

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base", use_fast=True)
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def generate_prompt(image_paths) -> str:
    if image_paths.startswith("http"):
        response = requests.get(image_paths)
        raw_image = Image.open(BytesIO(response.content)).convert("RGB")
    else:
        raw_image = Image.open(image_paths).convert("RGB")

    inputs = processor(raw_image, return_tensors="pt")
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)
    emotion = analyze_emotion(raw_image)
    return f"A {emotion} scene: {caption}."

@router.post("/generate/song_prompt")
def generate_song_prompt(image_paths: list[str] = Body(...)):
    for image_path in image_paths:
        if not os.path.exists(image_path):
            raise HTTPException(status_code=404, detail=f"{image_path} not found")

    try:
        base_prompts = [generate_prompt(p) for p in image_paths]
        song_prompts = [translate_prompt(p) for p in base_prompts]

        return {
            "base_prompts": base_prompts,
            "song_prompts": song_prompts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))