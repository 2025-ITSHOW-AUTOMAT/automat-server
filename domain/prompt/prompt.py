from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
from fastapi import APIRouter, HTTPException
from domain.prompt.emotionPrompt import analyze_emotion
import os

router = APIRouter()

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def generate_prompt(image_path) -> str:
    raw_image = Image.open(image_path).convert("RGB")
    inputs = processor(raw_image, return_tensors="pt")
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)

    emotion = analyze_emotion(image_path)

    prompt = (
        f"A {emotion} scene: {caption}. "
    )
    return prompt

@router.get("/analyze/emotion")
def emotion_api(image_path: str):
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    try:
        emotion = analyze_emotion(image_path)
        return {"emotion": emotion}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))