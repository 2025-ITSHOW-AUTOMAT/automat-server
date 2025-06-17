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

# def prompt_openai(base_prompts: list):
#     song_prompts = []
    
#     system_message = "You generate music prompts with genre suggestions."
#     for base_prompt in base_prompts:
#         user_message = (
#             f"Based on the following descriptions, create a song prompt that reflects the mood, atmosphere, and situation. "
#             f"Also, specify the song genre at the end.\n\nDescriptions: {base_prompt}"
#         )
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "system", "content": system_message},
#                 {"role": "user", "content": user_message}
#             ],
#             max_tokens=110,
#             temperature=0.7,
#         )
#         content = response.choices[0].message.content.strip()

#         song_genre = None
#         if "song_genre:" in content.lower():
#             parts = content.lower().split("song_genre:")
#             song_genre = parts[1].strip()
#             song_prompt = parts[0].strip()
#         else:
#             song_prompt = content
#             song_genre = None

#         if song_genre:
#             full_prompt = f"{song_genre} style music, {song_prompt}"
#         else:
#             full_prompt = song_prompt
        
#         song_prompts.append(full_prompt)

#     return song_prompts

def prompt_openai(base_prompts: list): # 테스트용 코드(나중에 지울 것)
    song_prompt = [
        "lo-fi hip hop style music, A joyful and uplifting lo-fi beat capturing the innocence and fun of childhood.",
        "lo-fi hip hop style music, A soothing ambient track with gentle synths and soft piano, evoking peace and reflection.",
        "lo-fi hip hop style music, A dark and moody electronic tune with pulsing bass, reflecting solitude and tension."
    ]
    
    return song_prompt


@router.post("/generate/song_prompt")
def generate_song_prompt(image_paths: list[str] = Body(...)):
    for image_path in image_paths:
        if not os.path.exists(image_path):
            raise HTTPException(status_code=404, detail=f"{image_path} not found")

    try:
        base_prompts = [generate_prompt(p) for p in image_paths]
        song_prompts = prompt_openai(base_prompts)
        translate_prompts = [translate_prompt(p) for p in song_prompts]

        return {
            "base_prompts": base_prompts,
            "song_prompts": song_prompts,
            "translate_prompts": translate_prompts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))