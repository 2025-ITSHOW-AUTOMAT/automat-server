from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
from fastapi import APIRouter, HTTPException, Query
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
from domain.prompt.emotionPrompt import analyze_emotion
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
#     combined_prompt = " ".join(base_prompts)
    
#     # 노래 생성을 위한 프롬프트
#     system_message = "You generate music prompts with genre suggestions."
#     user_message = (
#         f"Based on the following descriptions, create a song prompt that reflects the mood, atmosphere, and situation. "
#         f"Also, specify the song genre at the end.\n\nDescriptions: {combined_prompt}"
#     )
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": system_message},
#             {"role": "user", "content": user_message}
#         ],
#         max_tokens=110,
#         temperature=0.7,
#     )
#     song_prompt_with_genre = response.choices[0].message.content.strip()
#     genre = None
#     if "genre:" in song_prompt_with_genre.lower():
#         parts = song_prompt_with_genre.lower().split("genre:")
#         genre = parts[1].strip()
#         song_prompt = parts[0].strip()
#     else:
#         song_prompt = song_prompt_with_genre
    
#     return song_prompt, genre

def prompt_openai(base_prompts: list): # 테스트용 코드(나중에 지울 것)
    song_prompt = (
        "A inspired by the prompt: 'A woman wearing a black shirt is sitting in a parked car, "
        "her hands partially covering her face. She wears headphones and speaks quietly on a cellphone, "
        "her expression tense and emotional. The mood feels introspective, private, and filled with quiet intensity, "
        "as if she's lost in thought or trying to hold back tears. The city lights blur outside the car window, "
        "casting soft reflections inside. Music plays gently in the background, matching the atmosphere.'"
    )
    genre = "lo-fi hip hop"
    
    return song_prompt, genre

    
@router.get("/generate/song_prompt")
def generate_song_prompt(image_path: str, genre: str = Query("pop")):
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    try:
        base_prompt = generate_prompt(image_path)
        song_prompt = prompt_openai(base_prompt, genre)
        return {"song_prompt": song_prompt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))